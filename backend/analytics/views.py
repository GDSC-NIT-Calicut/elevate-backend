from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Count
from datetime import datetime, timedelta

from user.models import User
from company.models import Company
from experience.models import Experience
from opportunity.models import Opportunity, Notification
from tag.models import Tag, TagType

class IsAdminorSPOCorPR(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role=='spoc' or request.user.role=='admin' or request.user.role=='pr')

class DashboardAnalytics(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminorSPOCorPR]

    def get(self, request):
        # Basic counts
        total_users = User.objects.count()
        total_companies = Company.objects.count()
        total_experiences = Experience.objects.count()
        total_opportunities = Opportunity.objects.count()
        total_notifications = Notification.objects.count()
        total_tags = Tag.objects.count()

        # Verification stats
        verified_experiences = Experience.objects.filter(verified=True).count()
        pending_experiences = Experience.objects.filter(verified=False).count()
        verified_opportunities = Opportunity.objects.filter(verified=True).count()
        pending_opportunities = Opportunity.objects.filter(verified=False).count()

        # User role distribution
        user_roles = User.objects.values('role').annotate(count=Count('id')).order_by('-count')

        # Recent activity (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_experiences = Experience.objects.filter(published_date__gte=thirty_days_ago).count()
        recent_opportunities = Opportunity.objects.filter(created_date__gte=thirty_days_ago).count()
        recent_users = User.objects.filter(date_joined__gte=thirty_days_ago).count()

        # Top companies by experiences
        top_companies_experiences = Company.objects.annotate(
            experience_count=Count('experiences')
        ).filter(experience_count__gt=0).order_by('-experience_count')[:5]

        # Top companies by opportunities
        top_companies_opportunities = Company.objects.annotate(
            opportunity_count=Count('opportunities')
        ).filter(opportunity_count__gt=0).order_by('-opportunity_count')[:5]

        # Department distribution
        department_stats = User.objects.exclude(department__isnull=True).exclude(department='').values('department').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        # Program distribution
        program_stats = User.objects.exclude(programme__isnull=True).exclude(programme='').values('programme').annotate(
            count=Count('id')
        ).order_by('-count')

        # Monthly trends (last 6 months)
        six_months_ago = datetime.now() - timedelta(days=180)
        
        # Experiences by month
        experiences_by_month = Experience.objects.filter(
            published_date__gte=six_months_ago
        ).extra(
            select={'month': "DATE_TRUNC('month', published_date)"}
        ).values('month').annotate(count=Count('id')).order_by('month')

        # Opportunities by month
        opportunities_by_month = Opportunity.objects.filter(
            created_date__gte=six_months_ago
        ).extra(
            select={'month': "DATE_TRUNC('month', created_date)"}
        ).values('month').annotate(count=Count('id')).order_by('month')

        # Job type distribution
        job_type_stats = Experience.objects.values('job_type').annotate(
            count=Count('id')
        ).order_by('-count')

        # Opportunity type distribution
        opportunity_type_stats = Opportunity.objects.values('opportunity_type').annotate(
            count=Count('id')
        ).order_by('-count')

        # Notification stats
        unread_notifications = Notification.objects.filter(is_read=False).count()
        notification_types = Notification.objects.values('notification_type').annotate(
            count=Count('id')
        ).order_by('-count')

        return Response({
            'overview': {
                'total_users': total_users,
                'total_companies': total_companies,
                'total_experiences': total_experiences,
                'total_opportunities': total_opportunities,
                'total_notifications': total_notifications,
                'total_tags': total_tags,
            },
            'verification': {
                'verified_experiences': verified_experiences,
                'pending_experiences': pending_experiences,
                'verified_opportunities': verified_opportunities,
                'pending_opportunities': pending_opportunities,
                'experience_verification_rate': round((verified_experiences / total_experiences * 100), 2) if total_experiences > 0 else 0,
                'opportunity_verification_rate': round((verified_opportunities / total_opportunities * 100), 2) if total_opportunities > 0 else 0,
            },
            'user_stats': {
                'user_roles': list(user_roles),
                'department_distribution': list(department_stats),
                'program_distribution': list(program_stats),
            },
            'activity': {
                'recent_experiences': recent_experiences,
                'recent_opportunities': recent_opportunities,
                'recent_users': recent_users,
            },
            'companies': {
                'top_by_experiences': [
                    {
                        'name': company.name,
                        'slug': company.slug,
                        'count': company.experience_count
                    }
                    for company in top_companies_experiences
                ],
                'top_by_opportunities': [
                    {
                        'name': company.name,
                        'slug': company.slug,
                        'count': company.opportunity_count
                    }
                    for company in top_companies_opportunities
                ],
            },
            'trends': {
                'experiences_by_month': list(experiences_by_month),
                'opportunities_by_month': list(opportunities_by_month),
            },
            'content_types': {
                'job_types': list(job_type_stats),
                'opportunity_types': list(opportunity_type_stats),
            },
            'notifications': {
                'unread_count': unread_notifications,
                'types': list(notification_types),
            },
        }, status=status.HTTP_200_OK)
