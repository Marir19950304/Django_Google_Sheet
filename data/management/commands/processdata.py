from django.core.management.base import BaseCommand, CommandError
from sodapy import Socrata
from dotenv import load_dotenv
from django.utils import timezone
from data.models import *
import json
from django.db.models import Count, Max
import pytz
import os
load_dotenv()

API_KEY = os.environ.get("API_KEY")
APP_TOKEN = os.environ.get("APP_TOKEN")
API_SECRET = os.environ.get("API_SECRET")

EST = pytz.timezone("US/Eastern")


def write_json(obj, fn):
    """
    docstring
    """
    with open(fn, 'wt') as outfile:
        outfile.write(json.dumps(obj, indent=2))


def retain_latest():
    """
    docstring
    """
    for p in Property.objects.values('parid').annotate(Max('extracrdt')):
        Property.objects.filter(parid=p['parid']).exclude(
            extracrdt=p['extracrdt__max']).delete()


def fetch_pvadtc():
    limit = 1000
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
                        zoning=t.get('zoning'),
                        housenum_lo=t['housenum_lo'],
                        housenum_hi=t['housenum_hi'],
                        street_name=t['street_name'],
                        zip_code=t['zip_code'],
                        corner=t.get('corner'),
                        extracrdt=t.get('extracrdt')
                    )

                offset += limit

        Complaint.objects.filter(
            pk__in=[c.id for c in complaints]).update(step=1)
        complaints = Complaint.objects.filter(step=0)[:50]


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # fetch_pvadtc()
        retain_latest()
