from django.test import TestCase

from items.forms import ItemForm, OrderForm, DiscountForm
from items.models import Item, Order, Discount


class ItemFormTest(TestCase):
    def setUp(self):
        self.valid_rub_data = dict(
            price=1,
            name='a',
            description='b',
            product_id='qwe',
            price_id='ty',
            currency='rub'
        )
        self.eur_item = Item.objects.create(
            name='TestName',
            description='Test',
            price=100,
            currency='eur',
            product_id='123',
            price_id='1234'
        )
        self.eur_order = Order.objects.create()

    def test_valid_form(self):
        form = ItemForm(self.valid_rub_data)
        self.assertTrue(form.is_valid())

    def test_invalid_price(self):
        self.valid_rub_data['price'] = -1
        form = ItemForm(self.valid_rub_data)
        self.assertFalse(form.is_valid())

        self.valid_rub_data['price'] = 10000000000000000
        form = ItemForm(self.valid_rub_data)
        self.assertFalse(form.is_valid())

    def test_changing_item_currency_while_item_in_order(self):
        self.eur_order.items.add(self.eur_item)
        form = ItemForm(self.valid_rub_data, instance=self.eur_item)
        self.assertFalse(form.is_valid())


class OrderFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.eur_item = Item.objects.create(
            name='TestName',
            description='Test',
            price=100,
            currency='eur',
            product_id='123',
            price_id='1234'
        )
        cls.rub_item = Item.objects.create(
            name='TestName',
            description='Test',
            price=100,
            currency='rub',
            product_id='123',
            price_id='1234'
        )
        cls.another_rub_item = Item.objects.create(
            name='AnotherTestName',
            description='Test',
            price=100,
            currency='rub',
            product_id='123',
            price_id='1234'
        )
        cls.discount = Discount.objects.create(percent=70, name='Test')
        cls.eur_order = Order.objects.create()

    def test_valid_order_form(self):
        form = OrderForm(dict(
            items=[self.rub_item, self.another_rub_item],
            discount=self.discount
        ))
        self.assertTrue(form.is_valid())

    def test_invalid_different_currencies_order(self):
        form = OrderForm(dict(items=[self.eur_item, self.rub_item]))
        self.assertFalse(form.is_valid())


class DiscountFormTest(TestCase):
    def setUp(self):
        self.valid_data = dict(name='qwe', percent=50)

    def test_valid_form(self):
        form = DiscountForm(self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_discount_percent(self):
        self.valid_data['percent'] = -1
        form = DiscountForm(self.valid_data)
        self.assertFalse(form.is_valid())

        self.valid_data['percent'] = 200
        form = DiscountForm(self.valid_data)
        self.assertFalse(form.is_valid())

