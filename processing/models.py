from django.db import models

from farm.models import Farm, Picture

class ProcessedData(models.Model):

    class Meta:
        verbose_name = 'Processed Data'
        verbose_name_plural = 'Processed Data'

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    ndvi = models.ImageField(upload_to='processed_shots/NDVI', blank=True)
    ndre = models.ImageField(upload_to='processed_shots/NDRE', blank=True)
    grvi = models.ImageField(upload_to='processed_shots/GRVI', blank=True)
    gci = models.ImageField(upload_to='processed_shots/GCI', blank=True)
    processed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.processed_on}'
