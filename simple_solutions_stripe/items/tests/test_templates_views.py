from django.test import TestCase
from django.urls import reverse

from items.models import Item, Order


class TemplatesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item = Item.objects.create(name='TestName', description='Test', price=100)
        cls.order = Order.objects.create()
        cls.order.items.add(cls.item)

    def test_not_found_templates(self):
        response = self.client.get(reverse('success-payment'))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('cancel-payment'))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('order', args=[99]))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('item', args=[99]))
        self.assertEqual(response.status_code, 404)

    def test_after_payment_templates(self):
        after_success_item_payment_response = self.client.get(reverse('success-payment')+f'?item=1')
        self.assertTemplateUsed(after_success_item_payment_response, 'success.html')
        after_cancel_item_payment_response = self.client.get(reverse('cancel-payment') + f'?item=1')
        self.assertTemplateUsed(after_cancel_item_payment_response, 'cancel.html')
        after_success_item_payment_response = self.client.get(reverse('success-payment') + f'?order=1')
        self.assertTemplateUsed(after_success_item_payment_response, 'success.html')
        after_cancel_item_payment_response = self.client.get(reverse('cancel-payment') + f'?order=1')
        self.assertTemplateUsed(after_cancel_item_payment_response, 'cancel.html')

    def test_item_template(self):
        response = self.client.get(reverse('item', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_order_template(self):
        response = self.client.get(reverse('order', args=[1]))
        self.assertEqual(response.status_code, 200)

