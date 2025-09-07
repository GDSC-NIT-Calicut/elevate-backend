from django.urls import path
from .views import DashboardAnalytics

urlpatterns = [
    path('dashboard/', DashboardAnalytics.as_view(), name='dashboard-analytics'),
]
