from django.contrib import admin
from django.urls import path, re_path

from items import views

urlpatterns = [
    path('item/<str:id>/', views.ItemPage.as_view(), name='item'),
    path('buy/order/<str:id>/', views.BuyOrder.as_view(), name='buy-order'),
    path('order/<int:pk>/', views.OrderPage.as_view(), name='order'),
    path('buy/<str:id>/', views.BuyItem.as_view(), name='buy-item'),
    path('success/', views.SuccessPage.as_view(), name='success-payment'),
    path('cancel/', views.CancelPage.as_view(), name='cancel-payment')
]