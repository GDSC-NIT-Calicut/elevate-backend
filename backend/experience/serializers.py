from rest_framework import serializers
from .models import Experience
from user.models import User
from tag.models import Tag
from tag.serializers import TagSerializer

class AuthorSerialzer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['id','name','department']



class ExperienceSerializer(serializers.ModelSerializer):
    author=AuthorSerialzer(read_only=True)
    tags=TagSerializer(many=True, read_only=True)
    tag_ids=serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        source='tags', # maps to tag field in Experience model
        required=False
    )
    class Meta:
        model=Experience
        fields='__all__'
        read_only_fields=['author','published_date']

    def create(self,validated_data):
        tags=validated_data.pop('tags',[])
        validated_data.pop('verified',None)
        experience=Experience.objects.create(**validated_data)
        experience.tags.set(tags)
        return experience
    
    def update(self,instance,validated_data):
        request=self.context['request']
        role=getattr(request.user,'role',None)
        user=request.user
        
        if 'verified' in validated_data and role not in ['admin','spoc']:
            validated_data.pop('verified')
        
        if role=='admin' or user==instance.author :
            return super().update(instance,validated_data)
        elif role=='spoc':
            allowed_fields = {'verified', 'tags'}
            if any(field not in allowed_fields for field in validated_data.keys()):
                raise serializers.ValidationError("Spocs can only update verification status and tags.")
            print(validated_data.keys())
            return super().update(instance, validated_data)
        else:
            # Everyone else is denied
            raise serializers.ValidationError("You do not have permission to update this experience.")
