from rest_framework import serializers
from .models import Tag,TagType

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields='__all__'


class TagTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=TagType
        fields='__all__'

        