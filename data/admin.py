from django.contrib import admin
from data.models import *
# Register your models here.


@admin.register(Criteria)
class CriteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'text_value', 'date_value', 'qtype')


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):

    list_display = ('unique_key', 'created_date', 'closed_date', 'agency', 'complaint_type',
                    'descriptor', 'status', 'incident_zip', 'incident_address', 'city')
