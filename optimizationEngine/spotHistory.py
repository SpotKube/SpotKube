import boto3
import datetime
from scipy.interpolate import interp1d

client = boto3.client('ec2', region_name='us-east-1')
# regions = [x["RegionName"] for x in client.describe_regions()["Regions"]]

regions = ['us-east-1']

INSTANCE = "p2.xlarge"
print("Instance: %s" % INSTANCE)

STARTTIME = (datetime.datetime.now() - datetime.timedelta(days=30)).isoformat()
print("Start Time is: %s" % STARTTIME)

results = []
output = []
vectors = {
    'x': [],
    'y': []
}

for region in regions:
    client = boto3.client('ec2', region_name=region)
    prices = client.describe_spot_price_history(
        InstanceTypes=[INSTANCE],
        ProductDescriptions=['Linux/UNIX'],
        AvailabilityZone='us-east-1a',
        StartTime=STARTTIME,
        MaxResults=100
    )
    # print("Prices for region %s: %s" % (region, prices["SpotPriceHistory"]))
    for price in prices["SpotPriceHistory"]:
        results.append({
                        'Timestamp': price["Timestamp"].strftime('%m-%d-%Y'), 
                        'Price': price["SpotPrice"]
                        })

# for region, price in sorted(results, key=lambda x: x[1]):
#     print("Region: %s price: %s" % (region, price))
    count = 1
    price = 0
    for i in range(len(results)):
        # this will not add the last timestamp to the output
        # print("%sth result: %s" % (i, results[i]))
        if i == 0:
            temp = results[i]['Timestamp']
        else:
            if count == 1:
                    price += float(results[i-1]['Price'])
            if (results[i]['Timestamp'] == temp):
                count += 1
                price += float(results[i]['Price'])
            else:
                output.append({
                    'Timestamp': results[i-1]['Timestamp'], 
                    'Price': round(price/count, 3) 
                })
                vectors['x'].append(results[i-1]['Timestamp'])
                vectors['y'].append(round(price/count, 3))
                count = 1
                price = 0
                temp = results[i]['Timestamp']
        
        
# print(output)
# print(vectors)

def interpolate(vectors, x):
    # Finding the interpolation
    y_interp = interp1d(vectors['x'], vectors['y'])
    print("Value of Y at x = {} is".format(x),
        y_interp(x))
    
interpolate(vectors, '02-24-2023')