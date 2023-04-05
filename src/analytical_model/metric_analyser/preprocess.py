import os
import sys
import pandas as pd
import cpuAnalyser, memoryAnalyser

def preprocess():
    df_cpu = pd.read_csv('../../load_testing/output/cpu.csv')
    df_mem = pd.read_csv('../../load_testing/output/mem.csv')

    df_cpu['rps'] = (df_cpu.index + 1) * 100
    df_mem['rps'] = (df_mem.index + 1) * 100

    df_cpu['cpu_usage'] = round(df_cpu['cpu_usage'], 3)
    df_mem['memory_usage'] = round(df_mem['memory_usage']/1000000000, 3)


    print(df_cpu.head())
    print(df_mem.head())
    
    return df_cpu, df_mem