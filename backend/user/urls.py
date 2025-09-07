from django.urls import path
from .views import *

urlpatterns=[
    path('/google-oauth',Signin.as_view(),name='Signin'),
    path('/backup-email',Backup_Email.as_view(),name='Backup-Email'),
    path('/set-pr', SetPRRole.as_view(), name='set-pr'),
    path('/set-spoc', SetSPOCRole.as_view(), name='set-spoc'),
    path('/profile', UserProfile.as_view(), name='user-profile'),
    path('/list', UserList.as_view(), name='user-list'),
    path('/<int:id>', UserDetail.as_view(), name='user-detail'),
    path('/roll/<str:roll_number>', UserByRollNumber.as_view(), name='user-by-roll'),
]