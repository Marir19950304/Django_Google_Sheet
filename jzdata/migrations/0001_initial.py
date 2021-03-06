# Generated by Django 3.2.9 on 2021-12-07 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_key', models.CharField(blank=True, max_length=100, null=True, verbose_name='Unique Key')),
                ('created_date', models.CharField(max_length=100, verbose_name='Created Date')),
                ('closed_date', models.CharField(max_length=100, verbose_name='Closed Date')),
                ('agency', models.CharField(blank=True, max_length=100, null=True, verbose_name='Agency')),
                ('agency_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Agency Name')),
                ('complaint_type', models.CharField(blank=True, max_length=100, null=True, verbose_name='Complaint Type')),
                ('descriptor', models.CharField(blank=True, max_length=100, null=True, verbose_name='Descriptor')),
                ('location_type', models.CharField(blank=True, max_length=100, null=True, verbose_name='Location Type')),
                ('incident_zip', models.CharField(blank=True, max_length=100, null=True, verbose_name='Incident Zip')),
                ('incident_address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Incident Address')),
                ('street_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Street Name')),
                ('cross_street_1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Cross Street 1')),
                ('cross_street_2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Cross Street 2')),
                ('intersection_street_1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Intersection Street 1')),
                ('intersection_street_2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Intersection Street 2')),
                ('address_type', models.CharField(blank=True, max_length=100, null=True, verbose_name='Address Type')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='City')),
                ('landmark', models.CharField(blank=True, max_length=100, null=True, verbose_name='Landmark')),
                ('facility_type', models.CharField(blank=True, max_length=100, null=True, verbose_name='Facility Type')),
                ('status', models.CharField(blank=True, max_length=100, null=True, verbose_name='Status')),
                ('due_date', models.CharField(blank=True, max_length=100, null=True, verbose_name='Due Date')),
                ('resolution_description', models.CharField(blank=True, max_length=100, null=True, verbose_name='Resolution Description')),
                ('resolution_action_updated_date', models.CharField(blank=True, max_length=100, null=True, verbose_name='Resolution Action Updated Date')),
                ('community_board1w', models.CharField(blank=True, max_length=100, null=True, verbose_name='Community Board')),
                ('bbl', models.CharField(blank=True, max_length=100, null=True, verbose_name='BBL')),
                ('borough', models.CharField(blank=True, max_length=100, null=True, verbose_name='Borough')),
                ('x_coordinate_state_plane', models.CharField(blank=True, max_length=100, null=True, verbose_name='X Coordinate (State Plane)')),
                ('y_coordinate_state_plane', models.CharField(blank=True, max_length=100, null=True, verbose_name='Y Coordinate (State Plane)')),
                ('open_data_channel_type', models.CharField(blank=True, max_length=100, null=True, verbose_name='Open Data Channel Type')),
                ('park_facility_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Park Facility Name')),
                ('park_borough', models.CharField(blank=True, max_length=100, null=True, verbose_name='Park Borough')),
                ('vehicle_type', models.CharField(blank=True, max_length=100, null=True, verbose_name='Vehicle Type')),
                ('taxi_company_borough', models.CharField(blank=True, max_length=100, null=True, verbose_name='Taxi Company Borough')),
                ('taxi_pick_up_location', models.CharField(blank=True, max_length=100, null=True, verbose_name='Taxi Pick Up Location')),
                ('bridge_highway_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Bridge Highway Name')),
                ('bridge_highway_direction', models.CharField(blank=True, max_length=100, null=True, verbose_name='Bridge Highway Direction')),
                ('road_ramp', models.CharField(blank=True, max_length=100, null=True, verbose_name='Road Ramp')),
                ('bridge_highway_segment', models.CharField(blank=True, max_length=100, null=True, verbose_name='Bridge Highway Segment')),
                ('latitude', models.CharField(blank=True, max_length=100, null=True, verbose_name='Latitude')),
                ('longitude', models.CharField(blank=True, max_length=100, null=True, verbose_name='Longitude')),
                ('location', models.CharField(blank=True, max_length=100, null=True, verbose_name='Location')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
            },
        ),
        migrations.CreateModel(
            name='Criteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Name')),
                ('text_value', models.TextField(blank=True, null=True, verbose_name='Text Value')),
                ('qtype', models.CharField(blank=True, choices=[('IS', 'IS'), ('IS NOT', 'IS NOT'), ('STARTS WITH', 'STARTS WITH'), ('CONTAINS', 'CONTAINS'), ('DOES NOT CONTAIN', 'DOES NOT CONTAIN'), ('IS BLANK', 'IS BLANK')], max_length=50, null=True, verbose_name='Query Type')),
                ('date_value', models.DateTimeField(blank=True, null=True, verbose_name='Date Value')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'criteria',
                'verbose_name_plural': 'criterias',
            },
        ),
    ]
