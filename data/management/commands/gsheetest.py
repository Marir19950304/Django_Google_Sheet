from django.db.models.expressions import F
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gspread
from django.core.management.base import BaseCommand, CommandError
from sodapy import Socrata
from dotenv import load_dotenv
from django.utils import timezone
from data.models import *
from data.tasks import *
import pandas as pd
import json
from django.db.models import Count, Max
import pytz
import os
import gspread
load_dotenv()


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--type', default = 'fetchfromdate', type = str)
        parser.add_argument('--back-days', default = -1, type = int)

    def handle(self, *args, **options):
        # define the scope
        options = list(args)[1]

        fetch_type = options['type']
        back_days = options['back_days']
        
        scope = ["https://www.googleapis.com/auth/drive", 
                "https://www.googleapis.com/auth/spreadsheets",
                "https://spreadsheets.google.com/feeds"]
        # add credentials to the account
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            'auth2.json', scope)
        # authorize the clientsheet
        client = gspread.authorize(creds)
        # get the instance of the Spreadsheet
        # open_sheet = client.open('Google_'+fetch_type)
        # sheet = client.create('data_5')
        # sheet.share('quickpaydeal@gmail.com', perm_type='user', role='writer')
        # open_sheet.share('yeykeliezz1991@gmail.com', perm_type='user', role='writer')
        # sheet.share('yeykeliezz1991@gmail.com', perm_type='user', role='writer')
        # sheet_instance = sheet.get_worksheet(0)
        # get the first sheet of the Spreadsheet
        
        fetch_data = []

        if (fetch_type == 'fetchdaily'):
            fetch_data = google_fetch(back_days,'')
            
            sheet = client.create('data_311')

        else:
            if (fetch_type == 'fetchresult_1'):
                open_sheet = client.open('data_1')
                sheet = client.create('filter_data_1')
            elif (fetch_type == 'fetchresult_2'):
                open_sheet = client.open('data_2')
                sheet = client.create('filter_data_2')
            elif (fetch_type == 'fetchresult_3'):
                open_sheet = client.open('data_3')
                sheet = client.create('filter_data_3')
            elif (fetch_type == 'fetchresult_4'):
                open_sheet = client.open('data_4')
                sheet = client.create('filter_data_4')
            elif (fetch_type == 'fetchresult_5'):
                open_sheet = client.open('data_5')
                sheet = client.create('filter_data_5')
        
            open_sheet.share('quickpaydeal@gmail.com', perm_type='user', role='writer')
            # open_sheet.share('yeykeliezz1991@gmail.com', perm_type='user', role='writer')
            open_sheet_instance = open_sheet.get_worksheet(0)
            records_data = open_sheet_instance.get_all_records()
            fetch_data = google_fetch(-10,records_data)

        sheet.share('quickpaydeal@gmail.com', perm_type='user', role='writer')
        # sheet.share('yeykeliezz1991@gmail.com', perm_type='user', role='writer')
        sheet_instance = sheet.get_worksheet(0)
        if (len(fetch_data) > 0):
            header = ['PARID', 'BORO', 'BLOCK', 'LOT', 'OWNER', 'HOUSENUM_LO', 'HOUSENUM_HI', 
                    'STREET_NAME','APTNO', 'CITY', 'STATE', 'ZIP_CODE', 'ZONING', 'BLD_STORY', 
                    'BLDG_CLASS', 'UNITS', 'LOT_FRT', 'LOT_DEP', 'BLD_FRT', 'BLD_DEP', 
                    'LAND_AREA', 'GROSS_SQFT', 'PYMKTTOT', 'CURMKTTOT', 'PARTY 2', 'ADDRESS 1',
                    'ADDRESS 2', 'CITY', 'STATE', 'ZIP', 'PARTY2.2', 'ADDRESS 1', 'ADDRESS 2',
                    'CITY', 'STATE', 'ZIP', 'Good Through Date','DEED', 'RECORDED/FILED', 
                    'DOC.AMOUNT', 'MTG', 'DOC.DATE', 'RECORDED/FILED','TLS', 'MCON', 'DESCRIPTOR',
                    'FIRST DATE', 'LAST DATE']
                    # 'SUM_BAL', 'DT_GRACE', 'SUM']
            sheet_instance.update('A1:AV1', [header])
            sheet_instance.update('A2:AV'+str(1+len(fetch_data)), fetch_data)