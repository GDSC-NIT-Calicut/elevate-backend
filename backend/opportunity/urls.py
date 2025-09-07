from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OpportunityViewSet, MentorshipViewSet, NotificationViewSet,
    SavedOpportunitiesList, OpportunityAnalytics, CreateNotification
)

router = DefaultRouter()
router.register(r'opportunities', OpportunityViewSet)
router.register(r'mentorships', MentorshipViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('opportunities/saved/', SavedOpportunitiesList.as_view(), name='saved-opportunities'),
    path('opportunities/analytics/', OpportunityAnalytics.as_view(), name='opportunity-analytics'),
    path('notifications/create/', CreateNotification.as_view(), name='create-notification'),
]
