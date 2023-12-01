# Django + Stripe API Backend

**Стек:** Django, Gunicorn, Postgres, Nginx, Docker

#### Запуск
1) Рядом с .env (есть example.env в репозитории) и nginx.conf:
```
docker-compose.up
```
2) Создание админа:
```
docker exec -it django_stripe-dj-1
python3 manage.py createsuperuser
```
### API
`GET /item/<int:id> Страница товара`

`GET /order/<int:id> Страница Заказа`

`GET /buy/<int:id> Получение токена Checkout Session ID для товара`

`GET /buy/order/<int:id> Получение токена Checkout Session ID для заказа`

### Коментарии
- Присутствуют unit-тесты.
- Работа с Stripe выделена в сервис `services/stripe_backend`
- Изменение и создание Item в админке отображается в Stripe.
- При создании/изменении товара указывается валюта, что тоже отображается в Stripe.
- Присутствует модель Order (заказ), который формируется из товаров в админке и где к нему можно прикрепить Discount.
- Создание заказа возможно только для товаров одной валюты, изменение валюты товара находящегося в заказе с другими товарами отклоняется.