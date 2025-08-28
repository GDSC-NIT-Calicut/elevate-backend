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
