# Python imports

# Django imports

# DRF imports
from rest_framework import serializers

# Models imports
from shopping_list.models import ShoppingItem


class ShoppingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingItem
        fields = ['id', 'name', 'purchased']