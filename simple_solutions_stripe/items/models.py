import stripe
from django.db import models

from simple_solutions_stripe.settings import STRIPE_PRIVATE_KEY, STRIPE_SUPPORTED_CURRENCIES

stripe.api_key = STRIPE_PRIVATE_KEY


class Item(models.Model):
    name = models.CharField(blank=False, null=False, max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3, choices=STRIPE_SUPPORTED_CURRENCIES,
                                default=STRIPE_SUPPORTED_CURRENCIES[0][0])

    product_id = models.CharField(unique=True, max_length=128)
    price_id = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name} {self.currency.upper()} ({self.id})"


class Discount(models.Model):
    percent = models.PositiveIntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(Discount, blank=True, null=True, on_delete=models.SET_NULL)
