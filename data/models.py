from enum import unique
from django.db import models
from django.db.models.fields import CharField
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
    timestamp_created = models.DateTimeField(
        _("Timestamp"), auto_now_add=True)
    timestamp_modified = models.DateTimeField(
        _("Timestamp"), auto_now=True)

    unique_key = models.CharField(
        _('Unique Key'), max_length=100, null=True, blank=True, unique=True)
    created_date = models.CharField(
        _('Created Date'), max_length=100)
    closed_date = models.CharField(
        _('Closed Date'), max_length=100, null=True, blank=True)
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
    timestamp_created = models.DateTimeField(
        _("Timestamp"), auto_now_add=True)
    timestamp_modified = models.DateTimeField(
        _("Timestamp"), auto_now=True)

    parid = models.CharField(_('PARID'), max_length=64)
    boro = models.CharField(_('BORO'), max_length=64, null=True, blank=True)
    block = models.CharField(_('BLOCK'), max_length=64, null=True, blank=True)
    lot = models.CharField(_('LOT'), max_length=64, null=True, blank=True)

    easement = models.CharField(
        _('EASEMENT'), max_length=64, null=True, blank=True)

    subident_reuc = models.CharField(
        _('SUBIDENT-REUC'), max_length=64, null=True, blank=True)
    rectype = models.CharField(
        _('RECTYPE'), max_length=64, null=True, blank=True)

    year = models.CharField(_('YEAR'), max_length=64, null=True, blank=True)
    ident = models.CharField(_('IDENT'), max_length=64, null=True, blank=True)
    subident = models.CharField(
        _('SUBIDENT'), max_length=64, null=True, blank=True)
    roll_section = models.CharField(
        _('ROLL_SECTION'), max_length=64, null=True, blank=True)

    secvol = models.CharField(
        _('SECVOL'), max_length=64, null=True, blank=True)
    pymktland = models.CharField(
        _('PYMKTLAND'), max_length=64, null=True, blank=True)
    pymkttot = models.CharField(
        _('PYMKTTOT'), max_length=64, null=True, blank=True)
    pyactland = models.CharField(
        _('PYACTLAND'), max_length=64, null=True, blank=True)
    pyacttot = models.CharField(
        _('PYACTTOT'), max_length=64, null=True, blank=True)
    pyactextot = models.CharField(
        _('PYACTEXTOT'), max_length=64, null=True, blank=True)
    pytrnland = models.CharField(
        _('PYTRNLAND'), max_length=64, null=True, blank=True)
    pytrntot = models.CharField(
        _('PYTRNTOT'), max_length=64, null=True, blank=True)
    pytrnextot = models.CharField(
        _('PYTRNEXTOT'), max_length=64, null=True, blank=True)
    pytxbtot = models.CharField(
        _('PYTXBTOT'), max_length=64, null=True, blank=True)
    pytxbextot = models.CharField(
        _('PYTXBEXTOT'), max_length=64, null=True, blank=True)

    pytaxclass = models.CharField(
        _('PYTAXCLASS'), max_length=64, null=True, blank=True)

    tenmktland = models.CharField(
        _('TENMKTLAND'), max_length=64, null=True, blank=True)
    tenmkttot = models.CharField(
        _('TENMKTTOT'), max_length=64, null=True, blank=True)
    tenactland = models.CharField(
        _('TENACTLAND'), max_length=64, null=True, blank=True)
    tenacttot = models.CharField(
        _('TENACTTOT'), max_length=64, null=True, blank=True)
    tenactextot = models.CharField(
        _('TENACTEXTOT'), max_length=64, null=True, blank=True)
    tentrnland = models.CharField(
        _('TENTRNLAND'), max_length=64, null=True, blank=True)
    tentrntot = models.CharField(
        _('TENTRNTOT'), max_length=64, null=True, blank=True)
    tentrnextot = models.CharField(
        _('TENTRNEXTOT'), max_length=64, null=True, blank=True)
    tentxbtot = models.CharField(
        _('TENTXBTOT'), max_length=64, null=True, blank=True)
    tentxbextot = models.CharField(
        _('TENTXBEXTOT'), max_length=64, null=True, blank=True)

    tentaxclass = models.CharField(
        _('TENTAXCLASS'), max_length=64, null=True, blank=True)

    cbnmktland = models.CharField(
        _('CBNMKTLAND'), max_length=64, null=True, blank=True)
    cbnmkttot = models.CharField(
        _('CBNMKTTOT'), max_length=64, null=True, blank=True)
    cbnactland = models.CharField(
        _('CBNACTLAND'), max_length=64, null=True, blank=True)
    cbnacttot = models.CharField(
        _('CBNACTTOT'), max_length=64, null=True, blank=True)
    cbnactextot = models.CharField(
        _('CBNACTEXTOT'), max_length=64, null=True, blank=True)
    cbntrnland = models.CharField(
        _('CBNTRNLAND'), max_length=64, null=True, blank=True)
    cbntrntot = models.CharField(
        _('CBNTRNTOT'), max_length=64, null=True, blank=True)
    cbntrnextot = models.CharField(
        _('CBNTRNEXTOT'), max_length=64, null=True, blank=True)
    cbntxbtot = models.CharField(
        _('CBNTXBTOT'), max_length=64, null=True, blank=True)
    cbntxbextot = models.CharField(
        _('CBNTXBEXTOT'), max_length=64, null=True, blank=True)
    cbntaxclass = models.CharField(
        _('CBNTAXCLASS'), max_length=64, null=True, blank=True)
    finmktland = models.CharField(
        _('FINMKTLAND'), max_length=64, null=True, blank=True)
    finmkttot = models.CharField(
        _('FINMKTTOT'), max_length=64, null=True, blank=True)
    finactland = models.CharField(
        _('FINACTLAND'), max_length=64, null=True, blank=True)
    finacttot = models.CharField(
        _('FINACTTOT'), max_length=64, null=True, blank=True)
    finactextot = models.CharField(
        _('FINACTEXTOT'), max_length=64, null=True, blank=True)
    fintrnland = models.CharField(
        _('FINTRNLAND'), max_length=64, null=True, blank=True)
    fintrntot = models.CharField(
        _('FINTRNTOT'), max_length=64, null=True, blank=True)
    fintrnextot = models.CharField(
        _('FINTRNEXTOT'), max_length=64, null=True, blank=True)
    fintxbtot = models.CharField(
        _('FINTXBTOT'), max_length=64, null=True, blank=True)
    fintxbextot = models.CharField(
        _('FINTXBEXTOT'), max_length=64, null=True, blank=True)
    fintaxclass = models.CharField(
        _('FINTAXCLASS'), max_length=64, null=True, blank=True)
    curmktland = models.CharField(
        _('CURMKTLAND'), max_length=64, null=True, blank=True)
    curmkttot = models.CharField(
        _('CURMKTTOT'), max_length=64, null=True, blank=True)
    curactland = models.CharField(
        _('CURACTLAND'), max_length=64, null=True, blank=True)
    curacttot = models.CharField(
        _('CURACTTOT'), max_length=64, null=True, blank=True)
    curactextot = models.CharField(
        _('CURACTEXTOT'), max_length=64, null=True, blank=True)
    curtrnland = models.CharField(
        _('CURTRNLAND'), max_length=64, null=True, blank=True)
    curtrntot = models.CharField(
        _('CURTRNTOT'), max_length=64, null=True, blank=True)
    curtrnextot = models.CharField(
        _('CURTRNEXTOT'), max_length=64, null=True, blank=True)
    curtxbtot = models.CharField(
        _('CURTXBTOT'), max_length=64, null=True, blank=True)
    curtxbextot = models.CharField(
        _('CURTXBEXTOT'), max_length=64, null=True, blank=True)
    curtaxclass = models.CharField(
        _('CURTAXCLASS'), max_length=64, null=True, blank=True)
    period = models.CharField(
        _('PERIOD'), max_length=64, null=True, blank=True)
    newdrop = models.CharField(
        _('NEWDROP'), max_length=64, null=True, blank=True)

    noav = models.CharField(
        _('NOAV'), max_length=64, null=True, blank=True)
    valref = models.CharField(
        _('VALREF'), max_length=64, null=True, blank=True)
    bldg_class = models.CharField(
        _('BLDG_CLASS'), max_length=64, null=True, blank=True)
    owner = models.CharField(
        _('OWNER'), max_length=64, null=True, blank=True)
    zoning = models.CharField(
        _('ZONING'), max_length=64, null=True, blank=True)
    housenum_lo = models.CharField(
        _('HOUSENUM_LO'), max_length=64, null=True, blank=True)
    housenum_hi = models.CharField(
        _('HOUSENUM_HI'), max_length=64, null=True, blank=True)
    street_name = models.CharField(
        _('STREET_NAME'), max_length=64, null=True, blank=True)
    zip_code = models.CharField(
        _('ZIP_CODE'), max_length=64, null=True, blank=True)
    gepsupport_rc = models.CharField(
        _('GEPSUPPORT_RC'), max_length=64, null=True, blank=True)

    stcode = models.CharField(
        _('STCODE'), max_length=64, null=True, blank=True)
    lot_frt = models.CharField(
        _('LOT_FRT'), max_length=64, null=True, blank=True)
    lot_dep = models.CharField(
        _('LOT_DEP'), max_length=64, null=True, blank=True)

    lot_irreg = models.CharField(
        _('LOT_IRREG'), max_length=64, null=True, blank=True)

    bld_frt = models.CharField(
        _('BLD_FRT'), max_length=64, null=True, blank=True)
    bld_dep = models.CharField(
        _('BLD_DEP'), max_length=64, null=True, blank=True)

    bld_ext = models.CharField(
        _('BLD_EXT'), max_length=64, null=True, blank=True)

    bld_story = models.CharField(
        _('BLD_STORY'), max_length=64, null=True, blank=True)

    corner = models.CharField(
        _('CORNER'), max_length=64, null=True, blank=True)

    land_area = models.CharField(
        _('LAND_AREA'), max_length=64, null=True, blank=True)
    num_bldgs = models.CharField(
        _('NUM_BLDGS'), max_length=64, null=True, blank=True)
    yrbuilt = models.CharField(
        _('YRBUILT'), max_length=64, null=True, blank=True)
    yrbuilt_range = models.CharField(
        _('YRBUILT_RANGE'), max_length=64, null=True, blank=True)

    yrbuilt_flag = models.CharField(
        _('YRBUILT_FLAG'), max_length=64, null=True, blank=True)

    yralt1 = models.CharField(
        _('YRALT1'), max_length=64, null=True, blank=True)
    yralt1_range = models.CharField(
        _('YRALT1_RANGE'), max_length=64, null=True, blank=True)
    yralt2 = models.CharField(
        _('YRALT2'), max_length=64, null=True, blank=True)
    yralt2_range = models.CharField(
        _('YRALT2_RANGE'), max_length=64, null=True, blank=True)
    coop_apts = models.CharField(
        _('COOP_APTS'), max_length=64, null=True, blank=True)
    units = models.CharField(_('UNITS'), max_length=64, null=True, blank=True)

    reuc_ref = models.CharField(
        _('REUC_REF'), max_length=64, null=True, blank=True)
    aptno = models.CharField(_('APTNO'), max_length=64, null=True, blank=True)

    coop_num = models.CharField(
        _('COOP_NUM'), max_length=64, null=True, blank=True)
    cpb_boro = models.CharField(
        _('CPB_BORO'), max_length=64, null=True, blank=True)
    cpb_dist = models.CharField(
        _('CPB_DIST'), max_length=64, null=True, blank=True)

    appt_date = models.CharField(
        _('APPT_DATE'), max_length=50, null=True, blank=True)

    appt_boro = models.CharField(
        _('APPT_BORO'), max_length=64, null=True, blank=True)
    appt_block = models.CharField(
        _('APPT_BLOCK'), max_length=64, null=True, blank=True)
    appt_lot = models.CharField(
        _('APPT_LOT'), max_length=64, null=True, blank=True)

    appt_ease = models.CharField(
        _('APPT_EASE'), max_length=64, null=True, blank=True)

    condo_number = models.CharField(
        _('CONDO_Number'), max_length=64, null=True, blank=True)

    condo_sfx1 = models.CharField(
        _('CONDO_SFX1'), max_length=64, null=True, blank=True)

    condo_sfx2 = models.CharField(
        _('CONDO_SFX2'), max_length=64, null=True, blank=True)
    condo_sfx3 = models.CharField(
        _('CONDO_SFX3'), max_length=64, null=True, blank=True)

    uaf_land = models.CharField(
        _('UAF_LAND'), max_length=64, null=True, blank=True)
    uaf_bldg = models.CharField(
        _('UAF_BLDG'), max_length=64, null=True, blank=True)

    protest_1 = models.CharField(
        _('PROTEST_1'), max_length=64, null=True, blank=True)
    protest_2 = models.CharField(
        _('PROTEST_2'), max_length=64, null=True, blank=True)
    protest_old = models.CharField(
        _('PROTEST_OLD'), max_length=64, null=True, blank=True)

    attorney_group1 = models.CharField(
        _('ATTORNEY_GROUP1'), max_length=64, null=True, blank=True)
    attorney_group2 = models.CharField(
        _('ATTORNEY_GROUP2'), max_length=64, null=True, blank=True)
    attorney_group_old = models.CharField(
        _('ATTORNEY_GROUP_OLD'), max_length=64, null=True, blank=True)
    gross_sqft = models.CharField(
        _('GROSS_SQFT'), max_length=64, null=True, blank=True)
    hotel_area_gross = models.CharField(
        _('HOTEL_AREA_GROSS'), max_length=64, null=True, blank=True)
    office_area_gross = models.CharField(
        _('OFFICE_AREA_GROSS'), max_length=64, null=True, blank=True)
    residential_area_gross = models.CharField(
        _('RESIDENTIAL_AREA_GROSS'), max_length=64, null=True, blank=True)
    retail_area_gross = models.CharField(
        _('RETAIL_AREA_GROSS'), max_length=64, null=True, blank=True)
    loft_area_gross = models.CharField(
        _('LOFT_AREA_GROSS'), max_length=64, null=True, blank=True)
    factory_area_gross = models.CharField(
        _('FACTORY_AREA_GROSS'), max_length=64, null=True, blank=True)
    warehouse_area_gross = models.CharField(
        _('WAREHOUSE_AREA_GROSS'), max_length=64, null=True, blank=True)
    storage_area_gross = models.CharField(
        _('STORAGE_AREA_GROSS'), max_length=64, null=True, blank=True)
    garage_area = models.CharField(
        _('GARAGE_AREA'), max_length=64, null=True, blank=True)
    other_area_gross = models.CharField(
        _('OTHER_AREA_GROSS'), max_length=64, null=True, blank=True)
    reuc_description = models.TextField(
        _('REUC_DESCRIPTION'), null=True, blank=True)
    extracrdt = models.CharField(
        _('EXTRACRDT'), max_length=64, null=True, blank=True)
    pytaxflag = models.CharField(
        _('PYTAXFLAG'), max_length=64, null=True, blank=True)
    tentaxflag = models.CharField(
        _('TENTAXFLAG'), max_length=64, null=True, blank=True)
    cbntaxflag = models.CharField(
        _('CBNTAXFLAG'), max_length=64, null=True, blank=True)
    fintaxflag = models.CharField(
        _('FINTAXFLAG'), max_length=64, null=True, blank=True)
    curtaxflag = models.CharField(
        _('CURTAXFLAG'), max_length=64, null=True, blank=True)
    step = models.IntegerField(_("Step"), default=0)

    class Meta:
        verbose_name = _("property assessment")
        verbose_name_plural = _("property assessments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("property_detail", kwargs={"pk": self.pk})


class PropDocument(models.Model):
    timestamp_created = models.DateTimeField(
        _("Timestamp"), auto_now_add=True)
    timestamp_modified = models.DateTimeField(
        _("Timestamp"), auto_now=True)

    document_id = CharField("Document Id", max_length=64)
    borough = models.CharField(_('BORO'), max_length=64, null=True, blank=True)
    block = models.CharField(_('BLOCK'), max_length=64, null=True, blank=True)
    lot = models.CharField(_('LOT'), max_length=64, null=True, blank=True)
    recorded_borough = models.CharField(
        _('Recorded Borough'), max_length=64, null=True, blank=True)
    doc_type = models.CharField(
        _("DOC_TYPE"), max_length=64, null=True, blank=True)
    document_date = models.CharField(
        _('DOC.DATE'), max_length=64, null=True, blank=True)
    document_amt = models.DecimalField(
        _('DOC.AMOUNT'), default=0, max_digits=12, decimal_places=2)
    recorded_datetime = models.CharField(
        _('RECORDED / FILED'), max_length=64, null=True, blank=True)
    percent_trans = models.CharField(
        _('% TRANSFERRED'), max_length=64, null=True, blank=True)
    good_through_date = models.CharField(
        _('GOOD THROUGH DATE'), max_length=64, null=True, blank=True)
    step = models.IntegerField(_("Step"), default=0)

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")

    def __str__(self):
        return self.document_id

    def get_absolute_url(self):
        return reverse("propdoc_detail", kwargs={"pk": self.pk})
