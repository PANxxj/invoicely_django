from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

class ClientView(ModelViewSet):
    serializer_class=ClientSerializer
    queryset=Client.objects.all()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)