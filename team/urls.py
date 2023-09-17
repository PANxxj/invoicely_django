from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path,include
router=DefaultRouter()

router.register('teams',TeamView,basename='teams')

urlpatterns=[
    path('',include(router.urls))
]