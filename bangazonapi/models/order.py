"""Module for for Park Areas"""
from django.db import models
from .customer import Customer
from .payment import Payment


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="customerorders")
    payment_type = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, null=True)
    created_date = models.DateField(default="0000-00-00",)



    class Meta:
        verbose_name = ("order")
        verbose_name_plural = ("orders")

