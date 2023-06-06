import requests
import json
import sys
import pandas as pd
import numpy as np
import time

def fetch_cpu_metrics(service, host, start, end, api_token):
    url = f"{host}/api/ds/query"
    expr = "sum(rate(container_cpu_usage_seconds_total{container=\""+service+"\"}[5m])) by (container) /sum(container_spec_cpu_quota{container=\""+service+"\"}/container_spec_cpu_period{container=\""+service+"\"}) by (container)"
    # expr = "sum(rate(container_cpu_usage_seconds_total{container=\""+service+"\"}[10m])) by (name) *100"
    body = {
        "queries": [
            {
                "editorMode": "code",
                "expr": expr,
                "legendFormat": "__auto",
                "range": True,
                "instant": False,
                "exemplar": False,
                "utcOffsetSec": 19800,
                "interval": "",
                "datasourceId": 1,
                "intervalMs": 10000,
                "maxDataPoints": 1791
            }
        ],
        "from": start,
        "to": end
    }
    response = requests.post(url, headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}, data=json.dumps(body))
    json_response = json.loads(response.text)

    print(json_response)
    
    data = json_response["results"]["A"]["frames"][0]["data"]["values"]
    return data

def fetch_memory_metrics(service, host, start, end, api_token):
    url = f"{host}/api/ds/query"
    expr = "sum(container_memory_rss{container=\""+service+"\"}) by (name) /1000000000"
    body = {
        "queries": [
            {
                "editorMode": "code",
                "expr": expr,
                "legendFormat": "__auto",
                "range": True,
                "instant": False,
                "exemplar": False,
                "utcOffsetSec": 19800,
                "interval": "",
                "datasourceId": 1,
                "intervalMs": 10000,
                "maxDataPoints": 1791
            }
        ],
        "from": start,
        "to": end
    }
    response = requests.post(url, headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}, data=json.dumps(body))
    json_response = json.loads(response.text)
    
    print(json_response)
    
    data = json_response["results"]["A"]["frames"][0]["data"]["values"]
    return data

if __name__ == "__main__":
    args = sys.argv
    service = args[1]
    host = args[2]
    users = int(args[3])
    rate = int(args[4])
    start = args[5]
    end = time.time()*1000 #args[6]
    api_token = args[7]


    mem_data = fetch_memory_metrics(service, host, start, end, api_token)
    dic_mem = {'timestamp': np.array(mem_data[0]), 'memory_usage': np.array(mem_data[1])}
    df_mem = pd.DataFrame(dic_mem)

    cpu_data = fetch_cpu_metrics(service, host, start, end, api_token)
    dic_cpu = {'timestamp': np.array(cpu_data[0]), 'cpu_usage': np.array(cpu_data[1])}
    df_cpu = pd.DataFrame(dic_cpu)

    df_cpu.to_csv("cpu.csv", index=False)
    df_mem.to_csv("mem.csv", index=False)
