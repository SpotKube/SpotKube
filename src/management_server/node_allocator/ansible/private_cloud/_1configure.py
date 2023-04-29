import subprocess
import os
import json
import ansible.constants as C
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
from ansible import context

from utils import get_logger, format_terraform_error_message, run_subprocess_cmd

current_dir = os.getcwd()
ansible_dir = os.path.join(current_dir, "node_allocator", "ansible", "private_cloud")
terraform_dir = os.path.join(current_dir, "node_allocator", "terraform", "private_cloud")

# Create a callback plugin so we can capture the output
class ResultsCollectorJSONCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in.

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin.
    """

    def __init__(self, *args, **kwargs):
        super(ResultsCollectorJSONCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        host = result._host
        self.host_unreachable[host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        """Print a json representation of the result.

        Also, store the result in an instance attribute for retrieval later
        """
        host = result._host
        self.host_ok[host.get_name()] = result
        print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_failed(self, result, *args, **kwargs):
        host = result._host
        self.host_failed[host.get_name()] = result


async def generate_private_cloud_hosts_file():
    # Read control_plane_ip and worker_ips from input.json using jq
    with open(f"{terraform_dir}/private_instance_terraform_output.json") as f:
        output = json.load(f)
        control_plane_ip = output['private_master_ip']['value']
        worker_ips = [worker['private_ip'] for worker in output['private_workers']['value']]
        
    CONFIG_PATH = '~/.config/spotkube/provisioner.conf'
    config_path_expanded = os.path.expanduser(CONFIG_PATH)
    key_name = None

    with open(config_path_expanded, "r") as f:
        for line in f:
            if line.startswith("PRIVATE_INSTANCE_SSH_KEY_PATH="):
                key_path = line.strip().split("=")[1]
                key_name = key_path.split("/")[-1].replace("'", "")

    print(key_name)

    # Write the Ansible hosts file
    with open(f'{ansible_dir}/hosts', 'w') as f:
        f.write('[control_plane]\n')
        f.write(f'{control_plane_ip}\n\n')
        f.write('[workers]\n')
        for worker_ip in worker_ips:
            f.write(f'{worker_ip}\n')
        f.write('\n')
        f.write('[control_plane:vars]\n')
        f.write('ansible_connection=ssh\n')
        f.write('ansible_user=ubuntu\n')
        f.write(f'ansible_ssh_private_key_file=~/.ssh/{key_name}\n\n')
        f.write('[workers:vars]\n')
        f.write('ansible_connection=ssh\n')
        f.write('ansible_user=ubuntu\n')
        f.write(f'ansible_ssh_private_key_file=~/.ssh/{key_name}\n')
        
    return {"message": "Ansible hosts file generated", "status": "success"}
        
async def removed_configure_private_nodes():
    # Generate the Ansible hosts file
    await generate_private_cloud_hosts_file()
    
    # Run the initial playbook
    output = run_subprocess_cmd(["ansible-playbook", "-i", "hosts", "initial.yml"], cwd=ansible_dir)
    print(output)
    
    # Run the kube-dependencies playbook
    output = run_subprocess_cmd(["ansible-playbook", "-i", "hosts", "kube-dependencies.yml"], cwd=ansible_dir)
    print(output)
    
    # Run the control-plane playbook
    output = run_subprocess_cmd(["ansible-playbook", "-i", "hosts", "control-plane.yml"], cwd=ansible_dir)
    print(output)
    
    return {"message": "Nodes configured", "status": "success"}

async def rm_configure_private_nodes():
    # Generate the Ansible hosts file
    await generate_private_cloud_hosts_file()
    
    # Run the playbooks
    # playbook_paths = ["initial.yml", "kube-dependencies.yml", "control-plane.yml"]
    # playbook_paths = [f"{ansible_dir}/initial.yml"]
    # inventory = InventoryManager(loader=None, sources="hosts")
    # playbook_executor = PlaybookExecutor(playbooks=playbook_paths,
    #                                       inventory=inventory,
    #                                       variable_manager=None,
    #                                       loader=None,
    #                                       passwords=None)
    # playbook_executor.run()
    
    host_list = ['localhost', 'www.example.com', 'www.google.com']
    # since the API is constructed for CLI it expects certain options to always be set in the context object
    context.CLIARGS = ImmutableDict(connection='smart', module_path=['/to/mymodules', '/usr/share/ansible'], forks=10, become=None,
                                    become_method=None, become_user=None, check=False, diff=False, verbosity=0)
    # required for
    # https://github.com/ansible/ansible/blob/devel/lib/ansible/inventory/manager.py#L204
    sources = ','.join(host_list)
    if len(host_list) == 1:
        sources += ','
    
    # initialize needed objects
    loader = DataLoader()  # Takes care of finding and reading yaml, json and ini files
    passwords = dict(vault_pass='secret')

    # Instantiate our ResultsCollectorJSONCallback for handling results as they come in. Ansible expects this to be one of its main display outlets
    results_callback = ResultsCollectorJSONCallback()

    # create inventory, use path to host config file as source or hosts in a comma separated string
    inventory = InventoryManager(loader=loader, sources=sources)

    # variable manager takes care of merging all the different sources to give you a unified view of variables available in each context
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    # instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host list and tasks
    # IMPORTANT: This also adds library dirs paths to the module loader
    # IMPORTANT: and so it must be initialized before calling `Play.load()`.
    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        passwords=passwords,
        stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
    )

    # create data structure that represents our play, including tasks, this is basically what our YAML loader does internally.
    play_source = dict(
        name="Ansible Play",
        hosts=host_list,
        gather_facts='no',
        tasks=[
            dict(action=dict(module='shell', args='ls'), register='shell_out'),
            dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}'))),
            dict(action=dict(module='command', args=dict(cmd='/usr/bin/uptime'))),
        ]
    )

    # Create play object, playbook objects use .load instead of init or new methods,
    # this will also automatically create the task objects from the info provided in play_source
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    # Actually run it
    try:
        result = tqm.run(play)  # most interesting data for a play is actually sent to the callback's methods
    finally:
        # we always need to cleanup child procs and the structures we use to communicate with them
        tqm.cleanup()
        if loader:
            loader.cleanup_all_tmp_files()

    # Remove ansible tmpdir
    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    print("UP ***********")
    for host, result in results_callback.host_ok.items():
        print('{0} >>> {1}'.format(host, result._result['stdout']))

    print("FAILED *******")
    for host, result in results_callback.host_failed.items():
        print('{0} >>> {1}'.format(host, result._result['msg']))

    print("DOWN *********")
    for host, result in results_callback.host_unreachable.items():
        print('{0} >>> {1}'.format(host, result._result['msg']))
    
    return {"message": "Nodes configured", "status": "success"}


async def configure_private_nodes():
    # Generate the Ansible hosts file
    # await generate_private_cloud_hosts_file()
    
    loader = DataLoader()  # Takes care of finding and reading yaml, json and ini files
    passwords = dict(vault_pass='secret')
    
    # set up inventory
    inventory = InventoryManager(loader=DataLoader(), sources=os.path.join(ansible_dir, 'hosts'))
    
    # set up variables
    variable_manager = VariableManager(loader=DataLoader(), inventory=inventory)
    
    # set up callback plugin
    results_callback = ResultsCollectorJSONCallback()
    
    # set up options
    context.CLIARGS = ImmutableDict(connection='local', module_path=[os.path.join(ansible_dir, 'library')],
                                    forks=10, become=None, become_method=None, become_user=None,
                                    check=False, diff=False, verbosity=0)
    
    # create the play
    play_source = dict(
        name="Configure Private Nodes",
        hosts="all",
        gather_facts='no',
        tasks=[
            dict(name="Run Initial Playbook", include_tasks=os.path.join(ansible_dir, "initial.yml")),
            dict(name="Install Kubernetes Dependencies", include_tasks=os.path.join(ansible_dir, "kube-dependencies.yml")),
            dict(name="Configure Kubernetes Control Plane", include_tasks=os.path.join(ansible_dir, "control-plane.yml"))
        ]
    )
    play = Play().load(play_source, variable_manager=variable_manager, loader=DataLoader())
    
    # execute the play
    tqm = TaskQueueManager(inventory=inventory, variable_manager=variable_manager, loader=DataLoader(),
                           passwords=dict(), stdout_callback=results_callback)
    # Actually run it
    try:
        result = tqm.run(play)  # most interesting data for a play is actually sent to the callback's methods
    finally:
        # we always need to cleanup child procs and the structures we use to communicate with them
        tqm.cleanup()
        if loader:
            loader.cleanup_all_tmp_files()

    # # Remove ansible tmpdir
    # shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    print("UP ***********")
    for host, result in results_callback.host_ok.items():
        print('{0} >>> {1}'.format(host, result._result['stdout']))

    print("FAILED *******")
    for host, result in results_callback.host_failed.items():
        print('{0} >>> {1}'.format(host, result._result['msg']))

    print("DOWN *********")
    for host, result in results_callback.host_unreachable.items():
        print('{0} >>> {1}'.format(host, result._result['msg']))
    
    return {"message": "Nodes configured", "status": "success"}

        
