from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'backup_email', 'name', 'roll_number', 
            'department', 'programme', 'role', 'is_active', 'is_staff'
        ]
        read_only_fields = ['id', 'email', 'is_active', 'is_staff']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'roll_number', 'department', 'programme', 'role']
