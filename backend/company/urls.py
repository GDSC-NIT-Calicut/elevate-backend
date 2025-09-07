from django.urls import path
from .views import *

urlpatterns=[
    path('',ListCreateCompany.as_view(),name='company-list-create'),
    path('/<slug:slug>',CompanyDetail.as_view(),name='company-detail'),
    path('/<slug:slug>/experiences', CompanyExperienceList.as_view(), name='company-experiences'),
    path('/search', CompanySearch.as_view(), name='company-search'),
    path('/analytics', CompanyAnalytics.as_view(), name='company-analytics'),
]
