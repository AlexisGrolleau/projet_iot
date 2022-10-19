import os
import pandas as pd
import base64
from os import listdir
from os.path import isfile, join
import time
import requests

pd.options.mode.chained_assignment = None


def read_csv(filename: str) -> pd.DataFrame:
    """Reads a CSV file into a pandas DataFrame."""
    return pd.read_csv(filename)


def get_csv_files(path: str) -> list:
    """Returns a list of CSV files in a given path."""
    return [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.csv')]


def decode_AG(b):
    return base64.b64decode(b).hex()


if __name__ == '__main__':
    # Add end_device_id and function to apply to the payload
    dict_id = {"303636326B39820B": "decode_AG"}

    # Get the path to the current directory
    raw_directory = "/home/lora/projet_2022_2023/trameLoRaNonTraitee/"
    list_files = get_csv_files(raw_directory)
    print(list_files)
    for file in list_files:
        df_raw = read_csv(raw_directory + file)

        # Extract the data from the DataFrame
        for k, v in dict_id.items():
            df = df_raw.loc[df_raw["end_device_id (OUT)"] == k]
            try:
                df['payload (OUT)'] = df['payload (OUT)'].apply(eval(v))
                time = str(int(time.time()) * 100000000)
                for index, row in df.iterrows():
                    rssi = str(row['rssi (OUT)'])
                    snr = str(row['snr (OUT)'])
                    payload_Total = str(k) + ",host=admin Temps=" + time + ",Temperature=26,rssi_dbm="+ rssi + ",SNR_Db=" + snr
                    print(payload_Total)
                    r_Total = requests.post(url="http://localhost:8086/write?db=TrameLoRa", data=payload_Total)
            except NameError as e:
                print("Function name Error:", e)
