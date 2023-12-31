from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from django.core.exceptions import PermissionDenied

class ClientView(ModelViewSet):
    serializer_class=ClientSerializer
    queryset=Client.objects.all()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        obj=self.get_object()
        if self.request.user!=obj.created_by:
            raise PermissionDenied('wrong object owner')
        serializer.save()