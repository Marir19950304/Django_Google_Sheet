from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gspread
from django.core.management.base import BaseCommand, CommandError
from sodapy import Socrata
from dotenv import load_dotenv
from django.utils import timezone
from data.models import *
from data.tasks import *
import json
from django.db.models import Count, Max
import pytz
import os
load_dotenv()


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # define the scope
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        # add credentials to the account
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            'socrata-project-335309-3b827526f39f.json', scope)

        # authorize the clientsheet
        client = gspread.authorize(creds)

        # get the instance of the Spreadsheet
        sheet = client.open('JZ Prop')

        # get the first sheet of the Spreadsheet
        sheet_instance = sheet.get_worksheet(0)
        sheet_instance.insert_row(["hi"])
        import pdb; pdb.set_trace()
