from helpers import history, interpolate, updateJson
import os
import boto3
import sys

dirs = ['optimizer', 'cost_model']
for i in dirs:
    package_path = os.path.abspath(i)
    sys.path.append(package_path)

def predict(instance):
    print(f"{instance} Prediction Started")
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, '../.spotConfig.json')
    region = "us-east-1"
    client = boto3.client('ec2', region_name=region)
    df = history(client, instance, region)
    price = interpolate(df)
    updateJson(file_path, instance, cost = price)
    