import boto3
import datetime
from fbprophet import Prophet
import pandas as pd
import json as json


results = []

def history(client, instance, region_):
    INSTANCE = instance
    STARTTIME = (datetime.datetime.now() - datetime.timedelta(days=20)).isoformat()
    
    prices = client.describe_spot_price_history(
        InstanceTypes=[INSTANCE],
        ProductDescriptions=['Linux/UNIX'],
        AvailabilityZone="{region_}a".format(region_= region_),
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

def updateJson(file, instance, price):
    with open(file, "r") as jsonFile:
        data = json.load(jsonFile)

    data[instance]["cost"] = price
    data[instance]["date"] = str(datetime.datetime.now().date())

    with open(file, "w") as jsonFile:
        json.dump(data, jsonFile)
    
if __name__ == '__main__':
    region = "us-east-1"
    instance = "t3.medium"
    client = boto3.client('ec2', region_name=region)
    df = history(client, instance, region)
    price = interpolate(df)
    updateJson('./.spotConfig.json', instance, price)
