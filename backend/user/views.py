from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework.views import APIView


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import generics, status
# Create your views here.
from django.contrib.auth import authenticate

from rest_framework_simplejwt.authentication import JWTAuthentication

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.http import JsonResponse

from django.conf import settings

from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import BasePermission

CLIENT_ID=settings.CLIENT_ID

def verify_google_id_token(token: str):

    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), CLIENT_ID)
        if idinfo['aud'] != CLIENT_ID:
            return {"valid": False, "message": "Invalid client ID"}

        return {
            "valid": True,
        }
    except ValueError as e:
        return {"valid": False}

class IsAdminorSPOC(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'spoc']        
        

class Signin(APIView):

    def post(self,request):
        token= request.data.get('id_token')
        result =verify_google_id_token(token)

        if result['valid']==False:
            return Response({"success": False,'status': 401, 'message': "Invalid Credentials"},status=status.HTTP_401_UNAUTHORIZED)
        
        email=request.data.get('email')
        user=User.objects.filter(email=email).first()
            
        if not user:
            user=User.objects.filter(backup_email=email).first()

        if not user:
            
            if email.endswith('@nitc.ac.in'):
                user=User.objects.create(
                    email=email,
                    name=request.data.get('name'),
                    roll_number=request.data.get('roll_number'),
                    department=request.data.get('department'),
                    programme=request.data.get('programme'),
                    role='student',
                )
            
            else:
                return Response({"success": False,'status': 404, 'message': "Not found"},status=status.HTTP_404_NOT_FOUND)
        
        refresh=RefreshToken.for_user(user)


        return Response({
            'status': 200,
            "success": True,
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            "user": {
                "email": user.email,
                "backup_email":user.backup_email,
                "name": user.name,
                "roll_number": user.roll_number,
                "department": user.department,
                "programme": user.programme,
                "role": user.role
            }
        }, status=status.HTTP_202_ACCEPTED)
        
class Backup_Email(APIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self,request):
        user=request.user

        backup_email=request.data.get('backup_email')

        if not backup_email:
            return Response({
                "success": False,
                "message": "Backup email is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.backup_email=backup_email
        user.save()

        return Response({
            "success": True,
            "message": "Backup email added successfully.",
            "user": {
                "email": user.email,
                "backup_email": user.backup_email
            }
        }, status=status.HTTP_200_OK)


class SetPRRole(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminorSPOC]

    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"success": False, "message": "Email is required."}, status=400)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"success": False, "message": "User not found."}, status=404)

        user.role = 'pr'
        user.save()

        return Response({"success": True, "message": f"{user.name} set as PR."}, status=200)


class SetSPOCRole(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminorSPOC]

    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"success": False, "message": "Email is required."}, status=400)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"success": False, "message": "User not found."}, status=404)

        user.role = 'spoc'
        user.save()

        return Response({"success": True, "message": f"{user.name} set as SPOC."}, status=200)
    

#Profile Page
class UserProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "success": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "backup_email": user.backup_email,
                "name": user.name,
                "roll_number": user.roll_number,
                "department": user.department,
                "programme": user.programme,
                "role": user.role,
                "is_active": user.is_active,
                "is_staff": user.is_staff
            }
        }, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        data = request.data

        # Allow users to update their own profile
        allowed_fields = ['backup_email', 'name', 'roll_number', 'department', 'programme']
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])

        user.save()

        return Response({
            "success": True,
            "message": "Profile updated successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "backup_email": user.backup_email,
                "name": user.name,
                "roll_number": user.roll_number,
                "department": user.department,
                "programme": user.programme,
                "role": user.role
            }
        }, status=status.HTTP_200_OK)


class UserList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminorSPOC]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "users": serializer.data
        }, status=status.HTTP_200_OK)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminorSPOC]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "success": True,
            "user": serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "success": True,
            "message": "User updated successfully",
            "user": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "success": True,
            "message": "User deleted successfully"
        }, status=status.HTTP_200_OK)


class UserByRollNumber(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, roll_number):
        try:
            user = User.objects.get(roll_number=roll_number)
            serializer = UserSerializer(user)
            return Response({
                "success": True,
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                "success": False,
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
