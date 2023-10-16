from rest_framework import serializers
from .models import *
from invoice.models import Invoice

class clinetInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Invoice
        fields=(
            "id",
            "invoices", 
            "invoice_type",
            "is_send",
            "is_paid",
            "gross_amount",
            "vat_amount",
            "net_amount",
            "get_due_date_formatted",
            "is_credited",
        )

class ClientSerializer(serializers.ModelSerializer):
    invoices=clinetInvoiceSerializer(many=True)
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
            "invoices",
        )