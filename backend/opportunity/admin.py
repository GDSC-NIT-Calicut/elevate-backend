from django.contrib import admin
from .models import Opportunity, Notification

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ['title', 'opportunity_type', 'company', 'created_by', 'verified', 'created_date']
    list_filter = ['opportunity_type', 'verified', 'visibility', 'created_date']
    search_fields = ['title', 'description', 'company__name']
    readonly_fields = ['created_date', 'updated_date']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_date']
    list_filter = ['notification_type', 'is_read', 'created_date']
    search_fields = ['title', 'message', 'user__name']
