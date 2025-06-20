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
    
# We use the module Q since writing :             
# return Experience.objects.filter(visibility=True).filter(verified=True) | Experience.objects.filter(author=user)
# makes 2 database queries and joins them. However when we use Q, it sends it as one query making it much faster
# useful when dealing with large datasets


class ListCreateExperience(generics.ListCreateAPIView):
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
