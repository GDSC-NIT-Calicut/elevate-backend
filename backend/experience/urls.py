from django.urls import path
from .views import *

urlpatterns=[
    path('',ListExperience.as_view(),name='experience-list'),
    path('/<int:pk>',ExperienceDetail.as_view(),name='experience-detail'),
    path('/create',CreateExperience.as_view(),name='experience-create'),
    path('/unverified', UnverifiedExperienceList.as_view(), name='unverified-experiences')
]