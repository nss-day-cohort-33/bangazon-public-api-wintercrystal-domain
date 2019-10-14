from django.db import models
from .customer import Customer
from .payment import Payment
from .product import Product

'''
auther: Dustin Hobson
purpose: Class model for a user's product preference which evey product preference instance will inherit.
methods: all
'''


class CustomerProductPreference(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.DO_NOTHING,)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING,)
    like = models.BooleanField(default = True )





    class Meta:
        verbose_name = ("customerproductpreference")
        verbose_name_plural = ("customerproductpreferences")