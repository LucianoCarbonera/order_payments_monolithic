from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Order, Payment
from decimal import Decimal, InvalidOperation

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class CreateOrderView(View):
    def get(self, request):
        return render(request, 'order_form.html')

    def post(self, request):
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        if not product_name or not quantity or not price:
            return render(request, 'order_form.html', {'error_message': 'Por favor, preencha todos os campos.'})

        try:
            quantity = int(quantity)
            price = Decimal(price)
        except (ValueError, InvalidOperation):
            return render(request, 'order_form.html', {'error_message': 'Por favor, insira valores válidos.'})

        # Cria o pedido
        order = Order.objects.create(product_name=product_name, quantity=quantity, price=price)

        # Processa o pagamento associado ao pedido
        payment = Payment.objects.create(order=order, amount=order.total_price)
        payment.process_payment()

        # Redireciona para a página de agradecimento
        return redirect('thanks', order_id=order.id)

class ThanksView(View):
    def get(self, request, order_id=None):
        orders = Order.objects.all()
        selected_order = get_object_or_404(Order, pk=order_id) if order_id else None

        return render(request, 'thanks.html', {
            'orders': orders,
            'selected_order': selected_order,
        })

    def post(self, request, order_id=None):
        order_id = request.POST.get('order_id')
        if order_id:
            return redirect('thanks_with_id', order_id=order_id)
        return self.get(request)

class PaymentsListView(View):
    def get(self, request):
        payments = Payment.objects.all()
        return render(request, 'payments_list.html', {'payments': payments})
