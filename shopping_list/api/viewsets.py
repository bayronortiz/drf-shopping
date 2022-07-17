# Python imports

# Django imports

# DRF imports
from rest_framework import viewsets

# Models imports
from shopping_list.models import ShoppingItem

# Serializers imports
from shopping_list.api.serializers import ShoppingItemSerializer


class ShoppingItemViewSet(viewsets.ModelViewSet):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer