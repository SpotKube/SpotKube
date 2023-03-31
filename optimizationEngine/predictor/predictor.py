from helpers import *

def predict(instance):
    region = "us-east-1"
    client = boto3.client('ec2', region_name=region)
    df = history(client, instance, region)
    price = interpolate(df)
    updateJson('../.spotConfig.json', instance, price)
    