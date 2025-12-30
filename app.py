#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 13:31:56 2025

@author: jennaeverard
"""

import pandas as pd
import numpy as np
from auth import AuthClient
from ocd import get_well_log, save_well_log
from config import INPUT_PATH, OUTPUT_CSV

def single_well_query(auth):
    
    # Take user input of API
    api = input("Enter the API number (i.e. 30-035-00008): ").strip()

    print(f"Fetching well info for {api}")
    
    data = get_well_log(auth, api, include_file_bytes=True)
    
    # Save the well data we care about
    well_type = data.get("WellType",{}).get("Description")
    well_status = data.get("WellStatus",{}).get("StatusDescription")
    
    well_id = data.get("WellIdn")
    well_api = data.get("WellApi") 
    property_id = data.get("PropertyIdn")
    property_name = data.get("PropertyName") 
    well_name = data.get("WellName")
    operator_name = data.get('OperatorName')
    
    latitude = data.get("Latitude")
    longitude = data.get("Longitude")
    county = data.get('CountyName')
    
    # Print well data for user
    print(f"""
          Well API: {well_api}
          Well ID: {well_id}
          Well Name: {well_name}
          Property ID: {property_id}
          Property Name: {property_name}
          Operator Name: {operator_name}
          
          Well Type: {well_type}
          Well Status: {well_status}
          
          County: {county}
          Latitude: {latitude}
          Longitude: {longitude}
          """)
    
    # Download well logs and exit!
    print("Downloading well logs...")
    file_num = save_well_log(auth, data, data.get("WellApi"))
    print(f"Saved {file_num} well logs")
    print("Exiting!")
    
def bulk_query(auth):
    
    # Arrays to keep track of all the well info we care about
    well_api = []
    well_id = []
    well_name = []
    property_id = []
    property_name = []
    operator_name = []
    
    well_type = []
    well_status = []
    
    county = []
    latitude = []
    longitude = []
    
    num_well_logs = []
    
    savename = input("Run name (for saving summary file): ").strip()
    filepath = input("Enter name of file containing well APIs: ")
    
    # Try (and try again) to open file containing well APIs
    valid_file = False
    while not valid_file:
        try:
            data = pd.read_csv(INPUT_PATH + filepath, header=None)
            valid_file = True
        except FileNotFoundError:
            print("***ERROR*** File Not Found")
            filepath = input("Enter path to file containing well APIs: ")
        except ValueError:
            print("***ERROR*** Nonnumerical data in file")
            filepath = input("Enter path to file containing well APIs: ")
        except Exception as e:
            print("***ERROR*** Unknown")
            filepath = input("Enter path to file containing well APIs: ")
     
    apis = np.array(data[0])
    
    # Get well info and log for each API
    for api in apis:
        
        print(f"Fetching well info for {api}")
        data = get_well_log(auth, api, include_file_bytes=True)
        
        well_api.append(data.get("WellApi"))
        well_id.append(data.get("WellIdn"))
        well_name.append(data.get("WellName"))
        property_id.append(data.get("PropertyIdn"))
        property_name.append(data.get("PropertyName") )
        operator_name.append(data.get('OperatorName'))
        
        well_type.append(data.get("WellType",{}).get("Description"))
        well_status.append(data.get("WellStatus",{}).get("StatusDescription"))
        
        county.append(data.get('CountyName'))
        latitude.append(data.get("Latitude"))
        longitude.append(data.get("Longitude"))
        
        file_num = save_well_log(auth, data, data.get("WellApi"))
        
        num_well_logs.append(file_num)
    
    # Save all well info to a csv in the output directory
    df = pd.DataFrame({'Well API': well_api,
                       'Well ID': well_id,
                       'Well Name': well_name,
                       'Property ID': property_id,
                       'Property Name': property_name,
                       'Operator Name': operator_name,
                       'Well Type': well_type,
                       'Well Status': well_status,
                       'County': county,
                       'Latitude': latitude,
                       'Longitude': longitude,
                       'Well Log #': num_well_logs})
    df.to_csv(OUTPUT_CSV + savename + '.csv', index=False)

def main():
    
    auth = AuthClient()
    print("Verifying user authentication...")
    auth.login()
    
    print("\n*** Welcome! ***\n")
    
    print("Please enter a single digit to select your desired program:")
    print("0 - query a single well by API")
    print("1 - bulk query many well APIs (see GitHub for input format)")
    selection = input("Enter Value: ")
    
    if int(selection) == 0:
        single_well_query(auth)
    elif int(selection) == 1:
        bulk_query(auth)
    else:
        print("!!! Invalid Input !!!")
        print("Exiting...")
    
if __name__ == "__main__":
    main()
