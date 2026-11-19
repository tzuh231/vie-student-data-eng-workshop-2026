import pandas as pd
import numpy as np
from pathlib import Path
import datetime as dt

import os


path1 = Path('data/raw/1a5a47a0649e4ee9.csv')
path2 = Path('data/raw/3d7a0493484e7dbe.csv')

def read_data(data_path:Path):
    df = pd.read_csv(data_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def sanity_checks(data):
    if data['timestamp'].nunique() != data.shape[0]:
        raise ValueError("Non unique timestamps")
    return

def create_1min(data):
    return data

def create_5min(data):
    df = data.resample('5min',on='timestamp').agg({
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum'})

    return df

def pipeline(input_path:Path):
    df = read_data(input_path)
    sanity_checks(df)
    name = df['ticker'][0]
    date = df['timestamp'].astype(str)[0][:10]

    ticker_folder = name
    date_subfolder = date
    outdir = Path(f'data/clean'+f'/{ticker_folder}'+f'/{date_subfolder}')

    if not os.path.exists(outdir):
        os.makedirs(outdir)
        print('hey')

    min1 = create_1min(df)
    min5 = create_5min(df)
    min1.to_csv(f"{outdir}/bars_1min.csv")
    min5.to_csv(f"{outdir}/bars_5min.csv")
    
    return


for p in sorted(Path('data/raw').glob('*.csv')):
    try:
        pipeline(p)
    except ValueError as e:
        print('skipped', p.name, e)
