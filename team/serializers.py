from .models import *
from rest_framework import serializers


class TeamSerilizer(serializers.ModelSerializer):
    class Meta:
        model=Team
        fields='__all__'