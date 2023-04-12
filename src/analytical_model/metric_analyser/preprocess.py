import os
import sys
import pandas as pd
import cpuAnalyser, memoryAnalyser

def preprocess():
    df_cpu = pd.read_csv('../../load_testing/outputs/results_stats_history.csv')
    df_cpu = df_cpu[['User Count', 'Failures/s']]
    return df_cpu