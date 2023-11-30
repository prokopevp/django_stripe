from django.http import HttpResponseNotFound
from django.urls import reverse
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from items.models import Item, Order
from services.stripe_ import OrderStripeBackend, ItemStripeBackend
from simple_solutions_stripe.settings import STRIPE_PUBLISH_KEY


class AfterPaymentPage(APIView):
    def get(self, request: Request):
        item_id = request.query_params.get('item')
        order_id = request.query_params.get('order')
        if item_id:
            uri = request.build_absolute_uri(reverse('item', args=[int(item_id)]))
        elif order_id:
            uri = request.build_absolute_uri(reverse('order', args=[order_id]))
        else:
            return HttpResponseNotFound()
        return Response(dict(item_uri=uri))



class SuccessPage(AfterPaymentPage):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'success.html'


class CancelPage(AfterPaymentPage):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cancel.html'


class ItemPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'item.html'

    def get(self, request: Request, id: str):
        item = get_object_or_404(Item, id=id)
        return Response(dict(item=item, stripe_publish_key=STRIPE_PUBLISH_KEY))


class OrderPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'order.html'

    def get(self, request: Request, pk: int):
        order = get_object_or_404(Order, pk=pk)
        order_price = sum([item.price for item in order.items.all()])
        currency = order.items.first().currency
        return Response(dict(order_price=order_price, currency=currency, order=order, stripe_publish_key=STRIPE_PUBLISH_KEY))


class BuyOrder(APIView):
    def get(self, request: Request, id: int):
        order = get_object_or_404(Order, pk=id)

        order_stripe_backend = OrderStripeBackend(order)
        session_id = order_stripe_backend.create_checkout_session(
            request.build_absolute_uri(reverse('success-payment') + f'?order={order.id}'),
            request.build_absolute_uri(reverse('cancel-payment') + f'?order={order.id}')
        )

        return Response(dict(session_id=session_id))


class BuyItem(APIView):
    def get(self, request: Request, id: str):
        item = get_object_or_404(Item, id=id)

        item_stripe_backend = ItemStripeBackend(item)
        session_id = item_stripe_backend.create_checkout_session(
            request.build_absolute_uri(reverse('success-payment') + f'?item={item.id}'),
            request.build_absolute_uri(reverse('cancel-payment') + f'?item={item.id}')
        )

        return Response(dict(session_id=session_id))
