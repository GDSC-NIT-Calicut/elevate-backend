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