# Python imports
import uuid

# Django imports
from django.db import models


class ShoppingItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return self.name