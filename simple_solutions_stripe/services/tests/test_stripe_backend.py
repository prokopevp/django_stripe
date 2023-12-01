from unittest.mock import Mock

from django.test import TestCase
from unittest import mock

from items.models import Item
from services.stripe_backend import ItemStripeBackend

from services import stripe_backend


class ItemFormTest(TestCase):
    def setUp(self):
        self.item = Item(
            name='TestName',
            description='Test',
            price=100,
            currency='eur',
            product_id='123',
            price_id='1234'
        )

    @mock.patch('stripe.Product.create')
    def test_stripe_backend_changing_item_on_product_create(self, mock_stripe_product_create):
        mock_stripe_product_create.return_value = dict(id='product id', default_price='price id')

        item_stripe_backend = ItemStripeBackend(self.item)
        item_stripe_backend.create_product()

        self.assertEqual(self.item.product_id, 'product id')
        self.assertEqual(self.item.price_id, 'price id')

    def test_stripe_backend_change_item_price_id_on_price_change(self):
        """
        Тест на создание новой цены в stripe при изменении в БД
        :return:
        """
        with mock.patch('stripe.Price.retrieve') as mock_stripe_retrieve, \
                mock.patch('stripe.Price.create') as mock_stripe_price_create:
            mock_retrieved_price = Mock()
            mock_retrieved_price.currency = 'eur'
            mock_retrieved_price.unit_amount = 200
            mock_stripe_retrieve.return_value = mock_retrieved_price
            mock_stripe_price_create.return_value = dict(id='test')

            item_stripe_backend = stripe_backend.ItemStripeBackend(self.item)
            price_to_archive = item_stripe_backend.modify_price_id()
        self.assertEqual(price_to_archive, '1234')
        self.assertEqual(self.item.price, 100)
        self.assertEqual(self.item.price_id, 'test')

    def test_stripe_backend_change_item_price_id_on_currency_change(self):
        """
        Тест на создание новой цены в stripe при изменении валюты в БД
        :return:
        """
        with mock.patch('stripe.Price.retrieve') as mock_stripe_retrieve, \
                mock.patch('stripe.Price.create') as mock_stripe_price_create:
            mock_retrieved_price = Mock()
            mock_retrieved_price.currency = 'cny'
            mock_retrieved_price.unit_amount = 100
            mock_stripe_retrieve.return_value = mock_retrieved_price
            mock_stripe_price_create.return_value = dict(id='test')

            item_stripe_backend = stripe_backend.ItemStripeBackend(self.item)
            price_to_archive = item_stripe_backend.modify_price_id()
        self.assertEqual(price_to_archive, '1234')
        self.assertEqual(self.item.currency, 'eur')
        self.assertEqual(self.item.price_id, 'test')

