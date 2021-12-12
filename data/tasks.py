import json
from re import I
from celery import Celery, shared_task
from celery.schedules import crontab
import pytz
from django.utils import timezone
from django.utils.timezone import timedelta
from data.models import *
import os
from sodapy import Socrata
from django.db.models import Count, Max, Min
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get("API_KEY")
APP_TOKEN = os.environ.get("APP_TOKEN")
API_SECRET = os.environ.get("API_SECRET")

EST = pytz.timezone("US/Eastern")


@shared_task
def fetch_doc_details():
    """
    docstring
    """
    dataset_code = 'bnx9-e6tj'
    with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
        docs = PropDocument.objects.filter(step=0)[:50]
        for d in docs:
            details = client.get(
                dataset_code, where="document_id='{}'".format(d.document_id))
            if details and len(details) > 0:
                detail = details[0]
                PropDocument.objects.filter(id=d.id).update(
                    recorded_borough=detail['recorded_borough'],
                    doc_type=detail['doc_type'],
                    document_date=detail['document_date'],
                    document_amt=detail['document_amt'],
                    recorded_datetime=detail['recorded_datetime'],
                    percent_trans=detail['percent_trans'],
                    good_through_date=detail['good_through_date']
                )

        PropDocument.objects.filter(
            id__in=[d.id for d in docs]).update(step=1)


@shared_task
def fetch_documents():
    """
    docstring
    """
    # property legals
    dataset_code = '8h5j-fqxa'
    for p in Property.objects.values('parid').annotate(Max('extracrdt'), Min('id')):
        Property.objects.filter(parid=p['parid']).exclude(
            extracrdt=p['extracrdt__max'], id=p['id__min']).delete()

    props = Property.objects.filter(step=0)[:50]
    with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
        for prop in props:
            while True:
                legals = client.get(
                    dataset_code, where="borough='{}' AND block='{}' AND lot='{}'".format(prop.boro, prop.block, prop.lot))
                if not legals or len(legals) <= 0:
                    break

                for legal in legals:
                    PropDocument.objects.update_or_create(
                        document_id=legal['document_id'],
                        defaults={
                            "borough": legal['borough'],
                            "block": legal['block'],
                            "lot": legal['lot']
                        }
                    )
    Property.objects.filter(id__in=[p.id for p in props]).update(step=1)


@shared_task
def fetch_pvadtc():
    limit = 1000
    offset = 0
    dataset_code = '8y4t-faws'
    complaints = Complaint.objects.filter(step=0, bbl__ne='')[:50]
    while complaints and len(complaints) > 0:
        for c in complaints:
            Property.objects.filter(
                parid__in=[c.bbl for c in complaints]).delete()

        processed_ids = set()
        ids = ','.join(
            [f"'{c.bbl}'" for c in complaints if c.bbl and c.bbl != ''])

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
                        pymkttot=t.get('pymkttot'),
                        curmkttot=t.get('curmkttot'),
                        bldg_class=t.get('bldg_class'),
                        bld_story=t.get('bld_story'),
                        units=t.get('units'),
                        lot_frt=t.get('lot_frt'),
                        lot_dep=t.get('lot_dep'),
                        bld_frt=t.get('bld_frt'),
                        bld_dep=t.get('bld_dep'),
                        land_area=t.get('land_area'),
                        gross_sqft=t.get('gross_sqft'),
                        owner=t.get('owner'),
                        zoning=t.get('zoning'),
                        housenum_lo=t.get('housenum_lo'),
                        housenum_hi=t.get('housenum_hi'),
                        street_name=t['street_name'],
                        zip_code=t.get('zip_code'),
                        corner=t.get('corner'),
                        extracrdt=t.get('extracrdt')
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
                        "bbl": complaint.get('bbl', ''),
                        "step": 0
                    })

            offset += limit
