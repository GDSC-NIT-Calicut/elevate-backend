from django.urls import path
from .views import *

urlpatterns=[
    path('',ListCreateTag.as_view(),name='tag-list-create'),
    path('<int:pk>/',TagDetail.as_view(),name='tag-detail')
]
