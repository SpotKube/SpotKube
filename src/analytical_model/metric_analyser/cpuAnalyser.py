import pandas as pd
import numpy as np

def analyse(df):
    throttling_points = df.loc[df['Failures/s'] > 1 ]
    throttling_request_rate = throttling_points['User Count'].iloc[0]
    return throttling_request_rate
