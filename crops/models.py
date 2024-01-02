from django.db import models


# Create your models here.
class Species(models.Model):
    common_name = models.CharField(max_length=50)
    scientific_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.common_name}'


class SubSpecies(models.Model):
    super_species = models.ForeignKey(Species, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} - {self.super_species.common_name}'

    class Meta:
        verbose_name_plural = 'Sub-Species'
        unique_together = ('super_species', 'name')


class Variety(models.Model):
    sub_species = models.ForeignKey(SubSpecies, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Varieties'


class ReproductivePart(models.Model):
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    unit_of_measure = models.IntegerField(choices=(
        (1, 'grams'),
        (2, 'ounces')
    ))

    def __str__(self):
        return f'{self.variety.name} {self.weight}'

    class Meta:
        unique_together = ('variety', 'weight', 'unit_of_measure')


class ReproductivePartPricing(models.Model):
    seeds = models.ForeignKey(ReproductivePart, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    pricing_date = models.DateField()

    def __str__(self):
        return f'{self.seeds.variety.name} {self.price}'
