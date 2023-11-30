from django.contrib import admin

from items.forms import ItemForm, OrderForm, DiscountForm
from items.models import Item, Order, Discount
from services.stripe_ import ItemStripeBackend


class ItemAdmin(admin.ModelAdmin):
    model = Item
    form = ItemForm
    readonly_fields = ('price_id', 'product_id')

    def save_model(self, request, obj, form, change):
        item_stripe_backend = ItemStripeBackend(obj)
        item_stripe_backend.modify_or_create()
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        item_stripe_backend = ItemStripeBackend(obj)
        item_stripe_backend.delete()
        super().delete_model(request, obj)


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
