
import boto3
import datetime
from prophet import Prophet
import pandas as pd
import json as json
import yaml
import os

from pkg_resources import resource_filename


dir_path = os.path.dirname(os.path.abspath(__file__))
results = []

def history(client, instance, region):
    INSTANCE = instance
    STARTTIME = (datetime.datetime.now() - datetime.timedelta(days=20)).isoformat()
    
    prices = client.describe_spot_price_history(
        InstanceTypes=[INSTANCE],
        ProductDescriptions=['Linux/UNIX'],
        AvailabilityZone="{region_}a".format(region_= region),
        StartTime=STARTTIME,
        MaxResults=100
    )
    # print("Prices for region %s: %s" % (region, prices["SpotPriceHistory"]))
    for price in prices["SpotPriceHistory"]:
        results.append({
                        'Timestamp': price["Timestamp"].strftime('%m-%d-%Y'), 
                        'Price': price["SpotPrice"]
                        })

        
    df = pd.DataFrame.from_dict(results)
    df = df.rename(columns={'Timestamp': 'ds', 'Price': 'y'})
    df = df.sort_values('y', ascending=False).drop_duplicates('ds').sort_index()
    
    return df

def get_region_name(region_code):

    endpoint_file = resource_filename('botocore', 'data/endpoints.json')

    with open(endpoint_file, 'r') as f:
        endpoint_data = json.load(f)

    region_name = endpoint_data['partitions'][0]['regions'][region_code]['description']

    region_name = region_name.replace('Europe', 'EU')

    return region_name

def get_ec2_instance_hourly_price(region_code, 
                                  instance_type, 
                                  operating_system, 
                                  preinstalled_software='NA', 
                                  tenancy='Shared', 
                                  is_byol=False):
    
    region_name = get_region_name(region_code)                                  
    if is_byol:
        license_model = 'Bring your own license'
    else:
        license_model = 'No License required'

    if tenancy == 'Host':
        capacity_status = 'AllocatedHost'
    else:
        capacity_status = 'Used'
    
    filters = [
        {'Type': 'TERM_MATCH', 'Field': 'termType', 'Value': 'OnDemand'},
        {'Type': 'TERM_MATCH', 'Field': 'capacitystatus', 'Value': capacity_status},
        {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region_name},
        {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
        {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': tenancy},
        {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': operating_system},
        {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': preinstalled_software},
        {'Type': 'TERM_MATCH', 'Field': 'licenseModel', 'Value': license_model},
    ]

    pricing_client = boto3.client('pricing', region_name=region_code)
    
    response = pricing_client.get_products(ServiceCode='AmazonEC2', Filters=filters)

    for price in response['PriceList']:
        price = json.loads(price)

        for on_demand in price['terms']['OnDemand'].values():
            for price_dimensions in on_demand['priceDimensions'].values():
                price_value = price_dimensions['pricePerUnit']['USD']
            
        return round(float(price_value), 4)
    return 1e6

def interpolate(df, instance, region):
    model = Prophet(
        daily_seasonality = True,
        yearly_seasonality = False,
    )
    model.fit(df)
    
    future = model.make_future_dataframe(periods=1)
    forecast = model.predict(future)
    predicted_price = forecast['yhat'].iloc[-1]
    on_demand_price = get_ec2_instance_hourly_price(region, instance, "Linux")
    print("On demand", on_demand_price)
    bidding_price = round(predicted_price + predicted_price*0.05, 4)
    
    return min(on_demand_price, bidding_price)

def updateJson(file, instance, cost=None, cpu=None, mem=None):
    with open(file, "r") as jsonFile:
        data = json.load(jsonFile)

    if(cpu):
        data[instance]["cpu"] = cpu
    if(mem):
        data[instance]["memory"] = mem
    if(cost):
        data[instance]["cost"] = cost
        data[instance]["date"] = str(datetime.datetime.now().date())
        
    with open(file, "w") as jsonFile:
        json.dump(data, jsonFile)
    
def readYml(file):
    with open(file, "r") as stream:
        try:
            data = yaml.safe_load(stream)
            return data   
        except yaml.YAMLError as exc:
            print(exc)

def readJson(file):
    with open(file, "r") as jsonFile:
        data = json.load(jsonFile)
    return data

def getSpotInstances():
    file_path = os.path.join(dir_path, '../.spotConfig.json')
    spot_data = readJson(file_path)
    instances = list(spot_data.keys())
    return instances
        
    