from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Client(models.Model):
    name=models.CharField(max_length=225)
    email=models.EmailField()
    org_number=models.CharField(max_length=225,blank=True,null=True)
    address1=models.CharField(max_length=225,blank=True,null=True)
    address2=models.CharField(max_length=225,blank=True,null=True)
    zip_code=models.CharField(max_length=225,blank=True,null=True)
    place=models.CharField(max_length=225,blank=True,null=True)
    country=models.CharField(max_length=225,blank=True,null=True)
    contact_person=models.CharField(max_length=225,blank=True,null=True)
    contact_refrence=models.CharField(max_length=225,blank=True,null=True)
    created_by=models.ForeignKey(User,related_name='clients',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.name)
