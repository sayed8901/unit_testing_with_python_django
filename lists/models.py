from django.db import models


# Create your models here.
class Item(models.Model):
    text = models.TextField(default="")

    def __str__(self):
        return f'{self.id}. {self.text}'
