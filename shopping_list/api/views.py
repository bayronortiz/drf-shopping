# Python imports
# Django imports
# DRF imports
from rest_framework import generics

# Models imports
from shopping_list.models import ShoppingList, ShoppingItem

# Serializers imports
from shopping_list.api.serializers import ShoppingListSerializer, ShoppingItemSerializer


class ListAddShoppingList(generics.ListCreateAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer

    def perform_create(self, serializer):
        return serializer.save(members=[self.request.user])


class ShoppingListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer


class AddShoppingItem(generics.CreateAPIView):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer


class ShoppingItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer
    lookup_url_kwarg = 'item_pk'    # pk url 