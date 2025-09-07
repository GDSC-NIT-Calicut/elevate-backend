from django.shortcuts import render
from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework.views import APIView

from experience.serializers import ExperienceSerializer

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import generics, status
# Create your views here.

from rest_framework.permissions import IsAdminUser,IsAuthenticated, BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination


class IsAdminorSPOC(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role=='spoc' or request.user.role=='admin')


class IsAdminorSPOCorPR(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role=='spoc' or request.user.role=='admin' or request.user.role=='pr')

class ListCreateCompany(generics.ListCreateAPIView):
    authentication_classes=[JWTAuthentication]
    queryset=Company.objects.all()
    serializer_class=CompanySerializer

    def get_permissions(self):
        if self.request.method=='GET':
            return [IsAuthenticated()]
        return [IsAdminorSPOC()]

# Here we do not need to specify a lookup field since Django by default uses pk as the lookup field 
# Just be sure to add /<int:pk> in the urls.py file
class CompanyDetail(generics.RetrieveUpdateDestroyAPIView): 
    authentication_classes=[JWTAuthentication]
    
    queryset=Company.objects.all()
    serializer_class=CompanySerializer
    lookup_field='slug'


    def get_permissions(self):
        if self.request.method=='GET':
            return [IsAuthenticated()]
        return [IsAdminorSPOCorPR()]

class CompanyExperienceList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_field='slug'

    def get(self, request, slug):
        try:
            company = Company.objects.get(slug=slug)
        except Company.DoesNotExist:
            return Response({"detail": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        experiences = company.experiences.all()

        if request.user.role not in ['admin', 'spoc']:
            experiences = experiences.filter(visibility=True, verified=True)

        serializer = ExperienceSerializer(experiences, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListCompanies(generics.ListAPIView):
    queryset=Company.objects.all()
    serializer_class=CompanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']
    pagination_class = PageNumberPagination
    ordering = ['-created_at']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class CompanySearch(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get('search', '')
        
        if search_query:
            companies = Company.objects.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            ).order_by('name')
        else:
            companies = Company.objects.all().order_by('name')
        
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyAnalytics(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminorSPOCorPR]

    def get(self, request):
        from django.db.models import Count
        
        # Companies with most experiences
        companies_with_experiences = Company.objects.annotate(
            experience_count=Count('experiences')
        ).filter(experience_count__gt=0).order_by('-experience_count')[:10]
        
        # Companies with most opportunities
        companies_with_opportunities = Company.objects.annotate(
            opportunity_count=Count('opportunities')
        ).filter(opportunity_count__gt=0).order_by('-opportunity_count')[:10]
        
        # Total companies
        total_companies = Company.objects.count()
        
        return Response({
            'total_companies': total_companies,
            'companies_with_experiences': [
                {
                    'name': company.name,
                    'slug': company.slug,
                    'experience_count': company.experience_count
                }
                for company in companies_with_experiences
            ],
            'companies_with_opportunities': [
                {
                    'name': company.name,
                    'slug': company.slug,
                    'opportunity_count': company.opportunity_count
                }
                for company in companies_with_opportunities
            ],
        }, status=status.HTTP_200_OK)