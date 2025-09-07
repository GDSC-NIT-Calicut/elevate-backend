from rest_framework import serializers
from .models import Opportunity, Mentorship, Notification
from user.serializers import UserSerializer
from company.serializers import CompanySerializer
from tag.serializers import TagSerializer

class OpportunitySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    verified_by = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Opportunity
        fields = '__all__'

class MentorshipSerializer(serializers.ModelSerializer):
    mentor = UserSerializer(read_only=True)
    mentee = UserSerializer(read_only=True)
    
    class Meta:
        model = Mentorship
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
