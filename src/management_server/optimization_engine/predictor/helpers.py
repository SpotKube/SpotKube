import boto3
import datetime
from fbprophet import Prophet
import pandas as pd
import json as json
import yaml
import os


dir_path = os.path.dirname(os.path.abspath(__file__))
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
    
    print('Predicted spot price:', round(predicted_price, 4))
    print('Saved spot price:', round(predicted_price + predicted_price*0.05, 4) )
    return round(predicted_price + predicted_price*0.05, 4)

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
        
    