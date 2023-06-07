import os
import sys
import pandas as pd

def preprocess(service):
    df_cpu = pd.read_csv('../load_testing/outputs/'+service+'/results_stats_history.csv')
    df_cpu = df_cpu[['User Count', 'Failures/s']]
    return df_cpu
