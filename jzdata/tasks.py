from __future__ import absolute_import
from socket import setdefaulttimeout, timeout
from threading import TIMEOUT_MAX
from celery import shared_task
from django.core import serializers
from django.db.models.aggregates import Sum
from django.utils import timezone
from django.utils.timezone import timedelta
from django.db.models import Count, Max, Min, Q
from django.db import connection
from django.utils import timezone
from datetime import date, datetime
from re import I
import os
from sodapy import Socrata
import logging
from dotenv import load_dotenv
from dateutil import parser
import pandas as pd
import pytz
import gspread
from urllib3 import Timeout

from jzdata.models import *

from oauth2client.service_account import ServiceAccountCredentials


load_dotenv()

_logger = logging.getLogger(__name__)

API_KEY = os.environ.get("API_KEY")
APP_TOKEN = os.environ.get("APP_TOKEN")
API_SECRET = os.environ.get("API_SECRET")

EST = pytz.timezone("US/Eastern")

def run_task(fetch_type, back_days):
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

@shared_task
def run_delayed_task(fetch_type, back_days):
    run_task(fetch_type, back_days)

def get_full_query(criteria):
    full_criteria = {}
    full_criteria['name'] = criteria.name

    if 'CONTAINS' in criteria.qtype:
        full_criteria['query'] = 'LIKE'
        full_criteria['text_value'] = '%'+criteria.text_value+'%'
    elif criteria.qtype == 'STARTS WITH':
        full_criteria['query'] = 'LIKE'
        full_criteria['text_value'] = '%'+criteria.text_value
    elif criteria.qtype == 'IS BLANK':
        full_criteria['query'] = 'IS'
        full_criteria['text_value'] = ''
    else:
        full_criteria['query'] = criteria.qtype
        full_criteria['text_value'] = criteria.text_value

    if 'NOT' in criteria.qtype:
        full_criteria['sign'] = 'NOT'
    else:
        full_criteria['sign'] = ''

    return full_criteria


def convert_date(my_date):
    return '' if my_date == '' or my_date == None else parser.parse(my_date).strftime('%d/%m/%Y')


def delete_all():
    Complaint.objects.all().delete()
    Property.objects.all().delete()
    PropDocument.objects.all().delete()
    Party.objects.all().delete()


def fetch_doc_details():
    """
    docstring
    """
    # https://data.cityofnewyork.us/City-Government/ACRIS-Real-Property-Master/bnx9-e6tj/data
    time = datetime.now()
    dataset_code = 'bnx9-e6tj'
    docs = PropDocument.objects.all()
    limit = 300
    offset = 0

    with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
        # q = Q(doc_type__isnull=True) | Q(doc_type__iexact='')
        client.timeout = 50
        doc_ids = ','.join(
            [f"'{doc.document_id}'" for doc in docs[offset:offset+limit]])
        try:
            details = client.get(
                dataset_code, where=f"document_id in({doc_ids})")
        except:
            details = []
        while len(details) > 0:
            print(offset)
            details_dict = {}
            for per_detail in details:
                details_dict[per_detail['document_id']] = per_detail

            for i in range(offset, min(docs.count(), offset+limit)):
                if docs[i].document_id in details_dict:
                    detail = details_dict[docs[i].document_id]

                    PropDocument.objects.filter(id=docs[i].id).update(
                        recorded_borough=detail['recorded_borough'],
                        doc_type=detail['doc_type'],
                        document_date=detail.get('document_date'),
                        document_amt=detail['document_amt'],
                        recorded_datetime=detail['recorded_datetime'],
                        percent_trans=detail['percent_trans'],
                        good_through_date=detail['good_through_date']
                    )

            offset += limit

            if offset >= docs.count():
                break

            doc_ids = ','.join(
                [f"'{doc.document_id}'" for doc in docs[offset:offset+limit]])
            details = client.get(
                dataset_code, where=f"document_id in({doc_ids})")

    print(datetime.now() - time)
    # PropDocument.objects.filter(
    #     id__in=[d.id for d in docs]).update(step=1)


