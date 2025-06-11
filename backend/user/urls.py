from django.urls import path
from .views import *

urlpatterns=[
    path('google-oauth/',Signin.as_view(),name='Signin'),
    
]