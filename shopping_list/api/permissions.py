# Python imports
# Django imports
# DRF imports
from math import perm
from rest_framework import permissions

# Models imports
from shopping_list.models import ShoppingList


class ShoppingListMembersOnly(permissions.BasePermission):  # Detail list
    
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.is_superuser:
            return True
        
        if request.user in obj.members.all():
            return True

        return False


class ShoppingItemShoppingListMembersOnly(permissions.BasePermission):  # Items list

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.is_superuser:
            return True
        
        if request.user in obj.shopping_list.members.all():
            return True

        return False


class AllShoppingItemsShoppingListMembersOnly(permissions.BasePermission):  # Detail items

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.is_superuser:
            return True
        
        current_shopping_list = ShoppingList.objects.get(pk=view.kwargs.get('pk'))
        if request.user in current_shopping_list.members.all():
            return True

        return False