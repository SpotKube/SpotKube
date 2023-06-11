from .aws_service import get_on_demand_pricing, get_running_instances, get_spot_pricing

region = 'us-east-1'

def get_spot_instances():
    running_instances = get_running_instances(region)
    spot_instances = {}
    spot_instances_arr = []

    for instance in running_instances:
        for tag in instance['tags']:
            if tag['Key'] != 'Name':
                continue
            if tag['Value'] not in ['spotkube_master_node', 'spotkube_managment_node']: # 'spotkube_worker_node',
                if instance['instanceType'] not in spot_instances:

                    spot_instances[instance['instanceType']] = {
                        'instanceType': instance['instanceType'],
                        'count': 1,
                        'onDemandPricing': get_on_demand_pricing(instance['instanceType']),
                        'spotPricing': get_spot_pricing(instance['instanceType'], region),
                    }
                else:
                    spot_instances[instance['instanceType']]['count'] += 1

            break

    # Create spot_instances_arr array from spot_instances dict
    for key, value in spot_instances.items():
        spot_instances_arr.append(value)

    return spot_instances_arr
