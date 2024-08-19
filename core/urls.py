from django.contrib import admin
from django.urls import path
from .views import HomeView, CreateOrderView, ThanksView, PaymentsListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('orders/create/', CreateOrderView.as_view(), name='create_order'),
    path('orders/thanks/<int:order_id>/', ThanksView.as_view(), name='thanks_with_id'),
    path('orders/thanks/<int:order_id>/', ThanksView.as_view(), name='thanks'),
    path('payments/list/', PaymentsListView.as_view(), name='payments_list'),
]
