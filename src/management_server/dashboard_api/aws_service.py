

import boto3
import json

# Return on-deamnd pricing for a given instance type
def get_on_demand_pricing(instance_type):
    client = boto3.client('pricing', region_name='us-east-1')  # Adjust the region as per your requirement

    response = client.get_products(
        ServiceCode='AmazonEC2',
        Filters=[
            {
                'Type': 'TERM_MATCH',
                'Field': 'instanceType',
                'Value': instance_type
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'tenancy',
                'Value': 'Shared'  # Adjust the tenancy value as per your requirement (e.g., Dedicated, Host)
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'operatingSystem',
                'Value': 'Linux'  # Adjust the operating system value as per your requirement (e.g., Windows, Linux)
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'preInstalledSw',
                'Value': 'NA'  # Adjust the pre-installed software value as per your requirement (e.g., SQL, NA)
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'capacitystatus',
                'Value': 'Used'  # Adjust the capacity status value as per your requirement (e.g., Used, Unused)
            },
        ],
        MaxResults=1  # Adjust the MaxResults value as per your requirement
    )

    products = response['PriceList']
    price_list = json.loads(products[0])['terms']['OnDemand']
    price_dimension_key = next(iter(price_list))
    price_dimension = price_list[price_dimension_key]['priceDimensions']
    price_per_unit_key = next(iter(price_dimension))
    price_per_unit = price_dimension[price_per_unit_key]['pricePerUnit']['USD']
    price = float(price_per_unit)

    return price

# instance_type = 't2.micro'  # Replace with the desired instance type
# price = get_on_demand_pricing(instance_type)
# print(f"On-demand pricing for {instance_type}: ${price}/hour")

# Return spot instances in a given vpc

def get_running_instances(region):
    ec2 = boto3.client('ec2', region_name=region)
    
    response = ec2.describe_instances()
    
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            ec2Details = {
                'instanceId': instance['InstanceId'],
                'instanceType': instance['InstanceType'],
                'tags': instance['Tags'],
            } 
            instances.append(ec2Details)
    return instances

import boto3

def get_spot_pricing(instance_type, region):
    ec2_client = boto3.client('ec2', region_name=region)

    response = ec2_client.describe_spot_price_history(
        InstanceTypes=[instance_type],
        MaxResults=10,
        ProductDescriptions=['Linux/UNIX'],
        AvailabilityZone=region+'a', # Currently only supports one AZ, 
    )

    prices = []
    for price in response['SpotPriceHistory']:
        prices.insert(0, {'timestamp':price['Timestamp'], 'price':price['SpotPrice']})
    return prices
