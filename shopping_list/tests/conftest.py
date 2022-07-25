# Python imports
import pytest

# Models imports
from shopping_list.models import ShoppingItem, ShoppingList


@pytest.fixture(scope='session')
def create_shopping_item():     # Clousure
    def _create_shopping_item(name):
        shopping_list = ShoppingList.objects.create(name='Mercado')
        shopping_item = ShoppingItem.objects.create(name=name, shopping_list=shopping_list)

        return shopping_item

    return _create_shopping_item