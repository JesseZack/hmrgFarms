
# Create your models here.
from django.contrib.gis.db import models

from crops.models import Variety
from users.models import FarmSponsor


class Site(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    location = models.PointField()
    size = models.IntegerField(help_text='Size in square-meters')

    def __str__(self):
        return f'{self.name} {self.town}'


class FarmOrder(models.Model):
    sponsor = models.ForeignKey(FarmSponsor, on_delete=models.PROTECT)
    variety = models.ForeignKey(Variety, on_delete=models.PROTECT)
    size = models.IntegerField(help_text='Size in square-meters')


class Farm(models.Model):
    name = models.CharField(max_length=50)
    order = models.ForeignKey(FarmOrder, on_delete=models.PROTECT)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    size = models.IntegerField(help_text='Size in square-meters')
    start_date = models.DateField()
    status = models.IntegerField(choices=(
        (1, 'Processing'),
        (2, 'Land Preparation'),
        (3, 'Nursery'),
        (4, 'Growing and Maintenance'),
        (5, 'Harvesting'),
        (6, 'Complete')
    ), default=1)
    harvested = models.BooleanField(default=False)
    first_harvest_date = models.DateField(null=True, blank=True)
    last_harvest_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.order.sponsor.user_acc.first_name}'

    class Meta:
        verbose_name = 'Farm'
        verbose_name_plural = 'Farms'
