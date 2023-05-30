"""Defines URL patterns for solution_site"""

from django.urls import path
from .views import GoogleCalendarInitView, GoogleCalendarRedirectView, homePage

app_name = 'solution_app'

urlpatterns = [
    # Home page and only page
    path('', homePage, name='homePage'),
    path('rest/v1/calendar/init/', GoogleCalendarInitView.as_view(), name='init'),
    path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView.as_view(), name='redirect'),
]