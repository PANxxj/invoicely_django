from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name=models.CharField(max_length=255)
    org_number=models.CharField(max_length=255,blank=True,null=True)
    first_invoice_number=models.IntegerField(default=1)
    bank_account=models.CharField(max_length=255,blank=True,null=True)
    created_by=models.ForeignKey(User,related_name='team',on_delete=models.SET_NULL,null=True)

    def __str__(self) -> str:
        return f'{self.name}'

