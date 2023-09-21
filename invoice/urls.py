from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path,include

router=DefaultRouter()
router.register('invoices',InvoiceView,basename='invoices')
router.register('items',ItemView,basename='items')

urlpatterns=[
    path('',include(router.urls)),
    path('invoices/<int:invoice_id>/generate_pdf/',generate_pdf,name='generate_pdf')
]