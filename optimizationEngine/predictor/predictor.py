from helpers import *

def predict():
    region = "us-east-1"
    instance = "t2.small"
    client = boto3.client('ec2', region_name=region)
    df = history(client, instance, region)
    price = interpolate(df)
    updateJson('../.spotConfig.json', instance, price)
    

if __name__ == '__main__':
   predict()