def fetch_documents():
    """
    docstring
    """
    # property legals
    time = datetime.now()

    dataset_code = '8h5j-fqxa'
    props = Property.objects.all()

    limit = 100
    offset = 0

    with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
        client.timeout = 50
        while offset < props.count():
            print(offset)
            where_query = ""
            for i in range(offset, min(props.count(), offset+limit)):
                if where_query != "":
                    where_query += " OR "
                where_query += f"""(borough='{props[i].boro}' AND block='{props[i].block}' AND lot='{props[i].lot}')"""
            
            legal_limit = 1024
            legal_offset = 0

            legals = client.get(dataset_code, where=where_query, offset=legal_offset, limit=legal_limit)

            while len(legals) > 0:
                for legal in legals:
                    PropDocument.objects.create(
                        document_id=legal['document_id'],
                        borough=legal['borough'],
                        block=legal['block'],
                        lot=legal['lot']
                    )

                legal_offset += legal_limit
                legals = client.get(dataset_code, where=where_query, offset=legal_offset, limit=legal_limit)

            offset += limit

    print(datetime.now() - time)
    # Property.objects.filter(id__in=[p.id for p in props]).update(step=2)


def fetch_details():
    time = datetime.now()

    offset = 0
    limit = 512

    dataset_code = '8y4t-faws'  # Property Value Assessment and Tax Class

    complaints = Complaint.objects.all()
    if not complaints or len(complaints) <= 0:
        return

    property_dict = {}

    while offset < complaints.count():
        parids = ','.join(
            [f"'{c.bbl}'" for c in complaints[offset:offset+limit]])

        tax_offset = 0
        tax_limit = 1024

        with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
            taxes = client.get(
                dataset_code, where=f"parid in({parids})", select="""
                    parid, boro, block, lot, pymkttot, curmkttot, bldg_class, bld_story, units, 
                    lot_frt, lot_dep, bld_frt, bld_dep, land_area, gross_sqft, owner, zoning, 
                    housenum_lo, housenum_hi, street_name, zip_code, aptno, extracrdt
                """, offset=tax_offset, limit=tax_limit)

            while len(taxes) > 0:
                for t in taxes:
                    if t['parid'] in property_dict:
                        if t.get('extracrdt') > property_dict[t['parid']]['extracrdt']:
                            property_dict[t['parid']] = t
                    else:
                        property_dict[t['parid']] = t
                        property_dict[t['parid']]['extracrdt'] = t.get(
                            'extracrdt')

                tax_offset += tax_limit
                taxes = client.get(
                    dataset_code, where=f"parid in({parids})", select="""
                        parid, boro, block, lot, pymkttot, curmkttot, bldg_class, bld_story, units, 
                        lot_frt, lot_dep, bld_frt, bld_dep, land_area, gross_sqft, owner, zoning, 
                        housenum_lo, housenum_hi, street_name, zip_code, aptno, extracrdt
                    """, offset=tax_offset, limit=tax_limit)

        offset += limit

    for key, t in property_dict.items():
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
            street_name=t.get('street_name'),
            zip_code=t.get('zip_code'),
            aptno=t.get('aptno'),
            extracrdt=t.get('extracrdt'),
            step=0
        )

    print(datetime.now() - time)


