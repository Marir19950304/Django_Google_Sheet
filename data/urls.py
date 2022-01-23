from django.conf.urls import url
from . import views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.user_main, name='main'),
    url(r'^runbutton1', views.fetch_google_sheet_1, name="runbutton1"),
    url(r'^runbutton2', views.fetch_google_sheet_2, name="runbutton2"),
    url(r'^runbutton3', views.fetch_google_sheet_3, name="runbutton3"),
    url(r'^runbutton4', views.fetch_google_sheet_4, name="runbutton4"),
    url(r'^runbutton5', views.fetch_google_sheet_5, name="runbutton5"),
    url(r'^reloadbutton', views.reload_google_sheet, name="reloadbutton")
]
