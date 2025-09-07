from django.shortcuts import render
from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework.views import APIView


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import generics, status
# Create your views here.

from rest_framework.permissions import IsAdminUser,IsAuthenticated, BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q

class IsAdminorSPOC(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role=='spoc' or request.user.role=='admin')


class IsAdminorSPOCorPR(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role=='spoc' or request.user.role=='admin' or request.user.role=='pr')
    
# We use the module Q since writing :             
# return Experience.objects.filter(visibility=True).filter(verified=True) | Experience.objects.filter(author=user)
# makes 2 database queries and joins them. However when we use Q, it sends it as one query making it much faster
# useful when dealing with large datasets


class ListVerifiedExperience(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self,request):
        tags=request.data.get('tag_ids',[])
        if not isinstance(tags, list):
            return Response({"error": "tags must be a list"}, status=400)

        queryset= Experience.objects.filter(visibility=True,verified=True).distinct()
        
        if tags:
            queryset=queryset.filter(tags__id__in=tags).distinct()  
        serializer = ExperienceSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=200)

class CreateExperience(generics.CreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    serializer_class=ExperienceSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ExperienceDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    serializer_class=ExperienceSerializer
    
    def get_queryset(self):
        user=self.request.user
        
        if user.role in ['admin','spoc']:
            return Experience.objects.all()
        else:
            return Experience.objects.filter(
                Q(visibility=True,verified=True) | Q(author=user)
            ).distinct()

    def perform_destroy(self,instance):
        user=self.request.user
        if user==instance.author or user.role=='admin' or user.role=='spoc':
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this experience.")

class UnverifiedExperienceList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminorSPOCorPR]

    def get(self, request):
        queryset = Experience.objects.filter(verified=False)
        serializer = ExperienceSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyExperienceList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ExperienceSerializer
    def get_queryset(self):
        queryset = Experience.objects.filter(author=self.request.user)
        return queryset

class SaveUnsaveExperience(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self,request,pk):
        user=request.user

        try:
            experience=Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            return Response({"error":"Experience not found"},status=404)
        if experience.saved_by.filter(id=user.id).exists():
            experience.saved_by.remove(user)
            return Response({"message":"Experience unsaved"},status=200)
        else:
            experience.saved_by.add(user)
            return Response({"message":"Experience saved"},status=200)

class SavedExperiencesList(generics.ListAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=ExperienceSerializer

    def get_queryset(self):
        return self.request.user.saved_experiences.all().order_by('-id')


class ExperienceSearch(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get search parameters
        search_query = request.data.get('search', '')
        company = request.data.get('company', '')
        role = request.data.get('role', '')
        year = request.data.get('year', '')
        department = request.data.get('department', '')
        offer_type = request.data.get('offerType', '')
        verified = request.data.get('verified', '')
        tags = request.data.get('tags', [])
        date_range = request.data.get('dateRange', {})

        # Start with verified and visible experiences
        queryset = Experience.objects.filter(visibility=True, verified=True)

        # Apply filters
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(role__icontains=search_query) |
                Q(short_description__icontains=search_query) |
                Q(company__name__icontains=search_query) |
                Q(author__name__icontains=search_query)
            )

        if company:
            queryset = queryset.filter(company__slug=company)

        if role:
            queryset = queryset.filter(role__icontains=role)

        if year:
            queryset = queryset.filter(experience_date__year=year)

        if department:
            queryset = queryset.filter(author__department=department)

        if offer_type:
            queryset = queryset.filter(job_type=offer_type)

        if verified == 'verified':
            queryset = queryset.filter(verified=True)
        elif verified == 'unverified':
            queryset = queryset.filter(verified=False)

        if tags:
            queryset = queryset.filter(tags__id__in=tags).distinct()

        if date_range.get('start'):
            from datetime import datetime
            start_date = datetime.strptime(date_range['start'], '%Y-%m-%d').date()
            queryset = queryset.filter(experience_date__gte=start_date)

        if date_range.get('end'):
            from datetime import datetime
            end_date = datetime.strptime(date_range['end'], '%Y-%m-%d').date()
            queryset = queryset.filter(experience_date__lte=end_date)

        # Order by published date
        queryset = queryset.order_by('-published_date')

        serializer = ExperienceSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExperienceAnalytics(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminorSPOCorPR]

    def get(self, request):
        from django.db.models import Count
        from datetime import datetime, timedelta

        # Basic counts
        total_experiences = Experience.objects.count()
        verified_experiences = Experience.objects.filter(verified=True).count()
        pending_experiences = Experience.objects.filter(verified=False).count()
        verification_rate = (verified_experiences / total_experiences * 100) if total_experiences > 0 else 0

        # Experiences by month (last 6 months)
        six_months_ago = datetime.now() - timedelta(days=180)
        experiences_by_month = Experience.objects.filter(
            published_date__gte=six_months_ago
        ).extra(
            select={'month': "DATE_TRUNC('month', published_date)"}
        ).values('month').annotate(count=Count('id')).order_by('month')

        # Experiences by company (top 10)
        experiences_by_company = Experience.objects.values('company__name').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        # Experiences by department
        experiences_by_department = Experience.objects.values('author__department').annotate(
            count=Count('id')
        ).order_by('-count')

        # Experiences by job type
        experiences_by_job_type = Experience.objects.values('job_type').annotate(
            count=Count('id')
        ).order_by('-count')

        return Response({
            'total_experiences': total_experiences,
            'verified_experiences': verified_experiences,
            'pending_experiences': pending_experiences,
            'verification_rate': round(verification_rate, 2),
            'experiences_by_month': list(experiences_by_month),
            'experiences_by_company': list(experiences_by_company),
            'experiences_by_department': list(experiences_by_department),
            'experiences_by_job_type': list(experiences_by_job_type),
        }, status=status.HTTP_200_OK)