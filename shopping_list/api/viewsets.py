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
    
    @action(detail=False, methods=['PATCH'], url_path='mark-bulk-purchased', url_name='mark-bulk-purchased')
    def mark_bulk_purchased(self, request):
        """Custom action to bulk update data"""
        try:
            qs = ShoppingItem.objects.filter(id__in=request.data['shopping_items'])
            qs.update(purchased=request.data['value'])   # Actualiza compra
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)