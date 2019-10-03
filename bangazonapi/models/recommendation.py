from django.db import models
from .customer import Customer
from .product import Product


class Recommendation(models.Model):

    customer = models.ForeignKey(Customer, related_name='customer', on_delete=models.DO_NOTHING,)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING,)
    recommender = models.ForeignKey(Customer, related_name='recommender', on_delete=models.DO_NOTHING,)
    is_shown = models.BooleanField(default=False,)

    class Meta:
        verbose_name = ("Recommendation")
        verbose_name_plural = ("Recommendations")
