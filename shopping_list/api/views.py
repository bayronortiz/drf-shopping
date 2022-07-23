# Python imports
# Django imports
# DRF imports
from rest_framework import generics

# Models imports
from shopping_list.models import ShoppingList

# Serializers imports
from shopping_list.api.serializers import ShoppingListSerializer


class ListAddShoppingList(generics.ListCreateAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer


class ShoppingListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer