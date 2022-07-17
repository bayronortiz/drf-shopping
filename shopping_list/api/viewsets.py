# Python imports

# Django imports

# DRF imports
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Models imports
from shopping_list.models import ShoppingItem

# Serializers imports
from shopping_list.api.serializers import ShoppingItemSerializer


class ShoppingItemViewSet(viewsets.ModelViewSet):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer

    @action(detail=False, methods=['DELETE'], url_path='delete-all-purchased', url_name='delete-all-purchased')
    def delete_purchased(self, request):
        """Custom action to bulk delete data"""
        ShoppingItem.objects.filter(purchased=True).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['DELETE'], url_path='delete-all', url_name='delete-all')
    def delete_all(self, request):
        """Custom action to bulk delete data"""
        ShoppingItem.objects.all().delete()

        return Response(status=status.HTTP_204_NO_CONTENT)