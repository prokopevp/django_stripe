from django.db import models

from simple_solutions_stripe.settings import STRIPE_SUPPORTED_CURRENCIES


class Item(models.Model):
    name = models.CharField(blank=False, null=False, max_length=200)
    description = models.TextField(null=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    currency = models.CharField(max_length=3, choices=STRIPE_SUPPORTED_CURRENCIES,
                                default=STRIPE_SUPPORTED_CURRENCIES[0][0], null=False)

    product_id = models.CharField(unique=True, max_length=128, null=False)
    price_id = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name} {self.currency.upper()} ({self.id})"


class Discount(models.Model):
    percent = models.PositiveIntegerField(null=False)
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(Discount, blank=True, null=True, on_delete=models.SET_NULL)
