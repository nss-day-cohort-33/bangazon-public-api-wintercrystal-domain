
from django.db import models
from .customer import Customer
from .payment import Payment

'''
auther: Dustin Hobson
purpose: Class model for favorites which evey favorite instance will inherit.
methods: all
'''


class Favorite(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='favorites', null=True)
    seller = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, null=True)




    class Meta:
        verbose_name = ("favorite")
        verbose_name_plural = ("favorites")