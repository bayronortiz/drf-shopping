# Django imports
from email.mime import base
from django.urls import path, include

# DRF imports
from rest_framework import routers

# Views imports
from shopping_list.api.views import ListAddShoppingList, ShoppingListDetail

# Viewsets imports
from shopping_list.api.viewsets import ShoppingItemViewSet


# router = routers.DefaultRouter()
# router.register('shopping-items', ShoppingItemViewSet, basename='shopping-items')

urlpatterns = [
    # path('api/', include(router.urls))
    path('api/shopping-lists/', ListAddShoppingList.as_view(), name='all_shopping_lists'),
    path('api/shopping-lists/<uuid:pk>/', ShoppingListDetail.as_view(), name='shopping_list_detail')
]