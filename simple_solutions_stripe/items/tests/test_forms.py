from django.core.exceptions import ValidationError
from django.test import TestCase

from items.forms import ItemForm, OrderForm, DiscountForm
from items.models import Item, Order


class ItemFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.eur_item = Item.objects.create(
            name='TestName',
            description='Test',
            price=100,
            currency='eur'
        )
        cls.eur_order = Order.objects.create()
        cls.eur_order.items.add(cls.eur_item)

    def setUp(self):
        self.clean_data = dict(
            price=1,
            name='a',
            description='b',
            product_id='qwe',
            price_id='ty',
            currency='rub'
        )

    def test_wrong_price(self):
        self.clean_data['price'] = -1
        form = ItemForm(self.clean_data)
        self.assertFalse(form.is_valid())

        self.clean_data['price'] = 10000000000000000
        form = ItemForm(self.clean_data)
        self.assertFalse(form.is_valid())

    def test_changing_item_currency_while_item_in_order(self):
        data = self.clean_data.copy()
        rub_form = ItemForm(data, instance=self.eur_item)
        self.assertFalse(rub_form.is_valid())


class OrderFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.eur_item = Item.objects.create(
            name='TestName',
            description='Test',
            price=100,
            currency='eur',
            product_id='123'
        )
        cls.rub_item = Item.objects.create(
            name='TestName',
            description='Test',
            price=100,
            currency='eur'
        )
        cls.eur_order = Order.objects.create()
        cls.eur_order.items.add(cls.eur_item)
        cls.eur_order.save()

    def test_multivalue_order(self):
        form = OrderForm(data=dict(items=[self.eur_item, self.rub_item]))
        self.assertFalse(form.is_valid())


class DiscountFormTest(TestCase):
    def setUp(self):
        self.form_data = dict(name='qwe', percent=50)

    def test_discount_percent(self):
        self.form_data['percent'] = -1
        form = DiscountForm(self.form_data)
        self.assertFalse(form.is_valid())

        self.form_data['percent'] = 200
        form = DiscountForm(self.form_data)
        self.assertFalse(form.is_valid())

