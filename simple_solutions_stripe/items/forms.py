from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelForm

from items.models import Order, Item, Discount


class ItemForm(ModelForm):
    def clean_price(self):
        if self.cleaned_data['price'] < 0:
            raise ValidationError('Цена должна быть положительным числом!')
        return self.cleaned_data['price']

    def clean_currency(self):
        item_orders_with_wrong_currency = Order.objects.filter(
            Q(items__id=self.instance.id) & ~Q(items__currency=self.cleaned_data['currency'])
        ).count()
        if item_orders_with_wrong_currency:
            raise ValidationError(f'Невозможно изменить валюту пока товар находится в заказе...')

        return self.cleaned_data['currency']

    class Meta:
        model = Item
        fields = '__all__'

class OrderForm(ModelForm):
    def clean_items(self):
        currencies = []
        for item in self.cleaned_data['items']:
            currencies.append(item.currency)
        if len(currencies) > 1:
            raise ValidationError('Невозможно создать заказ с товарами в разных валютах!')
        return self.cleaned_data['items']

    class Meta:
        model = Order
        fields = '__all__'

class DiscountForm(ModelForm):
    def clean_percent(self):
        if 0 > self.cleaned_data['percent'] or self.cleaned_data['percent'] > 100:
            raise ValidationError('Процент скидки должен быть в промежутке [0..100]!')
        return self.cleaned_data['percent']

    class Meta:
        model = Discount
        fields = '__all__'