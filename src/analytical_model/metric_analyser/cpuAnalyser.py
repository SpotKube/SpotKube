import pandas as pd
import numpy as np

def analyse(df):
    throttling_points = df.loc[df['Failures/s'] > 1 ]
    if len(throttling_points) != 0:
        throttling_request_rate = throttling_points['User Count'].iloc[0]
    else:
        throttling_request_rate = df['User Count'].iloc[-1]
    return throttling_request_rate
