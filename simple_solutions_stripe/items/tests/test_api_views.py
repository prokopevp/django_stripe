import json
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from items.models import Item, Order


class BuyItemAndBuyOrderTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item = Item.objects.create(name='TestName', description='Test', price=100)
        cls.order = Order.objects.create()
        cls.order.items.add(cls.item)

    def check_session_id_in_response_json(self, response):
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIsInstance(data, dict)
        self.assertIn('session_id', data)

    @mock.patch('services.stripe_backend.ItemStripeBackend.create_checkout_session')
    def test_buy_item_view(self, mock_create_item_session):
        mock_create_item_session.return_value = 'mock-session-id'
        response = self.client.get(reverse('buy-item', args=[self.item.id]))
        self.check_session_id_in_response_json(response)

    @mock.patch('services.stripe_backend.OrderStripeBackend.create_checkout_session')
    def test_buy_order_view(self, mock_create_order_session):
        mock_create_order_session.return_value = 'mock-session-id'
        response = self.client.get(reverse('buy-order', args=[self.item.id]))
        self.check_session_id_in_response_json(response)

    def test_not_found_item_to_buy(self):
        response = self.client.get(reverse('buy-item', args=[99]))
        self.assertEqual(response.status_code, 404)

    def test_not_found_order_to_buy(self):
        response = self.client.get(reverse('buy-order', args=[99]))
        self.assertEqual(response.status_code, 404)