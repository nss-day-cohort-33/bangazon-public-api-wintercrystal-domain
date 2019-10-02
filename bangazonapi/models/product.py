from django.db import models
from .parkarea import ParkArea

class Attraction(models.Model):

    name = models.CharField(max_length=50)
    area = models.ForeignKey(ParkArea, on_delete=models.DO_NOTHING, related_name="attractions")

    class Meta:
        verbose_name = ("attraction")
        verbose_name_plural = ("attractions")

    def __str__(self):
        return self.name

