from .aws_service import get_on_demand_pricing, get_running_instances, get_spot_pricing

def get_spot_instances():
    running_instances = get_running_instances()
    spot_instances = []
    on_demand_pricing = {}
    spot_pricing = {}
    for instance in running_instances:
        for tag in instance['tags']:
            if tag['Key'] != 'Name':
                continue
            if tag['Value'] not in ['spotkube_master_node', 'spotkube_managment_node']: # 'spotkube_worker_node',
                if instance['instanceType'] not in on_demand_pricing:
                    on_demand_pricing[instance['instanceType']] = get_on_demand_pricing(instance['instanceType'])
                if instance['instanceType'] not in spot_pricing:
                    spot_pricing[instance['instanceType']] = get_spot_pricing(instance['instanceType'], 'us-east-1')
                ec2Details = {
                    'instanceId': instance['instanceId'],
                    'instanceType': instance['instanceType'],
                    'onDemandPricing': on_demand_pricing[instance['instanceType']],
                    'spotPricing': spot_pricing[instance['instanceType']],
                } 
                spot_instances.append(ec2Details)
            break
    return spot_instances
