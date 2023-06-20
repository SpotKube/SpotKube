

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

def get_running_instances(region):
    ec2 = boto3.client('ec2', region_name=region)
    
    response = ec2.describe_instances()
    
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            tags = []
            if 'Tags' in instance:
                tags = instance['Tags']
            ec2Details = {
                'instanceId': instance['InstanceId'],
                'instanceType': instance['InstanceType'],
                'tags':tags,
            } 
            instances.append(ec2Details)
    return instances

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

def get_aws_billing_data(start_date, end_date):
    # Create a Boto3 client for the Cost Explorer service
    ce_client = boto3.client('ce')

    # Specify the time period for which you want to retrieve billing data
    time_period = {
        'Start': start_date,
        'End': end_date
    }

    # Specify the metrics you want to retrieve
    metrics = ['BlendedCost']  # You can add more metrics like 'UnblendedCost', 'UsageQuantity', etc.

    # Make the API call to get the billing data
    response = ce_client.get_cost_and_usage(
        TimePeriod=time_period,
        Granularity='DAILY',  # You can specify other granularities like 'MONTHLY', 'HOURLY', etc.
        Metrics=metrics
    )

    # Retrieve the data from the response
    results = response['ResultsByTime']

    # Print the billing data for each day
    for result in results:
        start = result['TimePeriod']['Start']
        end = result['TimePeriod']['End']
        cost = result['Total']['BlendedCost']['Amount']
        unit = result['Total']['BlendedCost']['Unit']

        print(f"Period: {start} - {end}")
        print(f"Cost: {cost} {unit}")
        print('---')
