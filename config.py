#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 13:32:26 2025

@author: jennaeverard
"""

#### BASE ####
BASE_URL = "https://api.emnrd.nm.gov/wda"

#### AUTHORIZATION ENDPOINTS ####
LOGIN_URL = f"{BASE_URL}/v1/OCD/Authorization/Token/LoginCredentials"
REFRESH_URL = f"{BASE_URL}/v1/OCD/Authorization/Token/RefreshToken"

#### OCD ENDPOINTS ####
WELL_LOG_URL = f"{BASE_URL}/v1/OCD/Imaging/WellLog/File"

#### DEFAULT INPUT AND OUTPUT FILE PATHS ####
INPUT_PATH = "Inputs/"
OUTPUT_CSV = "Outputs - csv summaries/"
OUTPUT_LOGS = "Outputs - well log files/"

#### CREDENTIALS ####
USERNAME = #INPUT OCD USERNAME HERE#
PASSWORD = #INPUT OCD PASSWORD HERE#

TIMEOUT = 60
