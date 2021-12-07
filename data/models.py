from enum import unique
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Criteria(models.Model):
    QUERIES = (
        ('IS', 'IS'),
        ('IS NOT', 'IS NOT'),
        ('STARTS WITH', 'STARTS WITH'),
        ('CONTAINS', 'CONTAINS'),
        ('DOES NOT CONTAIN', 'DOES NOT CONTAIN'),
        ('IS BLANK', 'IS BLANK'),
    )

    name = models.CharField(_("Name"), max_length=250,
                            null=True, blank=True, unique=True)
    text_value = models.TextField(_("Text Value"), null=True, blank=True)
    qtype = models.CharField(
        _("Query Type"), max_length=50, choices=QUERIES, null=True, blank=True)
    date_value = models.DateTimeField(
        _("Date Value"), auto_now=False, null=True, blank=True, auto_now_add=False)

    class Meta:
        verbose_name = _("criteria")
        verbose_name_plural = _("criterias")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("criteria_detail", kwargs={"pk": self.pk})


# Create your models here.
class Complaint(models.Model):
    timestamp = models.DateTimeField(
        _("Timestamp"), auto_now=False, auto_now_add=True)
    unique_key = models.CharField(
        _('Unique Key'), max_length=100, null=True, blank=True, unique=True)
    created_date = models.CharField(
        _('Created Date'), max_length=100)
    closed_date = models.CharField(
        _('Closed Date'), max_length=100)
    agency = models.CharField(
        _('Agency'), max_length=100, null=True, blank=True)
    agency_name = models.CharField(
        _('Agency Name'), max_length=100, null=True, blank=True)
    complaint_type = models.CharField(
        _('Complaint Type'), max_length=100, null=True, blank=True)
    descriptor = models.CharField(
        _('Descriptor'), max_length=100, null=True, blank=True)
    location_type = models.CharField(
        _('Location Type'), max_length=100, null=True, blank=True)
    incident_zip = models.CharField(
        _('Incident Zip'), max_length=100, null=True, blank=True)
    incident_address = models.CharField(
        _('Incident Address'), max_length=100, null=True, blank=True)
    street_name = models.CharField(
        _('Street Name'), max_length=100, null=True, blank=True)
    cross_street_1 = models.CharField(
        _('Cross Street 1'), max_length=100, null=True, blank=True)
    cross_street_2 = models.CharField(
        _('Cross Street 2'), max_length=100, null=True, blank=True)
    intersection_street_1 = models.CharField(
        _('Intersection Street 1'), max_length=100, null=True, blank=True)
    intersection_street_2 = models.CharField(
        _('Intersection Street 2'), max_length=100, null=True, blank=True)
    address_type = models.CharField(
        _('Address Type'), max_length=100, null=True, blank=True)
    city = models.CharField(_('City'), max_length=100, null=True, blank=True)
    landmark = models.CharField(
        _('Landmark'), max_length=100, null=True, blank=True)
    facility_type = models.CharField(
        _('Facility Type'), max_length=100, null=True, blank=True)
    status = models.CharField(
        _('Status'), max_length=100, null=True, blank=True)
    due_date = models.CharField(
        _('Due Date'), max_length=100, null=True, blank=True)
    resolution_description = models.CharField(
        _('Resolution Description'), max_length=100, null=True, blank=True)
    resolution_action_updated_date = models.CharField(
        _('Resolution Action Updated Date'), max_length=100, null=True, blank=True)
    community_board1w = models.CharField(
        _('Community Board'), max_length=100, null=True, blank=True)
    bbl = models.CharField(_('BBL'), max_length=100, null=True, blank=True)
    borough = models.CharField(
        _('Borough'), max_length=100, null=True, blank=True)
    x_coordinate_state_plane = models.CharField(
        _('X Coordinate (State Plane)'), max_length=100, null=True, blank=True)
    y_coordinate_state_plane = models.CharField(
        _('Y Coordinate (State Plane)'), max_length=100, null=True, blank=True)
    open_data_channel_type = models.CharField(
        _('Open Data Channel Type'), max_length=100, null=True, blank=True)
    park_facility_name = models.CharField(
        _('Park Facility Name'), max_length=100, null=True, blank=True)
    park_borough = models.CharField(
        _('Park Borough'), max_length=100, null=True, blank=True)
    vehicle_type = models.CharField(
        _('Vehicle Type'), max_length=100, null=True, blank=True)
    taxi_company_borough = models.CharField(
        _('Taxi Company Borough'), max_length=100, null=True, blank=True)
    taxi_pick_up_location = models.CharField(
        _('Taxi Pick Up Location'), max_length=100, null=True, blank=True)
    bridge_highway_name = models.CharField(
        _('Bridge Highway Name'), max_length=100, null=True, blank=True)
    bridge_highway_direction = models.CharField(
        _('Bridge Highway Direction'), max_length=100, null=True, blank=True)
    road_ramp = models.CharField(
        _('Road Ramp'), max_length=100, null=True, blank=True)
    bridge_highway_segment = models.CharField(
        _('Bridge Highway Segment'), max_length=100, null=True, blank=True)
    latitude = models.CharField(
        _('Latitude'), max_length=100, null=True, blank=True)
    longitude = models.CharField(
        _('Longitude'), max_length=100, null=True, blank=True)
    location = models.CharField(
        _('Location'), max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.pk})
