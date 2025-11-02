from django.shortcuts import render
from rest_framework import generics
from basic_api.models import DRFPost
from basic_api.serializers import DRFPostSerializer

class API_objects(generics.ListCreateAPIView):
    queryset = DRFPost.objects.all()
    serializer_class = DRFPostSerializer

    def get_queryset (self):
        queryset = DRFPost.objects.all()
        search = self.request.query_params.get('search', None)

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset

class API_objects_details(generics.RetrieveUpdateDestroyAPIView):
    queryset = DRFPost.objects.all()
    serializer_class = DRFPostSerializer