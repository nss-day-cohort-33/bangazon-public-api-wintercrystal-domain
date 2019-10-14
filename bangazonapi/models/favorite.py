
from django.db import models
from .customer import Customer
from .payment import Payment

'''
auther: Dustin Hobson
purpose: Class model for favorites which evey favorite instance will inherit.
methods: all
'''


class Favorite(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='user', null=True)
    seller = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='seller', null=True)




    class Meta:
        verbose_name = ("favorite")
        verbose_name_plural = ("favorites")