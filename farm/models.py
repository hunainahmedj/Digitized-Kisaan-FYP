from django.db import models
from django.urls import reverse


class Country(models.Model):

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    country = models.CharField(max_length=120, blank=False, null=False)

    def __str__(self):
        return f'{self.country}'


class Farm(models.Model):

    farm_lookup = models.CharField(max_length=120, blank=True, null=True)
    farm_name = models.CharField(max_length=120, blank=False, null=False)
    farm_area = models.FloatField(blank=False, null=False)
    farm_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    farm_created_on = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('farm-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.farm_name}'


class Coordinates(models.Model):

    class Meta:
        verbose_name = 'Coordinate'
        verbose_name_plural = 'Coordinates'

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    longitude = models.CharField(max_length=120)
    latitude = models.CharField(max_length=120)

    def __str__(self):
        return f'Longitude: {self.longitude}, Latitude: {self.latitude}'


class Picture(models.Model):

    farm_id = models.ForeignKey(Farm, on_delete=models.CASCADE)
    resource_GRE = models.ImageField(upload_to='arial_shots/GRE', blank=False)
    resource_NIR = models.ImageField(upload_to='arial_shots/NIR', blank=False)
    resource_RED = models.ImageField(upload_to='arial_shots/RED', blank=False)
    resource_REG = models.ImageField(upload_to='arial_shots/REG', blank=False)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.uploaded_on}'

    def get_absolute_url(self):
        return reverse('farm-detail', kwargs={'pk': self.farm_id.id})

