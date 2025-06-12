from django.urls import path
from .views import *

urlpatterns = [
    path('', get_all_experiences, name='get_all_experiences'),
    path('<int:pk>/', get_experience_by_id, name='get_experience_by_id'),
    path('create/', create_experience, name='create_experience'),
    path('update/<int:pk>/', update_experience, name='update_experience'),
    path('delete/<int:pk>/', delete_experience, name='delete_experience'),
]