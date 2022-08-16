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
from shopping_list.tests.conftest import (
    create_authenticated_client, create_user, create_shopping_list, create_shopping_item
)


# CREATE TEST
@pytest.mark.django_db
def test_valid_shopping_list_is_created(create_user, create_authenticated_client):
    url = reverse('all-shopping-lists')
    data = {
        'name': 'Artistas'
    }
    # client = APIClient()    # Test sin autenticación
    client = create_authenticated_client(create_user())     # Test autenticación básica Django, aplicando fixtures
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert ShoppingList.objects.get().name == 'Artistas'

@pytest.mark.django_db
def test_shopping_list_name_missing_return_bad_request(create_user, create_authenticated_client):
    user = create_user()

    url = reverse('all-shopping-lists')
    data = {
        'none': 'Artistas'
    }
    client = create_authenticated_client(user)
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# LIST TESTS
@pytest.mark.django_db
def test_all_shopping_lists_are_listed(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user)
    create_shopping_list(user, 'Artistas')
    create_shopping_list(user, 'Música')
    
    url = reverse('all-shopping-lists')
    # ShoppingList.objects.create(name='Artistas')     # Test unauthenticated API
    # ShoppingList.objects.create(name='Música')        # Test unauthenticated API

    # client = APIClient()          # Test unauthenticated API
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]['name'] == 'Artistas'
    assert response.data[1]['name'] == 'Música'


# RETRIEVE TESTS
@pytest.mark.django_db
def test_shopping_list_is_retrieved_by_id(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user)
    shopping_list = create_shopping_list(user, name='Artistas')
    # shopping_list = ShoppingList.objects.create(name='Artistas')

    url = reverse('shopping-list-detail', args=[shopping_list.id])
    #client = APIClient()
    response = client.get(url, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Artistas'

@pytest.mark.django_db
def test_shopping_list_includes_only_corresponding_items(create_user, create_authenticated_client, create_shopping_list, create_shopping_item):
    user = create_user()
    client = create_authenticated_client(user)

    artistas_shopping_list = create_shopping_list(user, name='Artistas')
    musica_shopping_list = create_shopping_list(user, name='Música')
    # artistas_shopping_list = ShoppingList.objects.create(name='Artistas')
    # musica_shopping_list = ShoppingList.objects.create(name='Música')

    create_shopping_item(user, name='Kathia Buniatishvili', shopping_list=artistas_shopping_list)
    create_shopping_item(user, name='Mariam Kurasbediani', shopping_list=artistas_shopping_list)
    create_shopping_item(user, name='Clásica', shopping_list=musica_shopping_list)
    # ShoppingItem.objects.create(shopping_list=artistas_shopping_list, name='Kathia Buniatishvili')
    # ShoppingItem.objects.create(shopping_list=artistas_shopping_list, name='Mariam Kurasbediani')
    # ShoppingItem.objects.create(shopping_list=musica_shopping_list, name='Clásica')

    url = reverse('shopping-list-detail', args=[artistas_shopping_list.id])
    #client = APIClient()
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['shopping_items']) == 2
    assert response.data['shopping_items'][0]['name'] == 'Kathia Buniatishvili'
    assert response.data['shopping_items'][1]['name'] == 'Mariam Kurasbediani'


# UPDATE TESTS
@pytest.mark.django_db
def test_shopping_list_name_is_changed(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user)
    shopping_list = create_shopping_list(user, 'Música')
    # shopping_list = ShoppingList.objects.create(name='Música')

    url = reverse('shopping-list-detail', args=[shopping_list.id])
    data = {
        'name': 'Artistas'
    }
    # client = APIClient()
    response = client.put(url, data=data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Artistas'

@pytest.mark.django_db
def test_shopping_list_not_changed_because_name_missing(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user)
    shopping_list = create_shopping_list(user, 'Música')
    # shopping_list = ShoppingList.objects.create(name='Música')

    url = reverse('shopping-list-detail', args=[shopping_list.id])
    data = {
        'bad': 'Artistas'
    }
    # client = APIClient()
    response = client.put(url, data=data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_shopping_list_name_is_changed_with_partial_update(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user)
    shopping_list = create_shopping_list(user, 'Música')
    # shopping_list = ShoppingList.objects.create(name='Música')

    url = reverse('shopping-list-detail', args=[shopping_list.id])
    data = {
        'name': 'Artistas'
    }
    # client = APIClient()
    response = client.patch(url, data=data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Artistas'

@pytest.mark.django_db
def test_shopping_list_not_changed_because_name_missing_with_partial_update(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user)
    shopping_list = create_shopping_list(user, 'Música')
    # shopping_list = ShoppingList.objects.create(name='Música')

    url = reverse('shopping-list-detail', args=[shopping_list.id])
    data = {
        'bad': 'Artistas'
    }
    # client = APIClient()
    response = client.patch(url, data=data, format='json')

    assert response.status_code == status.HTTP_200_OK


# DELETE TESTS
@pytest.mark.django_db
def test_shopping_list_is_deleted(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user)
    shopping_list = create_shopping_list(user, 'Artistas')
    # shopping_list = ShoppingList.objects.create(name='Artistas')      # Unauthenticated test api

    url = reverse('shopping-list-detail', args=[shopping_list.id])
    # client = APIClient()   # Unauthenticated test api
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert ShoppingList.objects.count() == 0

@pytest.mark.django_db
def test_shopping_list_not_deleted_because_id_invalid(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user)
    shopping_list = create_shopping_list(user, 'Artistas')
    # shopping_list = ShoppingList.objects.create(name='Artistas')
    bad_shopping_list_id = uuid.uuid4()

    url = reverse('shopping-list-detail', args=[bad_shopping_list_id])
    # client = APIClient()
    response = client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert ShoppingList.objects.count() == 1    