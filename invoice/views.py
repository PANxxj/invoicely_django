from django.shortcuts import render
from .serializers  import *
from .models import *
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import PermissionDenied

class InvoiceView(ModelViewSet):
    serializer_class=InvoiceSerializer
    queryset=Invoice.objects.all()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        team=self.request.user.team.first()

        serializer.save(created_by=self.request.user,team=team)

    def perform_update(self, serializer):
        obj=self.get_object()
        if self.request.user!=obj.created_by:
            raise PermissionDenied('wrong object owner')
        serializer.save()

class ItemView(ModelViewSet):
    serializer_class=ItemSerializer
    queryset=Item.objects.all()

    def get_queryset(self):
        id=self.request.GET.get('invoice_id',0)
        return self.queryset.filter(invoice__id=id)