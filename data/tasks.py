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
def fetch_related():

    limit = 512
    offset = 0
    dataset_code = '8y4t-faws'

    complaints = Complaint.objects.filter(step=0)[:50]
    while complaints and len(complaints) > 0:
        for c in complaints:
            Property.objects.filter(
                parid__in=[c.bbl for c in complaints]).delete()

        processed_ids = set()
        ids = ','.join([f"'{c.bbl}'" for c in complaints])

        with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
            while True:
                taxes = client.get(
                    dataset_code, where=f"parid in({ids})", limit=limit, offset=offset)

                if not taxes or len(taxes) <= 0:
                    break

                for t in taxes:
                    Property.objects.create(
                        parid=t['parid'],
                        boro=t['boro'],
                        block=t['block'],
                        lot=t['lot'],
                        pymkttot=t['pymkttot'],
                        curmkttot=t['curmkttot'],
                        bldg_class=t['bldg_class'],
                        bld_story=t['bld_story'],
                        units=t['units'],
                        lot_frt=t['lot_frt'],
                        lot_dep=t['lot_dep'],
                        bld_frt=t['bld_frt'],
                        bld_dep=t['bld_dep'],
                        land_area=t['land_area'],
                        gross_sqft=t['gross_sqft'],
                        owner=t['owner'],
                        zoning=t['zoning'],
                        housenum_lo=t['housenum_lo'],
                        housenum_hi=t['housenum_hi'],
                        street_name=t['street_name'],
                        zip_code=t['zip_code'],
                        corner=t['corner']
                    )

                offset += limit

        Complaint.objects.filter(
            pk__in=[c.id for c in complaints]).update(step=1)
        complaints = Complaint.objects.filter(step=0)[:50]


@shared_task
def fetch_daily():
    limit = 512
    offset = 0

    # start_date = Criteria.objects.get(
    #     name='start_date').date_value.astimezone(EST).isoformat()[0:19]
    # end_date = Criteria.objects.get(
    #     name='end_date').date_value.astimezone(EST).isoformat()[0:19]
    dataset_code = 'erm2-nwe9'
    start_date = (timezone.now() - timedelta(days=1)).astimezone(
        EST).replace(hour=0, minute=0).isoformat()[0:19]
    end_date = timezone.now().astimezone(
        EST).replace(hour=23, minute=59).isoformat()[0:19]
    complaint_type = Criteria.objects.get(
        name='complaint_type').text_value
    descriptor = Criteria.objects.get(
        name='descriptor').text_value

    with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
        while True:
            complaints = client.get(
                dataset_code, where=f"created_date between '{start_date}' AND '{end_date}' AND complaint_type like '%{complaint_type}%' AND descriptor like '%{descriptor}%' AND bbl IS NOT NULL", limit=limit, offset=offset)
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
