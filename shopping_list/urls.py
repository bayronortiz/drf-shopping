# Django imports
from email.mime import base
from django.urls import path, include

# DRF imports
from rest_framework import routers

# Viewsets imports
from shopping_list.api.viewsets import ShoppingItemViewSet


router = routers.DefaultRouter()
router.register('shopping-items', ShoppingItemViewSet, basename='shopping-items')

urlpatterns = [
    path('api/', include(router.urls))
]