def fetch_daily(back_days):
    time = datetime.now()

    limit = 150
    offset = 0

    dataset_code = 'erm2-nwe9'
    if back_days == -1:
        start_date = Criteria.objects.get(
            name='start_date').date_value.astimezone(EST).isoformat()[0:19]
        try:
            end_date = Criteria.objects.get(
                name='end_date').date_value.astimezone(EST).isoformat()[0:19]
        except:
            end_date = timezone.now().astimezone(EST).isoformat()[0:19]
        print(end_date)
    else:
        start_date = (timezone.now() - timedelta(days=back_days)).astimezone(
            EST).replace(hour=0, minute=0).isoformat()[0:19]
        end_date = timezone.now().astimezone(
            EST).replace(hour=23, minute=59).isoformat()[0:19]

    criterias = Criteria.objects.all()
    where_query = f"""created_date between '{start_date}' AND '{end_date}' 
            AND NOT bbl IS NULL
        """
    for criteria in criterias:
        if criteria.name in ['start_date', 'end_date']:
            continue

        query_object = get_full_query(criteria)
        print(query_object)
        where_query += f""" AND {query_object['sign']} {query_object['name']} 
             {query_object['query']} '{query_object['text_value']}'"""

    print(where_query)
    _logger.info("@fetch_daily() from {} to {}".format(start_date, end_date))

    with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
        client.timeout = 50
        complaints = client.get(
            dataset_code, where=where_query, select="""
                    bbl, unique_key, created_date, closed_date, agency, complaint_type, 
                    descriptor, status, incident_zip, incident_address, city
                """, limit=limit, offset=offset)
        complaint_dict = {}

        while complaints and len(complaints) > 0:
            print (offset)
            for complaint in complaints:
                if complaint['bbl'] in complaint_dict:
                    if complaint.get('created_date') > complaint_dict[complaint['bbl']]['created_date']:
                        complaint['oldest_created_date'] = complaint_dict[complaint['bbl']
                                                                          ]['oldest_created_date']
                        complaint_dict[complaint['bbl']] = complaint

                    if complaint.get('created_date') < complaint_dict[complaint['bbl']]['oldest_created_date']:
                        complaint_dict[complaint['bbl']
                                       ]['oldest_created_date'] = complaint['created_date']
                else:
                    complaint['oldest_created_date'] = complaint['created_date']
                    complaint_dict[complaint['bbl']] = complaint

            offset += limit
            complaints = client.get(
                dataset_code, where=where_query, limit=limit, offset=offset)

        for key, complaint in complaint_dict.items():
            obj, created = Complaint.objects.update_or_create(
                bbl=complaint['bbl'],
                defaults={
                    "unique_key": complaint.get('unique_key'),
                    "created_date": complaint.get('created_date'),
                    "oldest_created_date": complaint.get('oldest_created_date'),
                    "closed_date": complaint.get('closed_date'),
                    "agency": complaint.get('agency'),
                    "complaint_type": complaint.get('complaint_type'),
                    "descriptor": complaint.get('descriptor'),
                    "status": complaint.get('status'),
                    "incident_zip": complaint.get('incident_zip'),
                    "incident_address": complaint.get('incident_address'),
                    "city": complaint.get('city'),
                    "step": 0
                })
    print(datetime.now() - time)


def fetch_party():
    """
    docstring
    """
    # https://data.cityofnewyork.us/City-Government/ACRIS-Real-Property-Parties/636b-3b5g/data
    time = datetime.now()

    dataset_code = '636b-3b5g'
    docs = PropDocument.objects.all()
    limit = 400
    offset = 0

    with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
        # q = Q(doc_type__isnull=True) | Q(doc_type__iexact='')
        client.timeout = 50
        doc_ids = ','.join(
            [f"'{doc.document_id}'" for doc in docs[offset:offset+limit]])
        try:
            parties = client.get(
                dataset_code, where=f"document_id in({doc_ids})")
        except:
            parties = []
        while len(parties) > 0:
            print (offset)
            
            totparty = {}
            print(datetime.now() - time)

            for per_party in parties:
                if 'document_id' in per_party and 'party_type' in per_party and int(per_party['party_type']) == 2:
                    key = per_party['document_id']
                    if not key in totparty:
                        totparty[key] = []
                        totparty[key].append(per_party)
                    elif len(totparty[key]) == 1:
                        if totparty[key][0].get('good_through_date') < per_party.get('good_through_date'):
                            totparty[key] = [per_party, totparty[key][0]]
                        else:
                            totparty[key] = [totparty[key][0], per_party]
                    else:
                        if totparty[key][0].get('good_through_date') < per_party.get('good_through_date'):
                            totparty[key] = [per_party, totparty[key][0]]
                        elif totparty[key][1].get('good_through_date') < per_party.get('good_through_date'):
                            totparty[key] = [totparty[key][0], per_party]

            for i in range(offset, min(docs.count(), offset+limit)):
                key_name = docs[i].document_id
                if key_name in totparty:
                    index = 1
                    for party in totparty[key_name]:
                        Party.objects.update_or_create(
                            document_id=party['document_id'],
                            party_type=party['party_type']+str(index),
                            defaults={
                                'record_type': party.get('record_type', ''),
                                'name': party.get('name', ''),
                                'address_1': party.get('address_1', ''),
                                'address_2': party.get('address_2', ''),
                                'country': party.get('country', ''),
                                'city': party.get('city', ''),
                                'state': party.get('state', ''),
                                'zip': party.get('zip', ''),
                                'good_through_date': party.get('good_through_date', '')
                            }
                        )
                        index += 1

            offset += limit

            if offset >= docs.count():
                break

            doc_ids = ','.join(
                [f"'{doc.document_id}'" for doc in docs[offset:offset+limit]])
            parties = client.get(
                dataset_code, where=f"document_id in({doc_ids})")

    print(datetime.now() - time)


