from django.urls import path
from .views import *

urlpatterns=[
    path('',ListVerifiedExperience.as_view(),name='experience-list'),
    path('/<int:pk>',ExperienceDetail.as_view(),name='experience-detail'),
    path('/create',CreateExperience.as_view(),name='experience-create'),
    path('/unverified', UnverifiedExperienceList.as_view(), name='unverified-experiences'),
    path('/self', MyExperienceList.as_view(), name='my-experiences'),
]