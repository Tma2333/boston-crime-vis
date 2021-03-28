import os
import pandas as pd
import numpy as np


def import_data():
    # check dataset
    current_dir = os.path.realpath(__file__)
    parent_dir = os.path.dirname(os.path.dirname(current_dir))
    data_dir = os.path.join(parent_dir, 'data', 'crime.csv')
    if not os.path.exists(data_dir):
        raise FileNotFoundError('Dataset not found')
    # import data
    df = pd.read_csv(data_dir, engine='python')
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
    

def get_location (df, header, keys):
    lat = np.array([])
    lon = np.array([])
    for key in keys:
        df = df[df[header] == key]
        lat = np.append(lat, df['Lat'].to_numpy())
        lon = np.append(lon, df['Long'].to_numpy())
    return lat, lon



def test(df):
    print(get_location(df, 'INCIDENT_NUMBER',['I182080058']))