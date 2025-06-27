from django.urls import path
from .views import *

urlpatterns=[
    path('',ListCreateTag.as_view(),name='tag-list-create'),
    path('/<int:pk>',TagDetail.as_view(),name='tag-detail'),
    path('/type',ListCreateTagType.as_view(),name='tagtype-list-create'),
    path('/type/<int:pk>',TagTypeDetail.as_view(),name='tagtype-detail'),
    path('/type/<int:pk>/tags', TagsByTagType.as_view(), name='tags-by-type')
]
