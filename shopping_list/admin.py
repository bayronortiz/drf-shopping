# Django imports
from django.contrib import admin

# Models imports
from shopping_list.models import ShoppingItem, ShoppingList


admin.site.register(ShoppingList)
admin.site.register(ShoppingItem)