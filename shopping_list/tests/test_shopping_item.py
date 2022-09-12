# Python imports
import pytest
import uuid
import json


# Django imports
from django.urls import reverse
from django.contrib.auth.models import User

# DRF imports
from rest_framework import status
from rest_framework.test import APIClient

# Models imports
from shopping_list.models import ShoppingList, ShoppingItem


# CREATE TEST
@pytest.mark.django_db
def test_valid_shopping_item_is_created(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user)
    shopping_list = create_shopping_list(user, name='Mercado')
    # shopping_list = ShoppingList.objects.create(name='Mercado')

    url = reverse('add-shopping-item', args=[shopping_list.id])
    data = {
        'name': 'Aceite'
    }
    # client = APIClient()
    response = client.post(url, data=data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'Aceite'
    assert response.data['purchased'] == False

@pytest.mark.django_db
def test_admin_can_add_shopping_items(create_user, create_authenticated_client, admin_client, create_shopping_list):
    # user = create_user()
    user = User.objects.get(username='admin')
    client = create_authenticated_client(user)
    shopping_list = create_shopping_list(user, name='Bicicletas')

    url = reverse('add-shopping-item', kwargs={'pk':shopping_list.id})
    data = {
        "name": "Giant",
    }
    
    response = client.post(url, data=data, format='json')     # admin_client is a fixture from pytest library
    print(response)

    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_create_shopping_item_missing_data_returns_bad_request(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user)
    shopping_list = create_shopping_list(user, name='Mercado')
    # shopping_list = ShoppingList.objects.create(name='Mercado')

    url = reverse('add-shopping-item', args=[shopping_list.id])
    data = {}
    # client = APIClient()
    response = client.post(url, data=data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
   

# RETRIEVE TEST
@pytest.mark.django_db
def test_shopping_item_is_retrieved_by_id(create_user, create_authenticated_client, create_shopping_item):
    user = create_user()
    client = create_authenticated_client(user)
    shopping_item = create_shopping_item(name='Arroz', user=user)

    url = reverse('shopping-item-detail', kwargs={'pk': shopping_item.shopping_list.id, 'item_pk': shopping_item.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Arroz'

@pytest.mark.django_db
def test_not_member_of_list_can_not_add_shopping_item(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    another_user = User.objects.create_user('Creator', 'creator@list.com', 'password')
    client = create_authenticated_client(user)
    shopping_list = create_shopping_list(another_user, 'Bicicletas')

    url = reverse('add-shopping-item', args=[shopping_list.id])
    data = {
        'name': 'Giant'
    }

    response = client.post(url, data=data, format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN


# UPDATE TEST
@pytest.mark.django_db
def test_change_shopping_item_purchased_status(create_user, create_authenticated_client, create_shopping_item):
    user = create_user()
    client = create_authenticated_client(user)
    shopping_item = create_shopping_item(user, name='Aceite')

    url = reverse('shopping-item-detail', kwargs={'pk': shopping_item.shopping_list.id, 'item_pk': shopping_item.id})
    data = {
        'name': 'Aceite',
        'purchased': True
    }
    # client = APIClient()
    response = client.put(url, data=data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert ShoppingItem.objects.get().purchased == True

@pytest.mark.django_db
def test_change_shopping_item_purchased_status_with_missing_data_returns_bad_request(create_user, create_authenticated_client, create_shopping_item):
    user = create_user()
    client = create_authenticated_client(user)
    shopping_item = create_shopping_item(user, name='Aceite')

    url = reverse('shopping-item-detail', kwargs={'pk': shopping_item.shopping_list.id, 'item_pk': shopping_item.id})
    data = {
        'purchased': True
    }
    # client = APIClient()
    response = client.put(url, data=data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_change_shopping_item_purchased_status_with_partial_update(create_user, create_authenticated_client, create_shopping_item):
    user = create_user()
    client = create_authenticated_client(user)
    shopping_item = create_shopping_item(user, name='Aceite')

    url = reverse('shopping-item-detail', kwargs={'pk': shopping_item.shopping_list.id, 'item_pk': shopping_item.id})
    data = {
        'purchased': True
    }
    # client = APIClient()
    response = client.patch(url, data=data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert ShoppingItem.objects.get().purchased == True
 

# DELETE TEST
@pytest.mark.django_db
def test_shopping_item_is_deleted(create_user, create_authenticated_client, create_shopping_item):
    user = create_user()
    client = create_authenticated_client(user)
    shopping_item = create_shopping_item(user, name='Aceite')

    url = reverse('shopping-item-detail', kwargs={'pk': shopping_item.shopping_list.id, 'item_pk': shopping_item.id})
    # client = APIClient()
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert ShoppingItem.objects.count() == 0