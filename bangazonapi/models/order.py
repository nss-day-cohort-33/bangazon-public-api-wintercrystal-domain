"""Module for for Park Areas"""
from django.db import models


class ParkArea(models.Model):
    """Model class for ParkArea"""
    name = models.CharField(max_length=50)
    theme = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("parkarea")
        verbose_name_plural = ("parkareas")

    def __str__(self):
        return self.name

