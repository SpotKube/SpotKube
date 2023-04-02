from helpers import *
import os

def predict(instance):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, '../.spotConfig.json')
    region = "us-east-1"
    client = boto3.client('ec2', region_name=region)
    df = history(client, instance, region)
    price = interpolate(df)
    updateJson(file_path, instance, price)
    