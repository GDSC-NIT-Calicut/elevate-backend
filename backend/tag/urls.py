from django.urls import path
from .views import *

urlpatterns=[
    path('tags/',CreateTag.as_view(),name='tag-list-create'),
    path('tags/<int:pk>/',TagDetail.as_view(),name='tag-detail')
]
