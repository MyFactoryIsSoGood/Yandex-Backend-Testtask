from django.db import models
from simple_history.models import HistoricalRecords


class ShopUnitType(models.TextChoices):
    OFFER = 'OFFER'
    CATEGORY = 'CATEGORY'


class ShopUnit(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField(verbose_name='Имя')
    date = models.DateTimeField(verbose_name='Время последнего обновления', null=True, blank=True)
    type = models.CharField(max_length=8, choices=ShopUnitType.choices, verbose_name='Тип')
    price = models.IntegerField(null=True, blank=True, verbose_name='Цена')
    parentId = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    stats = HistoricalRecords(cascade_delete_history=True)  # django-simple-history
