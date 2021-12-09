from re import I
from celery import Celery, shared_task
from celery.schedules import crontab
import pytz
from django.utils import timezone
from django.utils.timezone import timedelta
from data.models import *
import os
from sodapy import Socrata
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get("API_KEY")
APP_TOKEN = os.environ.get("APP_TOKEN")
API_SECRET = os.environ.get("API_SECRET")

EST = pytz.timezone("US/Eastern")


@shared_task
def fetch_daily():
    limit = 400
    offset = 0

    # start_date = Criteria.objects.get(
    #     name='start_date').date_value.astimezone(EST).isoformat()[0:19]
    # end_date = Criteria.objects.get(
    #     name='end_date').date_value.astimezone(EST).isoformat()[0:19]
    start_date = (timezone.now() - timedelta(days=1)).astimezone(
        EST).replace(hour=0, minute=0).isoformat()[0:19]
    end_date = timezone.now().astimezone(
        EST).replace(hour=23, minute=59).isoformat()[0:19]
    print("From {} to {}".format(start_date, end_date))
    complaint_type = Criteria.objects.get(
        name='complaint_type').text_value
    descriptor = Criteria.objects.get(
        name='descriptor').text_value

    with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
        while True:
            complaints = client.get(
                "erm2-nwe9", where=f"created_date between '{start_date}' AND '{end_date}' AND complaint_type like '%{complaint_type}%' AND descriptor like '%{descriptor}%' AND bbl IS NOT NULL", limit=limit, offset=offset)
            if not complaints or len(complaints) <= 0:
                print("No items found!")
                break

            for complaint in complaints:
                obj, created = Complaint.objects.update_or_create(
                    unique_key=complaint['unique_key'], defaults={
                        "created_date": complaint['created_date'],
                        "closed_date": complaint.get('closed_date'),
                        "agency": complaint['agency'],
                        "complaint_type": complaint['complaint_type'],
                        "descriptor": complaint['descriptor'],
                        "status": complaint['status'],
                        "incident_zip": complaint['incident_zip'],
                        "incident_address": complaint['incident_address'],
                        "city": complaint['city'],
                        "bbl": complaint['bbl'],
                        "step": 0
                    })

            offset += limit