def fetch_from_excel(data):
    time = datetime.now()
    
    # current_path = os.getcwd()
    col_names = ['BBL', 'BORO', 'BLOCK', 'LOT']
    db_col_names = {
        'BBL': 'parid',
        'BORO': 'boro',
        'BLOCK': 'block',
        'LOT': 'lot',
        'DESCRIPTOR': 'descriptor'
    }

    descriptors = {}

    # data = pd.read_excel(current_path+'/'+'google_sheet.xlsx')
    excel_sheet = []

    for item in data:
        new_row = {}
        for col_name in col_names:
            col_value = item[col_name]
            if str(col_value) != 'nan' and str(col_value) != '':
                new_row[col_name] = str(col_value)
        
        if item['BBL'] != '':
            descriptors[str(item['BBL'])] = item['DESCRIPTOR']

        if item['BORO'] != '':
            descriptors[str(item['BORO'])+','+str(item['BLOCK'])+','+str(item['LOT'])] = item['DESCRIPTOR']
        
        excel_sheet.append(new_row)

    dataset_code = 'erm2-nwe9'

    limit = 200
    offset = 0
    complaint_dict = {}
    complaint_bbls = set()

    with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
        while offset < len(excel_sheet):
            print(offset)
            where_query = ""
            for i in range(offset, min(len(excel_sheet), offset+limit)):
                if where_query != "":
                    where_query += " OR "

                clause = "("
                for key, value in excel_sheet[i].items():
                    if str(value) != 'nan' and str(value) != '':
                        if clause != "(":
                            clause += " AND "
                        clause += f"{db_col_names[key]}='{value}'"
                clause += ")"

                where_query += clause
            
            complaints = client.get('8y4t-faws', where=where_query)

            for complaint in complaints:
                complaint_bbls.add(complaint['parid'])

                if descriptors.get(complaint['parid'], '') == '':
                    descriptors[complaint['parid']] = descriptors[complaint['boro']+','+complaint['block']+','+complaint['lot']]
            
            offset += limit

    complaint_bbls = list(complaint_bbls)
    offset = 0
    limit = 100

    while offset < len(complaint_bbls):
        where_query = ""
        for i in range(offset, min(len(complaint_bbls), offset+limit)):
            if where_query != "":
                where_query += " OR "

            clause = f"(bbl='{complaint_bbls[i]}' AND descriptor like '%{descriptors[complaint_bbls[i]]}%')"
            where_query += clause

        complaints = client.get(dataset_code, where=where_query)

        for complaint in complaints:
            if complaint['bbl'] in complaint_dict:
                if complaint.get('created_date') > complaint_dict[complaint['bbl']]['created_date']:
                    complaint['oldest_created_date'] = complaint_dict[complaint['bbl']
                                                                    ]['oldest_created_date']
                    complaint_dict[complaint['bbl']] = complaint

                if complaint.get('created_date') < complaint_dict[complaint['bbl']]['oldest_created_date']:
                    complaint_dict[complaint['bbl']
                                ]['oldest_created_date'] = complaint['created_date']
            else:
                complaint['oldest_created_date'] = complaint['created_date']
                complaint_dict[complaint['bbl']] = complaint


        offset += limit

    for key, complaint in complaint_dict.items():
        obj, created = Complaint.objects.update_or_create(
            bbl=complaint['bbl'],
            defaults={
                "unique_key": complaint.get('unique_key'),
                "created_date": complaint.get('created_date'),
                "oldest_created_date": complaint.get('oldest_created_date'),
                "closed_date": complaint.get('closed_date'),
                "agency": complaint.get('agency'),
                "complaint_type": complaint.get('complaint_type'),
                "descriptor": complaint.get('descriptor'),
                "status": complaint.get('status'),
                "incident_zip": complaint.get('incident_zip'),
                "incident_address": complaint.get('incident_address'),
                "city": complaint.get('city'),
                "step": 0
            })

    print(datetime.now() - time)


