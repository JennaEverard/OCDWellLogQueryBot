#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 13:32:15 2025

@author: jennaeverard
"""

import requests
from config import LOGIN_URL, REFRESH_URL, USERNAME, PASSWORD, TIMEOUT

class AuthClient:
    
    # keep track of access and refresh token
    def __init__(self):
        self.access_token = None
        self.refresh_token = None

    # login and get tokens
    # first time logging in
    def login(self):
        
        # store username and password in secure file!!
        r = requests.post(
            LOGIN_URL,
            json={"UserName": USERNAME, "Password": PASSWORD},
            timeout=TIMEOUT
        )
        r.raise_for_status() # check for success
        data = r.json()
        
        # retrieve access and refresh token
        self.access_token = data["AccessToken"]
        self.refresh_token = data["RefreshToken"]

    # login and get tokens
    # renewig access token after first time
    def refresh(self):
        
        r = requests.post(
            REFRESH_URL,
            json={
                "UserName": USERNAME,
                "RefreshToken": self.refresh_token
            },
            timeout=TIMEOUT
        )
        r.raise_for_status() # check for success
        data = r.json()
        
        self.access_token = data["AccessToken"]
        self.refresh_token = data["RefreshToken"]

    # get headers to send with url request
    # won't work otherwise!!
    def headers(self):
        if not self.access_token:
            self.login()
        return {"Authorization": f"Bearer {self.access_token}"}
