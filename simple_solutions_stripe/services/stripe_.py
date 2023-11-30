import stripe

from items.models import Item, Order
from simple_solutions_stripe import settings

stripe.api_key = settings.STRIPE_PRIVATE_KEY


class ItemStripeBackend:
    def __init__(self, item: Item):
        self.item = item

    def create_product(self) -> None:
        """
        Создает Stripe.Product вместе с ценой
        """
        default_price_data = dict(
            unit_amount=int(self.item.price * 100),
            currency=self.item.currency
        )
        product = stripe.Product.create(
            default_price_data=default_price_data,
            name=self.item.name,
            description=self.item.description
        )
        self.item.product_id = product['id']
        self.item.price_id = product['default_price']

    def modify_price_id(self) -> None | str:
        """
        Изменение price_id модели на основе price модели.
        Особенность Stripe - надо создать новую цену, а старую архивировать
        :return: price_id для архивации
        """
        old_price_data = stripe.Price.retrieve(self.item.price_id)
        price_to_archive = None

        if old_price_data.currency != self.item.currency or old_price_data.unit_amount != int(self.item.price * 100):
            price_to_archive = self.item.price_id
            new_price_data = stripe.Price.create(
                product=self.item.product_id,
                currency=self.item.currency,
                unit_amount=int(self.item.price * 100)
            )
            self.item.price_id = new_price_data['id']

        return price_to_archive

    def modify_product(self) -> None:
        """
        Изменение Stripe.Product+Stripe.Price
        :return:
        """
        price_to_archive = self.modify_price_id()
        stripe.Product.modify(
            self.item.product_id,
            default_price=self.item.price_id,
            name=self.item.name,
            description=self.item.description
        )
        if price_to_archive is not None:
            self.archive_price_id(price_to_archive)

    def archive_price_id(self, price_id: str):
        stripe.Price.modify(price_id, active=False)

    def modify_or_create(self):
        """
        Изменение или создание Stripe.Product+Stripe.Price.
        :return:
        """
        if self.item.id is None:
            self.create_product()
        else:
            self.modify_product()

    def delete(self):
        """
        Удаление сопутствующих объектов Stripe
        :return:
        """
        stripe.Product.modify(self.item.product_id, active=False)
        stripe.Price.modify(self.item.price_id, active=False)

    def create_checkout_session(self, success_url: str, cancel_url: str) -> str:
        """

        :param success_url: Для редиректа при удачной оплате
        :param cancel_url: При неудачном
        :return: id сессии
        """
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            currency=self.item.currency,
            success_url=success_url,
            cancel_url=cancel_url,
            line_items=[
                dict(price=self.item.price_id, quantity=1)
            ]
        )

        return session['id']


class OrderStripeBackend:
    def __init__(self, order: Order):
        self.order = order

    def create_discount_coupon(self) -> dict:
        """
        Создание одноразового купона на скидку.
        :return: Купон
        """
        coupon = stripe.Coupon.create(
            percent_off=self.order.discount.percent,
            name=self.order.discount.name,
            duration='once'
        )
        return coupon

    def create_checkout_session(self, success_url: str, cancel_url: str) -> str:
        """
        :param success_url: Для редиректа при удачной оплате
        :param cancel_url: При неудачном
        :return: id сессии
        """
        coupon = self.create_discount_coupon() if self.order.discount else None
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            discounts=[dict(coupon=coupon)],
            success_url=success_url,
            cancel_url=cancel_url,
            currency=self.order.items.first().currency,
            line_items=[dict(price=item.price_id, quantity=1) for item in self.order.items.all()]
        )

        return checkout_session['id']
