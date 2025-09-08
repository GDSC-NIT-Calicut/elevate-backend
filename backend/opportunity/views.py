from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from django.db.models import Q
from .models import Opportunity, Mentorship, Notification
from .serializers import OpportunitySerializer, MentorshipSerializer, NotificationSerializer
from user.models import User
from user.serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
class IsAdminorSPOCorPR(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role=='spoc' or request.user.role=='admin' or request.user.role=='pr')

class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Opportunity.objects.filter(visibility=True)
        
        # Filter by opportunity type
        opportunity_type = self.request.query_params.get('type', None)
        if opportunity_type:
            queryset = queryset.filter(opportunity_type=opportunity_type)
            
        # Filter by company
        company = self.request.query_params.get('company', None)
        if company:
            queryset = queryset.filter(company__slug=company)
            
        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
            
        return queryset.order_by('-created_date')
    
    @action(detail=True, methods=['post'])
    def save(self, request, pk=None):
        opportunity = self.get_object()
        opportunity.saved_by.add(request.user)
        return Response({'status': 'saved'})
    
    @action(detail=True, methods=['post'])
    def unsave(self, request, pk=None):
        opportunity = self.get_object()
        opportunity.saved_by.remove(request.user)
        return Response({'status': 'unsaved'})
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        if request.user.role not in ['pr', 'spoc', 'admin']:
            return Response({'error': 'Insufficient permissions'}, status=status.HTTP_403_FORBIDDEN)
        
        opportunity = self.get_object()
        opportunity.verified = True
        opportunity.verified_by = request.user
        opportunity.save()
        return Response({'status': 'verified'})

class MentorshipViewSet(viewsets.ModelViewSet):
    queryset = Mentorship.objects.all()
    serializer_class = MentorshipSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Mentorship.objects.filter(
            Q(mentor=user) | Q(mentee=user)
        ).order_by('-created_date')
    
    @action(detail=False, methods=['get'])
    def available_mentors(self, request):
        # Get users who can be mentors (seniors, alumni, etc.)
        mentors = User.objects.filter(
            role__in=['student', 'spoc', 'pr', 'admin']
        ).exclude(id=request.user.id)
        return Response(UserSerializer(mentors, many=True).data)

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_date')
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'all marked as read'})

    def destroy(self, request, pk=None):
        notification = self.get_object()
        notification.delete()
        return Response({'status': 'deleted'})


class SavedOpportunitiesList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        saved_opportunities = Opportunity.objects.filter(
            saved_by=request.user,
            visibility=True
        ).order_by('-created_date')
        
        serializer = OpportunitySerializer(saved_opportunities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OpportunityAnalytics(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminorSPOCorPR]

    def get(self, request):
        from django.db.models import Count
        from datetime import datetime, timedelta

        # Basic counts
        total_opportunities = Opportunity.objects.count()
        verified_opportunities = Opportunity.objects.filter(verified=True).count()
        pending_opportunities = Opportunity.objects.filter(verified=False).count()
        verification_rate = (verified_opportunities / total_opportunities * 100) if total_opportunities > 0 else 0

        # Opportunities by type
        opportunities_by_type = Opportunity.objects.values('opportunity_type').annotate(
            count=Count('id')
        ).order_by('-count')

        # Opportunities by month (last 6 months)
        six_months_ago = datetime.now() - timedelta(days=180)
        opportunities_by_month = Opportunity.objects.filter(
            created_date__gte=six_months_ago
        ).extra(
            select={'month': "DATE_TRUNC('month', created_date)"}
        ).values('month').annotate(count=Count('id')).order_by('month')

        # Opportunities by company (top 10)
        opportunities_by_company = Opportunity.objects.filter(
            company__isnull=False
        ).values('company__name').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        return Response({
            'total_opportunities': total_opportunities,
            'verified_opportunities': verified_opportunities,
            'pending_opportunities': pending_opportunities,
            'verification_rate': round(verification_rate, 2),
            'opportunities_by_type': list(opportunities_by_type),
            'opportunities_by_month': list(opportunities_by_month),
            'opportunities_by_company': list(opportunities_by_company),
        }, status=status.HTTP_200_OK)


class CreateNotification(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminorSPOCorPR]

    def post(self, request):
        title = request.data.get('title')
        message = request.data.get('message')
        notification_type = request.data.get('notification_type', 'system')
        user_id = request.data.get('user_id')
        related_opportunity_id = request.data.get('related_opportunity_id')
        related_experience_id = request.data.get('related_experience_id')

        if not title or not message:
            return Response({
                'error': 'Title and message are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        notification_data = {
            'title': title,
            'message': message,
            'notification_type': notification_type,
            'user_id': user_id,
        }

        if related_opportunity_id:
            notification_data['related_opportunity_id'] = related_opportunity_id
        if related_experience_id:
            notification_data['related_experience_id'] = related_experience_id

        serializer = NotificationSerializer(data=notification_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)