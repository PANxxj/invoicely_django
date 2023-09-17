from rest_framework import serializers
from .models import *

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Client
        # read_only=('created_by',)
        # fields='__all__'
        # exclude=('created_by',)

        read_only_fields = (
            "created_at",
            "created_by",
        ),
        fields = (
            "id",
            "name",
            "email",
            "org_number",
            "address1",
            "address2",
            "zip_code",
            "place",
            "country",
            "contact_person",
            "contact_refrence",
            # "invoices",
        )