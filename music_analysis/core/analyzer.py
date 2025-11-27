import pandas as pd
import numpy as np

def compute_kpis(df):
    """
    Computes basic KPIs from the dataframe.
    """
    kpis = {}
    if df.empty:
        return kpis
        
    kpis['total_tracks'] = len(df)
    if 'duration_ms' in df.columns:
        kpis['avg_duration_min'] = df['duration_ms'].mean() / 60000
    
    if 'tempo' in df.columns:
        kpis['avg_bpm'] = df['tempo'].mean()
        kpis['std_bpm'] = df['tempo'].std()
        
    return kpis
