from django.urls import path
from .views import *

urlpatterns=[
    path('',ListCreateCompany.as_view(),name='company-list-create'),
    path('<int:pk>/',CompanyDetail.as_view(),name='company-detail')
]
