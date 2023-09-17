from .models import *
from rest_framework  import serializers

class InvoiceSerializer(serializers.ModelSerializer):
    client=serializers.StringRelatedField()
    class Meta:
        model=Invoice
        fields='__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields='__all__'