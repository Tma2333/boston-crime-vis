import os
import pathlib
import json
import pandas as pd
import numpy as np
import logging


def import_data():
    # check dataset
    current_dir = pathlib.Path(__file__)
    data_dir = current_dir.parents[1] / 'data'
    data_path=  data_dir / 'crime.csv'
    if not data_path.exists():
        raise FileNotFoundError('Dataset not found')
    # import data
    df = pd.read_csv(data_path, engine='python')
    # remove duplicates
    df = df.drop_duplicates(subset=['INCIDENT_NUMBER'])
    # remove useless data
    df = df.drop(columns=['SHOOTING'])
    # remove nan in lat lon
    df = df.dropna(subset=['Lat', 'Long'])
    # remove invalid lat lon
    df = df[df['Lat'] > 40]
    df = df[df['Long'] < -65]
    return df
    

def get_location (df, filters):
    lat = np.array([])
    lon = np.array([])
    for header, keys in filters.items():
        for key in keys:
            df = df[df[header] == key]
            lat = np.append(lat, df['Lat'].to_numpy())
            lon = np.append(lon, df['Long'].to_numpy())
    logging.debug('lat lenth: {}'.format(lat.shape[0]))
    logging.debug('lon lenth: {}'.format(lon.shape[0]))
    return lat, lon


def get_map_png():
    current_dir = pathlib.Path(__file__)
    data_dir = current_dir.parents[1] / 'data'
    return data_dir / 'map.png'


def get_map_spec():
    current_dir = pathlib.Path(__file__)
    data_dir = current_dir.parents[1] / 'data'
    with open(data_dir/'map.json') as f:
        map_specs = json.load(f)
    extent = [map_specs['min_lon'], map_specs['max_lon'],
            map_specs['min_lat'], map_specs['max_lat']]
    return extent
    

def test(df):
    print(get_location(df, 'INCIDENT_NUMBER',['I182080058']))