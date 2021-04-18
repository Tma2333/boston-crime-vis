import os
import pathlib
import json
import pandas as pd
import numpy as np
import logging


def import_data():
    # check dataset
    logging.info('Importing data...')
    current_dir = pathlib.Path(__file__)
    data_dir = current_dir.parents[1] / 'data'
    data_path=  data_dir / 'crime.csv'
    if not data_path.exists():
        logging.error('Dataset not found, you can find information about access the dataset in /data')
        raise FileNotFoundError('Dataset not found')
    # import data
    df = pd.read_csv(data_path, engine='python')
    logging.info('Data imported & Processing....')
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
    try:
        logging.debug(filters)
        header_ds = pd.DataFrame(df)
        for header, keys in filters.items():
            if keys == 'all':
                continue
            ds = pd.DataFrame()
            for key in keys:
                temp = header_ds[header_ds[header] == key]
                ds=pd.concat([ds,temp])
            ds = ds.dropna(subset=['Lat', 'Long'])
            header_ds = pd.DataFrame(ds)
        lat = np.append(lat, header_ds['Lat'].to_numpy())
        lon = np.append(lon, header_ds['Long'].to_numpy())
        logging.debug('lat lenth: {}'.format(lat.shape[0]))
        logging.debug('lon lenth: {}'.format(lon.shape[0]))
    except Exception as e:
        logging.fatal(e)
        logging.fatal('shit hits the fan')
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