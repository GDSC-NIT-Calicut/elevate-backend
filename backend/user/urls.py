from django.urls import path
from .views import *

urlpatterns=[
    path('google-oauth/',Signin.as_view(),name='Signin'),
    path('backup-email/',Backup_Email.as_view(),name='Backup-Email'),
    
]