# Python imports
import pytest

# Django imports
from django.contrib.auth.models import User

# DRF imports
from rest_framework.test import APIClient

# Models imports
from shopping_list.models import ShoppingItem, ShoppingList


@pytest.fixture(scope='session')
def create_shopping_item():     # Clousure
    def _create_shopping_item(user, name, shopping_list_name='Mercado', shopping_list=None):
        if not shopping_list:
            shopping_list = ShoppingList.objects.create(name=shopping_list_name)
            shopping_list.members.add(user)
        shopping_item = ShoppingItem.objects.create(name=name, shopping_list=shopping_list)

        return shopping_item

    return _create_shopping_item


@pytest.fixture(scope='session')
def create_user():
    def _create_user():
        return User.objects.create_user(username='Testuser', password='testuser123')
    
    return _create_user


@pytest.fixture(scope='session')
def create_authenticated_client():
    def _create_authenticated_client(user):
        client = APIClient()
        client.force_login(user)
        return client
        
    return _create_authenticated_client


@pytest.fixture(scope='session')
def create_shopping_list():
    def _create_shopping_list(user, name='Artistas'):
        shopping_list = ShoppingList.objects.create(name=name)
        shopping_list.members.add(user)

        return shopping_list

    return _create_shopping_list