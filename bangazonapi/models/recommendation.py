from django.db import models
from .customer import Customer
from .product import Product


class Recommendation(models.Model):

    customer = models.ForeignKey(Customer, related_name='recommendee', on_delete=models.DO_NOTHING,)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING,)
    # Recommender is creator of recommendation and the one who is doing the 'recommending'
    recommender = models.ForeignKey(Customer, on_delete=models.DO_NOTHING,)
    is_shown = models.BooleanField(default=False,)

    class Meta:
        verbose_name = ("recommendation")
        verbose_name_plural = ("recommendations")
