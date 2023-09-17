from django.db import models
from django.contrib.auth.models import User
from client.models import Client
from team.models import Team

class Invoice(models.Model):
    invoices=models.IntegerField(default=1)
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
    sender_refrence=models.CharField(max_length=225,blank=True,null=True)
    invoice_type=models.CharField(max_length=20,choices=(
        ('Invoice','Invoice'),
        ('Credit Note','Credit Note')
    ), default='Invoice')
    due_days=models.IntegerField(default=14)
    is_credit_for=models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True)
    is_send=models.BooleanField(default=False)
    is_paid=models.BooleanField(default=False)
    gross_amount=models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
    vat_amount=models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
    net_amount=models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
    discount_amount=models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True )
    team=models.ForeignKey(Team,on_delete=models.CASCADE,related_name='invoices')
    client=models.ForeignKey(Client,on_delete=models.CASCADE,related_name='invoices')
    created_by=models.ForeignKey(User,related_name='created_invoice',on_delete=models.CASCADE)
    modified_by=models.ForeignKey(User,related_name='updated_invoice',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.invoices} {self.name}'
    
    class Meta:
        odering=('-created_at',)
    

class Item(models.Model):
    invoice=models.ForeignKey(Invoice,related_name='items',on_delete=models.SET_NULL,null=True)
    title=models.CharField(max_length=225)
    quantity=models.IntegerField(default=1)
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)
    net_amount=models.DecimalField(max_digits=6,decimal_places=2)
    vat_rate=models.IntegerField(default=0)
    discount=models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.title    }'