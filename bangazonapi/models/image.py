from django.db import models


class Image(models.Model):

    product_pic = models.ImageField(upload_to='product_imgs/', height_field=None, width_field=None, max_length=None)

    class Meta:
        verbose_name = ("image")
        verbose_name_plural = ("images")
