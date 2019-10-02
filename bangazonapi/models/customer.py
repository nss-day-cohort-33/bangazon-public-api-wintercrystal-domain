from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    family_members = models.IntegerField()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        ordering = (F('user.date_joined').asc(nulls_last=True),)
