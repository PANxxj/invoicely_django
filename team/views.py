from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import PermissionDenied
# Create your views here.


class TeamView(ModelViewSet):
    serializer_class=TeamSerilizer
    queryset=Team.objects.all()

    def get_queryset(self):
        teams=self.request.user.team.all()

        if not teams:
            Team.objects.create(name='',org_number='',created_by=self.request.user)
        return self.queryset.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        obj=self.get_object()
        if self.request.user!=obj.created_by:
            raise PermissionDenied('wrong object owner')
        serializer.save()