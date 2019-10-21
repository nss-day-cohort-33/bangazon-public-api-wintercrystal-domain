from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING,)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=55)


    @property
    def avg_rating(self):
        ratings =self.customer_rating.all()
        total_score = 0
        if len(ratings) > 0:
            for score in ratings:
                total_score += score.score
            total_score = +total_score/len(ratings)
        else:
            total_score = 0


        return total_score

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


    class Meta:
        verbose_name = ("customer")
        verbose_name_plural = ("customers")
