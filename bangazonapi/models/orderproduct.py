from django.db import models

class OrderProduct(models.Model):

    order = models.ForeignKey("Order", on_delete=models.DO_NOTHING, related_name="invoiceline")
    product = models.ForeignKey("Product", on_delete=models.DO_NOTHING, related_name="item")
    quantity = models.IntegerField()

    class Meta:
        verbose_name = ("orderproduct")
        verbose_name_plural = ("orderproducts")