def google_fetch(back_days,data):
    # return datetime.timestamp(datetime.strptime('2020 Jun 15 12:00:00 AM', '%Y %b %d %I:%M:%S %p'))
    delete_all()
    if back_days == -10:
        print ('fetch_excel')
        print(data,len(data))
        fetch_from_excel(data)
    else:
        print ('fetch_daily')
        fetch_daily(back_days)
    print ('fetch_details')
    fetch_details()
    print('fetch_documents')
    fetch_documents()
    print ('fetch_doc_details')
    fetch_doc_details()
    print ('fetch_party')
    fetch_party()

    with connection.cursor() as cursor:
        results = cursor.execute(f"""
                SELECT jzdata_complaint.id, bbl, jzdata_property.boro, jzdata_property.block, jzdata_property.lot, 
                    jzdata_property.owner, jzdata_property.housenum_lo, jzdata_property.housenum_hi, jzdata_property.street_name,
                    jzdata_property.aptno, jzdata_complaint.city, 'NY', jzdata_complaint.incident_zip, jzdata_property.zoning, 
                    jzdata_property.bld_story, jzdata_property.bldg_class, jzdata_property.units, jzdata_property.lot_frt,
                    jzdata_property.lot_dep, jzdata_property.bld_frt, jzdata_property.bld_dep, jzdata_property.land_area,
                    jzdata_property.gross_sqft, jzdata_property.pymkttot, jzdata_property.curmkttot
                FROM jzdata_complaint
                INNER JOIN jzdata_property ON jzdata_complaint.bbl=jzdata_property.parid 
                INNER JOIN jzdata_propdocument 
                    ON jzdata_property.boro=jzdata_propdocument.borough 
                        AND jzdata_property.block=jzdata_propdocument.block
                        AND jzdata_property.lot=jzdata_propdocument.lot
                WHERE 
                    NOT jzdata_property.boro IS NULL
                    AND NOT jzdata_property.block IS NULL
                    AND NOT jzdata_property.lot IS NULL
                GROUP BY bbl, jzdata_property.boro, jzdata_property.block, jzdata_property.lot
            """).fetchall()

    result_dict = {}
    for result in results:
        result = list(result)[1:]
        key = result[0]+','+result[1]+','+result[2]+','+result[3]
        result_dict[key] = list(result)
        for i in range(0, 12):
            result_dict[key].append('')
    with connection.cursor() as cursor:
        parties = cursor.execute(f"""
                SELECT jzdata_complaint.id, bbl, jzdata_property.boro, jzdata_property.block, jzdata_property.lot, 
                    jzdata_propdocument.document_id, jzdata_party.party_type, jzdata_party.name, 
                    jzdata_party.address_1, jzdata_party.address_2, jzdata_party.city, 
                    jzdata_party.state, jzdata_party.zip
                FROM jzdata_complaint
                INNER JOIN jzdata_property ON jzdata_complaint.bbl=jzdata_property.parid
                INNER JOIN jzdata_propdocument
                    ON jzdata_property.boro=jzdata_propdocument.borough 
                        AND jzdata_property.block=jzdata_propdocument.block
                        AND jzdata_property.lot=jzdata_propdocument.lot
                INNER JOIN jzdata_party ON jzdata_propdocument.document_id=jzdata_party.document_id
                WHERE (jzdata_propdocument.doc_type LIKE '%DEED%' OR
                        jzdata_propdocument.doc_type LIKE '%RPTT%')
                    AND NOT jzdata_property.boro IS NULL
                    AND NOT jzdata_property.block IS NULL
                    AND NOT jzdata_property.lot IS NULL
                ORDER BY jzdata_propdocument.document_date DESC
            """).fetchall()

    party_dict = {}
    for party in parties:
        party = list(party)[1:]
        key = party[0]+','+party[1]+','+party[2]+','+party[3]

        if not key in party_dict:
            party_dict[key] = [party]
        elif party_dict[key][0][4] == party[4]:
            party_dict[key].append(party)
    for key, parties in party_dict.items():
        for party in parties:
            offset = (int(party[5][1:])-1) * 6

            for i in range(0, 6):
                result_dict[key][24+i+offset] = party[6+i]
    for key, value in result_dict.items():
        result_dict[key] += google_property_master(
            value[1], value[2], value[3])
        result_dict[key] += list()
    with connection.cursor() as cursor:
        results = cursor.execute(f"""
                SELECT jzdata_complaint.id, bbl, jzdata_property.boro, jzdata_property.block, jzdata_property.lot, 
                    jzdata_complaint.descriptor, jzdata_complaint.oldest_created_date, jzdata_complaint.created_date
                FROM jzdata_complaint
                INNER JOIN jzdata_property ON jzdata_complaint.bbl=jzdata_property.parid 
                INNER JOIN jzdata_propdocument 
                    ON jzdata_property.boro=jzdata_propdocument.borough 
                        AND jzdata_property.block=jzdata_propdocument.block
                        AND jzdata_property.lot=jzdata_propdocument.lot
                WHERE (jzdata_propdocument.doc_type LIKE '%DEED%' OR
                        jzdata_propdocument.doc_type LIKE '%RPTT%')
                    AND NOT jzdata_property.boro IS NULL
                    AND NOT jzdata_property.block IS NULL
                    AND NOT jzdata_property.lot IS NULL
                GROUP BY bbl, jzdata_property.boro, jzdata_property.block, jzdata_property.lot
            """).fetchall()

    for result in results:
        result = result[1:]
        key = result[0]+','+result[1]+','+result[2]+','+result[3]
        if key in result_dict:
            result_dict[key] += [result[4],result[5],result[6]]

    with connection.cursor() as cursor:
        results = cursor.execute(f"""
                SELECT jzdata_complaint.id, bbl, jzdata_property.boro, jzdata_property.block, jzdata_property.lot, 
                    jzdata_complaint.descriptor, jzdata_complaint.oldest_created_date, jzdata_complaint.created_date
                FROM jzdata_complaint
                INNER JOIN jzdata_property ON jzdata_complaint.bbl=jzdata_property.parid 
                INNER JOIN jzdata_propdocument 
                    ON jzdata_property.boro=jzdata_propdocument.borough 
                        AND jzdata_property.block=jzdata_propdocument.block
                        AND jzdata_property.lot=jzdata_propdocument.lot
                WHERE NOT jzdata_property.boro IS NULL
                    AND NOT jzdata_property.block IS NULL
                    AND NOT jzdata_property.lot IS NULL
                GROUP BY bbl, jzdata_property.boro, jzdata_property.block, jzdata_property.lot
            """).fetchall()

    for result in results:
        result = result[1:]
        key = result[0]+','+result[1]+','+result[2]+','+result[3]
        if key in result_dict and len(result_dict[key]) != 48:
            result_dict[key] += [result[4],result[5],result[6]]

    return list(result_dict.values())

    # return list(map(list, result_dict.values()))[0]


