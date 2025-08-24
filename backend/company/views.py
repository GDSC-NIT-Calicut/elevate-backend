from django.shortcuts import render
from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework.views import APIView

from backend.experience.serializers import ExperienceSerializer

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import generics, status
# Create your views here.

from rest_framework.permissions import IsAdminUser,IsAuthenticated, BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication


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

