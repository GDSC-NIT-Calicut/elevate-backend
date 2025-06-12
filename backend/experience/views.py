from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Experience
from .serializers import ExperienceSerializer


@api_view(['GET'])
def get_all_experiences(request):
    experiences = Experience.objects.all()
    serializer = ExperienceSerializer(experiences, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_experience_by_id(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    serializer = ExperienceSerializer(experience)
    return Response(serializer.data)


@api_view(['POST'])
def create_experience(request):
    serializer = ExperienceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_experience(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    serializer = ExperienceSerializer(instance=experience, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_experience(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    experience.delete()
    return Response({'message': 'Experience deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