def google_property_master(boro, block, lot):
    prop_documents = PropDocument.objects.filter(
        borough=boro, block=block, lot=lot)
    deed_docs = prop_documents.filter(Q(doc_type__contains='DEED') | Q(doc_type__contains='RPTT')).order_by(
        '-document_date', '-recorded_datetime')

    ret_arr = []
    flag = 0
    # max_deed_date = deed_docs.aggregate(Max('document_date'))['document_date__max']
    if deed_docs.count() == 0:
        max_deed_date = (datetime.now() - timedelta(weeks=1000)).astimezone(
            EST).replace(hour=0, minute=0).isoformat()[0:19]
        recorded_field = ''
        good_through_date = ''
        deed_amount = 0
        flag = 1
    elif deed_docs[0].document_date in ('', None):
        max_deed_date = (datetime.now() - timedelta(weeks=1000)).astimezone(
            EST).replace(hour=0, minute=0).isoformat()[0:19]
        recorded_field = deed_docs[0].recorded_datetime
        good_through_date = deed_docs[0].good_through_date
        deed_amount = deed_docs[0].document_amt
        flag = 1
    else:
        max_deed_date = deed_docs[0].document_date
        recorded_field = deed_docs[0].recorded_datetime
        good_through_date = deed_docs[0].good_through_date
        deed_amount = deed_docs[0].document_amt

    mtge_docs = prop_documents.filter(Q(doc_type__contains='MTGE') &
                                      (Q(document_date__gte=max_deed_date) | Q(recorded_datetime__gte=max_deed_date))).order_by('-document_amt')

    if mtge_docs.count() == 0:
        mtge_amount = ''
        mtge_doc_date = ''
        mtge_recorded_field = ''
    else:
        mtge_amount = mtge_docs[0].document_amt
        mtge_recorded_field = mtge_docs[0].recorded_datetime
        mtge_doc_date = mtge_docs[0].document_date

    tls_docs = prop_documents.filter(
        doc_type__contains='TLS', document_date__gte=max_deed_date)
    tls_count = tls_docs.count()

    mcon_docs = prop_documents.filter(
        doc_type__contains='MCON', document_date__gte=max_deed_date)
    if mcon_docs.count() == 0:
        mcon_date = ''
    else:
        mcon_date = mcon_docs[0].document_date

    if flag == 1:
        max_deed_date = ''

    ret_arr.append(convert_date(good_through_date))
    ret_arr.append(convert_date(max_deed_date))
    ret_arr.append(convert_date(recorded_field))
    ret_arr.append(str(deed_amount))
    ret_arr.append(str(mtge_amount))
    ret_arr.append(convert_date(mtge_doc_date))
    ret_arr.append(convert_date(mtge_recorded_field))
    ret_arr.append(tls_count)
    ret_arr.append(mcon_date)
    return ret_arr


def fetch_result(parid):
    dataset_code = 'scjx-j6np'

    total_bal = 0
    dt_grace = []
    with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
        # total_result = client.get(
        #     dataset_code, select="sum(sum_bal) as total_bal, min(due_date) as oldest_dt", where="sum_bal > 300")
        data = client.get(dataset_code, where="parid='{parid}'")
    for i in range(0, len(data)-1):
        if float(data[i]['sum_bal']) > 300:
            total_bal = total_bal + float(data[i]['sum_bal'])
            dt_grace.append(data[i]['dt_grace'])
    dt_grace.sort()
    for i in range(0, len(data)-1):
        if data[i]['dt_grace'] == dt_grace[0]:
            sum = data[i]['sum_bal']

    return [total_bal, dt_grace[0], sum]
    # return charge_balance
