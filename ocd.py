#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 13:32:22 2025

@author: jennaeverard
"""

import os
import requests
from config import WELL_LOG_URL, TIMEOUT, OUTPUT_LOGS

# Use the well log schema to get well info and well log files
def get_well_log(login, api, include_file_bytes=True):
    
    include = "true" if include_file_bytes else "false" # default to this
    url = f"{WELL_LOG_URL}/{api}/{include}" # build url

    r = requests.get(url, headers=login.headers(), timeout=TIMEOUT) # GET

    if r.status_code == 401: # invalid authentication
        login.refresh() # get refresh token
        r = requests.get(url, headers=login.headers(), timeout=TIMEOUT)

    r.raise_for_status() # checks for successful status
    return r.json()

# Use the schema response to download well log files (if available)
def save_well_log(login, response_data, well_api):
    
    # Get list of log files (or empty list if none)
    log_files = response_data.get("LogImagingFiles", [])
    
    # Make directory for saved files
    save_dir = OUTPUT_LOGS + str(well_api)
    os.makedirs(save_dir, exist_ok=True)
    
    # keep track of file count
    count = 0
    
    for log in log_files: # iterate through all files
    
        file_url = log.get("Url")
        file_name = log.get("FileName")
        
        print(f"Downloading {file_name}...")
        
        response = requests.get(file_url, headers=login.headers(), stream=True)
        response.raise_for_status() # checks for successful status
        
        filepath = os.path.join(save_dir, file_name)
        
        # write the file
        with open(filepath, "wb") as writeout:
            
            # save in chunks - don't kill your memory!
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    writeout.write(chunk)
                    
        count += 1
        
    return count # return the number of files saved