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
    step = models.IntegerField(_("Step"), default=0)

    class Meta:
        verbose_name = _("complaint")
        verbose_name_plural = _("complaints")

    def __str__(self):
        return self.unique_key

    def get_absolute_url(self):
        return reverse("complaint_detail", kwargs={"pk": self.pk})


class Property(models.Model):
    parid = models.CharField(_('PARID'), max_length=250)
    boro = models.IntegerField(_('BORO'), default=0)
    block = models.IntegerField(_('BLOCK'), default=0)
    lot = models.IntegerField(_('LOT'), default=0)

    easement = models.CharField(
        _('EASEMENT'), max_length=250, null=True, blank=True)

    subident_reuc = models.CharField(
        _('SUBIDENT-REUC'), max_length=250, null=True, blank=True)
    rectype = models.IntegerField(_('RECTYPE'), default=0)

    year = models.CharField(_('YEAR'), max_length=250, null=True, blank=True)
    ident = models.CharField(_('IDENT'), max_length=250, null=True, blank=True)
    subident = models.CharField(
        _('SUBIDENT'), max_length=250, null=True, blank=True)
    roll_section = models.CharField(
        _('ROLL_SECTION'), max_length=250, null=True, blank=True)

    secvol = models.IntegerField(_('SECVOL'), default=0)
    pymktland = models.IntegerField(_('PYMKTLAND'), default=0)
    pymkttot = models.IntegerField(_('PYMKTTOT'), default=0)
    pyactland = models.IntegerField(_('PYACTLAND'), default=0)
    pyacttot = models.IntegerField(_('PYACTTOT'), default=0)
    pyactextot = models.IntegerField(_('PYACTEXTOT'), default=0)
    pytrnland = models.IntegerField(_('PYTRNLAND'), default=0)
    pytrntot = models.IntegerField(_('PYTRNTOT'), default=0)
    pytrnextot = models.IntegerField(_('PYTRNEXTOT'), default=0)
    pytxbtot = models.IntegerField(_('PYTXBTOT'), default=0)
    pytxbextot = models.IntegerField(_('PYTXBEXTOT'), default=0)

    pytaxclass = models.CharField(
        _('PYTAXCLASS'), max_length=250, null=True, blank=True)

    tenmktland = models.IntegerField(_('TENMKTLAND'), default=0)
    tenmkttot = models.IntegerField(_('TENMKTTOT'), default=0)
    tenactland = models.IntegerField(_('TENACTLAND'), default=0)
    tenacttot = models.IntegerField(_('TENACTTOT'), default=0)
    tenactextot = models.IntegerField(_('TENACTEXTOT'), default=0)
    tentrnland = models.IntegerField(_('TENTRNLAND'), default=0)
    tentrntot = models.IntegerField(_('TENTRNTOT'), default=0)
    tentrnextot = models.IntegerField(_('TENTRNEXTOT'), default=0)
    tentxbtot = models.IntegerField(_('TENTXBTOT'), default=0)
    tentxbextot = models.IntegerField(_('TENTXBEXTOT'), default=0)

    tentaxclass = models.CharField(
        _('TENTAXCLASS'), max_length=250, null=True, blank=True)

    cbnmktland = models.IntegerField(_('CBNMKTLAND'), default=0)
    cbnmkttot = models.IntegerField(_('CBNMKTTOT'), default=0)
    cbnactland = models.IntegerField(_('CBNACTLAND'), default=0)
    cbnacttot = models.IntegerField(_('CBNACTTOT'), default=0)
    cbnactextot = models.IntegerField(_('CBNACTEXTOT'), default=0)
    cbntrnland = models.IntegerField(_('CBNTRNLAND'), default=0)
    cbntrntot = models.IntegerField(_('CBNTRNTOT'), default=0)
    cbntrnextot = models.IntegerField(_('CBNTRNEXTOT'), default=0)
    cbntxbtot = models.IntegerField(_('CBNTXBTOT'), default=0)
    cbntxbextot = models.IntegerField(_('CBNTXBEXTOT'), default=0)
    cbntaxclass = models.CharField(
        _('CBNTAXCLASS'), max_length=250, null=True, blank=True)
    finmktland = models.IntegerField(_('FINMKTLAND'), default=0)
    finmkttot = models.IntegerField(_('FINMKTTOT'), default=0)
    finactland = models.IntegerField(_('FINACTLAND'), default=0)
    finacttot = models.IntegerField(_('FINACTTOT'), default=0)
    finactextot = models.IntegerField(_('FINACTEXTOT'), default=0)
    fintrnland = models.IntegerField(_('FINTRNLAND'), default=0)
    fintrntot = models.IntegerField(_('FINTRNTOT'), default=0)
    fintrnextot = models.IntegerField(_('FINTRNEXTOT'), default=0)
    fintxbtot = models.IntegerField(_('FINTXBTOT'), default=0)
    fintxbextot = models.IntegerField(_('FINTXBEXTOT'), default=0)
    fintaxclass = models.CharField(
        _('FINTAXCLASS'), max_length=250, null=True, blank=True)
    curmktland = models.IntegerField(_('CURMKTLAND'), default=0)
    curmkttot = models.IntegerField(_('CURMKTTOT'), default=0)
    curactland = models.IntegerField(_('CURACTLAND'), default=0)
    curacttot = models.IntegerField(_('CURACTTOT'), default=0)
    curactextot = models.IntegerField(_('CURACTEXTOT'), default=0)
    curtrnland = models.IntegerField(_('CURTRNLAND'), default=0)
    curtrntot = models.IntegerField(_('CURTRNTOT'), default=0)
    curtrnextot = models.IntegerField(_('CURTRNEXTOT'), default=0)
    curtxbtot = models.IntegerField(_('CURTXBTOT'), default=0)
    curtxbextot = models.IntegerField(_('CURTXBEXTOT'), default=0)
    curtaxclass = models.CharField(
        _('CURTAXCLASS'), max_length=250, null=True, blank=True)
    period = models.IntegerField(_('PERIOD'), default=0)
    newdrop = models.IntegerField(_('NEWDROP'), default=0)

    noav = models.CharField(
        _('NOAV'), max_length=250, null=True, blank=True)
    valref = models.CharField(
        _('VALREF'), max_length=250, null=True, blank=True)
    bldg_class = models.CharField(
        _('BLDG_CLASS'), max_length=250, null=True, blank=True)
    owner = models.CharField(
        _('OWNER'), max_length=250, null=True, blank=True)
    zoning = models.CharField(
        _('ZONING'), max_length=250, null=True, blank=True)
    housenum_lo = models.CharField(
        _('HOUSENUM_LO'), max_length=250, null=True, blank=True)
    housenum_hi = models.CharField(
        _('HOUSENUM_HI'), max_length=250, null=True, blank=True)
    street_name = models.CharField(
        _('STREET_NAME'), max_length=250, null=True, blank=True)
    zip_code = models.CharField(
        _('ZIP_CODE'), max_length=250, null=True, blank=True)
    gepsupport_rc = models.CharField(
        _('GEPSUPPORT_RC'), max_length=250, null=True, blank=True)

    stcode = models.IntegerField(_('STCODE'), default=0)
    lot_frt = models.IntegerField(_('LOT_FRT'), default=0)
    lot_dep = models.IntegerField(_('LOT_DEP'), default=0)

    lot_irreg = models.CharField(
        _('LOT_IRREG'), max_length=250, null=True, blank=True)

    bld_frt = models.IntegerField(_('BLD_FRT'), default=0)
    bld_dep = models.IntegerField(_('BLD_DEP'), default=0)

    bld_ext = models.CharField(
        _('BLD_EXT'), max_length=250, null=True, blank=True)

    bld_story = models.IntegerField(_('BLD_STORY'), default=0)

    corner = models.CharField(
        _('CORNER'), max_length=250, null=True, blank=True)

    land_area = models.IntegerField(_('LAND_AREA'), default=0)
    num_bldgs = models.IntegerField(_('NUM_BLDGS'), default=0)
    yrbuilt = models.IntegerField(_('YRBUILT'), default=0)
    yrbuilt_range = models.IntegerField(_('YRBUILT_RANGE'), default=0)

    yrbuilt_flag = models.CharField(
        _('YRBUILT_FLAG'), max_length=250, null=True, blank=True)

    yralt1 = models.IntegerField(_('YRALT1'), default=0)
    yralt1_range = models.IntegerField(_('YRALT1_RANGE'), default=0)
    yralt2 = models.IntegerField(_('YRALT2'), default=0)
    yralt2_range = models.IntegerField(_('YRALT2_RANGE'), default=0)
    coop_apts = models.IntegerField(_('COOP_APTS'), default=0)
    units = models.IntegerField(_('UNITS'), default=0)

    reuc_ref = models.CharField(
        _('REUC_REF'), max_length=250, null=True, blank=True)
    aptno = models.CharField(_('APTNO'), max_length=250, null=True, blank=True)

    coop_num = models.IntegerField(_('COOP_NUM'), default=0)
    cpb_boro = models.IntegerField(_('CPB_BORO'), default=0)
    cpb_dist = models.IntegerField(_('CPB_DIST'), default=0)

    appt_date = models.CharField(
        _('APPT_DATE'), max_length=50, null=True, blank=True)

    appt_boro = models.IntegerField(_('APPT_BORO'), default=0)
    appt_block = models.IntegerField(_('APPT_BLOCK'), default=0)
    appt_lot = models.IntegerField(_('APPT_LOT'), default=0)

    appt_ease = models.CharField(
        _('APPT_EASE'), max_length=250, null=True, blank=True)

    condo_number = models.IntegerField(_('CONDO_Number'), default=0)

    condo_sfx1 = models.CharField(
        _('CONDO_SFX1'), max_length=250, null=True, blank=True)

    condo_sfx2 = models.IntegerField(_('CONDO_SFX2'), default=0)
    condo_sfx3 = models.CharField(
        _('CONDO_SFX3'), max_length=250, null=True, blank=True)

    uaf_land = models.IntegerField(_('UAF_LAND'), default=0)
    uaf_bldg = models.IntegerField(_('UAF_BLDG'), default=0)

    protest_1 = models.CharField(
        _('PROTEST_1'), max_length=250, null=True, blank=True)
    protest_2 = models.CharField(
        _('PROTEST_2'), max_length=250, null=True, blank=True)
    protest_old = models.CharField(
        _('PROTEST_OLD'), max_length=250, null=True, blank=True)

    attorney_group1 = models.IntegerField(_('ATTORNEY_GROUP1'), default=0)
    attorney_group2 = models.CharField(
        _('ATTORNEY_GROUP2'), max_length=250, null=True, blank=True)
    attorney_group_old = models.IntegerField(
        _('ATTORNEY_GROUP_OLD'), default=0)
    gross_sqft = models.IntegerField(_('GROSS_SQFT'), default=0)
    hotel_area_gross = models.IntegerField(_('HOTEL_AREA_GROSS'), default=0)
    office_area_gross = models.IntegerField(_('OFFICE_AREA_GROSS'), default=0)
    residential_area_gross = models.IntegerField(
        _('RESIDENTIAL_AREA_GROSS'), default=0)
    retail_area_gross = models.IntegerField(_('RETAIL_AREA_GROSS'), default=0)
    loft_area_gross = models.IntegerField(_('LOFT_AREA_GROSS'), default=0)
    factory_area_gross = models.IntegerField(
        _('FACTORY_AREA_GROSS'), default=0)
    warehouse_area_gross = models.IntegerField(
        _('WAREHOUSE_AREA_GROSS'), default=0)
    storage_area_gross = models.IntegerField(
        _('STORAGE_AREA_GROSS'), default=0)
    garage_area = models.IntegerField(_('GARAGE_AREA'), default=0)
    other_area_gross = models.IntegerField(_('OTHER_AREA_GROSS'), default=0)
    reuc_description = models.TextField(
        _('REUC_DESCRIPTION'), null=True, blank=True)

    extracrdt = models.CharField(
        _('EXTRACRDT'), max_length=50, null=True, blank=True)
    pytaxflag = models.CharField(
        _('PYTAXFLAG'), max_length=150, null=True, blank=True)
    tentaxflag = models.CharField(
        _('TENTAXFLAG'), max_length=250, null=True, blank=True)
    cbntaxflag = models.CharField(
        _('CBNTAXFLAG'), max_length=250, null=True, blank=True)
    fintaxflag = models.CharField(
        _('FINTAXFLAG'), max_length=250, null=True, blank=True)
    curtaxflag = models.CharField(
        _('CURTAXFLAG'), max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = _("property")
        verbose_name_plural = _("properties")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("property_detail", kwargs={"pk": self.pk})
