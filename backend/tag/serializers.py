from rest_framework import serializers
from .models import Tag,TagType


class TagTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=TagType
        fields='__all__'



class TagSerializer(serializers.ModelSerializer):
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=TagType.objects.all(),
        write_only=True,
        source='type'
    )
    type = TagTypeSerializer(read_only=True)
    class Meta:
        model=Tag
        fields='__all__'