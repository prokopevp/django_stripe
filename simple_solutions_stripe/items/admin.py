import stripe
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response

from items.forms import ItemForm, OrderForm, DiscountForm
from items.models import Item, Order, Discount
from services.stripe_backend import ItemStripeBackend


class ItemAdmin(admin.ModelAdmin):
    model = Item
    form = ItemForm
    readonly_fields = ('price_id', 'product_id')


    def save_model(self, request, obj, form, change):
        item_stripe_backend = ItemStripeBackend(obj)
        try:
            item_stripe_backend.modify_or_create()
            super().save_model(request, obj, form, change)
        except stripe.error.StripeError as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Ошибка при обращении к Stripe...')

    def delete_model(self, request, obj):
        item_stripe_backend = ItemStripeBackend(obj)
        try:
            item_stripe_backend.delete()
            super().delete_model(request, obj)
        except stripe.error.StripeError as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Ошибка при обращении к Stripe...')


class OrderAdmin(admin.ModelAdmin):
    model = Order
    form = OrderForm
    filter_horizontal = ('items', )


class DiscountAdmin(admin.ModelAdmin):
    model = Discount
    form = DiscountForm


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Discount, DiscountAdmin)
