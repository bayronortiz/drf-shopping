# Django imports
from email.mime import base
from django.urls import path, include

# DRF imports
from rest_framework import routers

# Views imports
from shopping_list.api.views import (
    ListAddShoppingList, ShoppingListDetail, AddShoppingItem, ShoppingItemDetail
)

# Viewsets imports
from shopping_list.api.viewsets import ShoppingItemViewSet


# router = routers.DefaultRouter()
# router.register('shopping-items', ShoppingItemViewSet, basename='shopping-items')

urlpatterns = [
    # path('api/', include(router.urls))
    path('api/shopping-lists/', ListAddShoppingList.as_view(), name='all-shopping-lists'),
    path('api/shopping-lists/<uuid:pk>/', ShoppingListDetail.as_view(), name='shopping-list-detail'),
    path('api/shopping-lists/<uuid:pk>/shopping-items/', AddShoppingItem.as_view(), name='add-shopping-item'),
    path('api/shopping-lists/<uuid:pk>/shopping-items/<uuid:item_pk>/', ShoppingItemDetail.as_view(), name='shopping-item-detail')
]