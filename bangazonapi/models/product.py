from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .customer import Customer
from .productcategory import ProductCategory
from .image import Image

class Product(models.Model):

    name = models.CharField(max_length=50,)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING,)
    price = models.FloatField(validators=[MinValueValidator(0.00), MaxValueValidator(10000.00)],)
    description = models.CharField(max_length=255,)
    quantity = models.IntegerField(validators=[MinValueValidator(0)],)
    created_date = models.DateField(default="0000-00-00",)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING,)
    location = models.CharField(max_length=50,)
    image = models.ImageField(upload_to='product_imgs/', height_field=None, width_field=None, max_length=None, null=True)


    class Meta:
        verbose_name = ("product")
        verbose_name_plural = ("products")
