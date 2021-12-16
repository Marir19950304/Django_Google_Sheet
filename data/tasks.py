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
from django.db.models import Count, Max, Min, Q
import logging
from dotenv import load_dotenv
load_dotenv()

_logger = logging.getLogger(__name__)

API_KEY = os.environ.get("API_KEY")
APP_TOKEN = os.environ.get("APP_TOKEN")
API_SECRET = os.environ.get("API_SECRET")

EST = pytz.timezone("US/Eastern")


@shared_task
def fetch_doc_details():
    """
    docstring
    """
    # https://data.cityofnewyork.us/City-Government/ACRIS-Real-Property-Master/bnx9-e6tj/data
    dataset_code = 'bnx9-e6tj'
    with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
        q = Q(doc_type__isnull=True) | Q(doc_type__iexact='')
        docs = PropDocument.objects.filter(q)[:50]
        for d in docs:
            details = client.get(
                dataset_code, where="document_id='{}'".format(d.document_id))
            if not details or len(details) <= 0:
                continue

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
    props = Property.objects.filter(step=1)[:50]
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
    Property.objects.filter(id__in=[p.id for p in props]).update(step=2)


@shared_task
def fetch_details():
    limit = 500
    offset = 0
    dataset_code = '8y4t-faws'  # Property Value Assessment and Tax Class

    complaints = Complaint.objects.filter(step=0).exclude(
        bbl__exact='').exclude(bbl__isnull=True)[:100]
    if not complaints or len(complaints) <= 0:
        return

    ids = [c.id for c in complaints]
    parids = ','.join([f"'{c.bbl}'" for c in complaints])

    Property.objects.filter(complaint__id__in=ids).delete()
    with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
        taxes = client.get(
            dataset_code, where=f"parid in({parids})", limit=limit, offset=offset)
        while taxes and len(taxes) > 0:
            for t in taxes:
                try:
                    complaint = Complaint.objects.get(bbl=t['parid'])
                    Property.objects.create(
                        complaint=complaint,
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
                        street_name=t.get('street_name'),
                        zip_code=t.get('zip_code'),
                        corner=t.get('corner'),
                        extracrdt=t.get('extracrdt'),
                        step=0
                    )
                except Exception as e:
                    _logger.exception(e)

            offset += limit
            taxes = client.get(
                dataset_code, where=f"parid in({parids})", limit=limit, offset=offset)

    Complaint.objects.filter(id__in=ids).update(step=1)
    props = Property.objects.filter(complaint__id__in=ids).values(
        'parid').annotate(Max('extracrdt'), Min('id'))
    for p in props:
        Property.objects.filter(
            parid=p['parid']).exclude(extracrdt=p['extracrdt__max']).delete()
        Property.objects.filter(parid=p['parid']).update(step=1)

    # while complaints and len(complaints) > 0:
    #     for c in complaints:
    #         Property.objects.filter(
    #             parid__in=[c.bbl for c in complaints]).delete()

    #     ids = ','.join([f"'{c.bbl}'" for c in complaints])

    #     with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
    #         while True:
    #             taxes = client.get(
    #                 dataset_code, where=f"parid in({ids})", limit=limit, offset=offset)

    #             if not taxes or len(taxes) <= 0:
    #                 break

    #             for t in taxes:
    #                 Property.objects.create(
    #                     parid=t['parid'],
    #                     boro=t['boro'],
    #                     block=t['block'],
    #                     lot=t['lot'],
    #                     pymkttot=t.get('pymkttot'),
    #                     curmkttot=t.get('curmkttot'),
    #                     bldg_class=t.get('bldg_class'),
    #                     bld_story=t.get('bld_story'),
    #                     units=t.get('units'),
    #                     lot_frt=t.get('lot_frt'),
    #                     lot_dep=t.get('lot_dep'),
    #                     bld_frt=t.get('bld_frt'),
    #                     bld_dep=t.get('bld_dep'),
    #                     land_area=t.get('land_area'),
    #                     gross_sqft=t.get('gross_sqft'),
    #                     owner=t.get('owner'),
    #                     zoning=t.get('zoning'),
    #                     housenum_lo=t.get('housenum_lo'),
    #                     housenum_hi=t.get('housenum_hi'),
    #                     street_name=t['street_name'],
    #                     zip_code=t.get('zip_code'),
    #                     corner=t.get('corner'),
    #                     extracrdt=t.get('extracrdt')
    #                 )

    #             offset += limit

    #     Complaint.objects.filter(
    #         pk__in=[c.id for c in complaints]).update(step=1)
    #     complaints = Complaint.objects.filter(step=0)[:50]

    # for p in Property.objects.values('parid').annotate(Max('extracrdt'), Min('id')):
    #     Property.objects.filter(parid=p['parid']).exclude(
    #         extracrdt=p['extracrdt__max'], id=p['id__min']).delete()


@shared_task
def fetch_daily(back_days=1):
    limit = 512
    offset = 0

    # start_date = Criteria.objects.get(
    #     name='start_date').date_value.astimezone(EST).isoformat()[0:19]
    # end_date = Criteria.objects.get(
    #     name='end_date').date_value.astimezone(EST).isoformat()[0:19]
    dataset_code = 'erm2-nwe9'
    start_date = (timezone.now() - timedelta(days=back_days)).astimezone(
        EST).replace(hour=0, minute=0).isoformat()[0:19]
    end_date = timezone.now().astimezone(
        EST).replace(hour=23, minute=59).isoformat()[0:19]
    complaint_type = Criteria.objects.get(
        name='complaint_type').text_value
    descriptor = Criteria.objects.get(
        name='descriptor').text_value

    _logger.info("@fetch_daily() from {} to {}".format(start_date, end_date))

    with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
        complaints = client.get(
            dataset_code, where=f"created_date between '{start_date}' AND '{end_date}' AND complaint_type like '%{complaint_type}%' AND descriptor like '%{descriptor}%' AND bbl IS NOT NULL", limit=limit, offset=offset)
        while complaints and len(complaints) > 0:
            for complaint in sorted(complaints, key=lambda k: k['created_date']):
                obj, created = Complaint.objects.update_or_create(
                    bbl=complaint['bbl'],
                    defaults={
                        "unique_key": complaint['unique_key'],
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
            complaints = client.get(
                dataset_code, where=f"created_date between '{start_date}' AND '{end_date}' AND complaint_type like '%{complaint_type}%' AND descriptor like '%{descriptor}%' AND bbl IS NOT NULL", limit=limit, offset=offset)
