from django.urls import path
from .views import *

urlpatterns=[
    path('',ListCreateExperience.as_view(),name='experience-list-create'),
    path('/<int:pk>',ExperienceDetail.as_view(),name='experience-detail')
]