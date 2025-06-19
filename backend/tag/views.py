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


class IsAdminorSPOC(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role=='spoc' or request.user.role=='admin')

class CreateTag(generics.ListCreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminorSPOC]
    queryset=Tag.objects.all()
    serializer_class=TagSerializer

# Here we do not need to specify a lookup field since Django by default uses pk as the lookup field 
# Just be sure to add /<int:pk> in the urls.py file
class TagDetail(generics.RetrieveUpdateDestroyAPIView): 
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminorSPOC]
    queryset=Tag.objects.all()
    serializer_class=TagSerializer

