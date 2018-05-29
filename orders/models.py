from django.db import models


class Phones(models.Model):
    phone = models.CharField('phone number', max_length=255, unique=True)


class Orders(models.Model):
    """  """
    phones = models.ManyToManyField(Phones, related_name='orders')
    data = models.CharField('data', max_length=1024)

    def __str__(self):
        return self.data
