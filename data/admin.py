from django.contrib import admin
from data.models import *
# Register your models here.


@admin.action(description='Reset to step 0')
def reset_step(modeladmin, request, queryset):
    queryset.update(step=0)


@admin.register(Criteria)
class CriteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'text_value', 'date_value', 'qtype')


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):

    list_display = ('unique_key', 'bbl', 'created_date', 'closed_date', 'agency', 'complaint_type',
                    'descriptor', 'status', 'incident_zip', 'incident_address', 'city', 'step')
    actions = [reset_step]


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('parid', 'extracrdt', 'boro', 'block', 'lot', 'pymkttot', 'curmkttot', 'bldg_class', 'bld_story', 'units', 'lot_frt', 'lot_dep',
                    'bld_frt', 'bld_dep', 'land_area', 'gross_sqft', 'owner', 'zoning', 'housenum_lo', 'housenum_hi', 'street_name', 'zip_code', 'corner', 'step')
    actions = [reset_step]


@admin.register(PropDocument)
class PropDocumentAdmin(admin.ModelAdmin):
    list_display = ('document_id', 'borough', 'block', 'lot', 'recorded_borough', 'doc_type',
                    'document_date', 'document_amt', 'recorded_datetime', 'percent_trans', 'good_through_date')


@admin.register(Csv)
class CsvAdmin(admin.ModelAdmin):
    list_display = ('file', 'status')
    readonly_fields = ["status"]
