import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime, date
from pprint import pprint as pp
SHEET_NAME = "Kanticha Mansion"

def get_client(sheet_name=SHEET_NAME):
    # use creds to create a client to interact with the Google Drive API
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"
             ]
    
    creds = ServiceAccountCredentials.from_json_keyfile_name("GOOGLE_CRED.json",scope)
    client = gspread.authorize(creds)
    # Find a workbook by name and open the first sheet
    client = client.open(sheet_name).sheet1
    data = client.get_all_records() 
    pp(data)
    return client



if __name__ == "__main__":
    get_client()