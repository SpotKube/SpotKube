import boto3
import datetime
from fbprophet import Prophet
import pandas as pd

client = boto3.client('ec2', region_name='us-east-1')
# regions = [x["RegionName"] for x in client.describe_regions()["Regions"]]

regions = ['us-east-1']

INSTANCE = "m4.large"
print("Instance: %s" % INSTANCE)

STARTTIME = (datetime.datetime.now() - datetime.timedelta(days=20)).isoformat()
print("Start Time is: %s" % STARTTIME)

results = []

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

    
df = pd.DataFrame.from_dict(results)
df = df.rename(columns={'Timestamp': 'ds', 'Price': 'y'})

df_new = df.sort_values('y', ascending=False).drop_duplicates('ds').sort_index()

# print(df_new)

def interpolate(df):
    model = Prophet(
        daily_seasonality = True,
        yearly_seasonality = False,
    )
    model.fit(df)
    
    future = model.make_future_dataframe(periods=1)
    forecast = model.predict(future)
    predicted_price = forecast['yhat'].iloc[-1]
    
    print('Predicted spot price:', round(predicted_price, 3))
    
    return round(predicted_price, 3)
    
interpolate(df_new)
print(df_new)