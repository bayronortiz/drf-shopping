# Python imports
import pytest
import uuid


# Django imports
from django.urls import reverse

# DRF imports
from rest_framework import status
from rest_framework.test import APIClient

# Models imports
from shopping_list.models import ShoppingList, ShoppingItem


# CREATE TEST
@pytest.mark.django_db
def test_valid_shopping_item_is_created():
    shopping_list = ShoppingList.objects.create(name='Mercado')

    url = reverse('add-shopping-item', args=[shopping_list.id])
    data = {
        'name': 'Aceite'
    }
    client = APIClient()
    response = client.post(url, data=data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'Aceite'
    assert response.data['purchased'] == False

@pytest.mark.django_db
def test_create_shopping_item_missing_data_returns_bad_request():
    shopping_list = ShoppingList.objects.create(name='Mercado')

    url = reverse('add-shopping-item', args=[shopping_list.id])
    data = {}
    client = APIClient()
    response = client.post(url, data=data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
   

# RETRIEVE TEST
@pytest.mark.django_db
def test_shopping_item_is_retrieved_by_id(create_shopping_item):
    shopping_item = create_shopping_item(name='Aceite')

    url = reverse('shopping-item-detail', kwargs={'pk': shopping_item.shopping_list.id, 'item_pk': shopping_item.id})
    client = APIClient()
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Aceite'


# UPDATE TEST
@pytest.mark.django_db
def test_change_shopping_item_purchased_status(create_shopping_item):
    shopping_item = create_shopping_item(name='Aceite')

    url = reverse('shopping-item-detail', kwargs={'pk': shopping_item.shopping_list.id, 'item_pk': shopping_item.id})
    data = {
        'name': 'Aceite',
        'purchased': True
    }
    client = APIClient()
    response = client.put(url, data=data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert ShoppingItem.objects.get().purchased == True

@pytest.mark.django_db
def test_change_shopping_item_purchased_status_with_missing_data_returns_bad_request(create_shopping_item):
    shopping_item = create_shopping_item(name='Aceite')

    url = reverse('shopping-item-detail', kwargs={'pk': shopping_item.shopping_list.id, 'item_pk': shopping_item.id})
    data = {
        'purchased': True
    }
    client = APIClient()
    response = client.put(url, data=data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_change_shopping_item_purchased_status_with_partial_update(create_shopping_item):
    shopping_item = create_shopping_item(name='Aceite')

    url = reverse('shopping-item-detail', kwargs={'pk': shopping_item.shopping_list.id, 'item_pk': shopping_item.id})
    data = {
        'purchased': True
    }
    client = APIClient()
    response = client.patch(url, data=data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert ShoppingItem.objects.get().purchased == True
 

# DELETE TEST
@pytest.mark.django_db
def test_shopping_item_is_deleted(create_shopping_item):
    shopping_item = create_shopping_item(name='Aceite')

    url = reverse('shopping-item-detail', kwargs={'pk': shopping_item.shopping_list.id, 'item_pk': shopping_item.id})
    client = APIClient()
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert ShoppingItem.objects.count() == 0