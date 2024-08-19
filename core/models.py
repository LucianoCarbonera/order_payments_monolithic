from django.db import models
import uuid
import time
from decimal import Decimal

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pendente'),
        ('COMPLETED', 'Concluído'),
        ('CANCELLED', 'Cancelado'),
    )

    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido {self.pk} - {self.product_name}"

    @property
    def total_price(self):
        return self.quantity * self.price

    def mark_as_completed(self):
        """Marcar o pedido como concluído."""
        self.status = 'COMPLETED'
        self.save()

class Payment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pendente'),
        ('COMPLETED', 'Completo'),
        ('FAILED', 'Falhou'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pagamento {self.transaction_id} - Pedido {self.order.pk}"

    def process_payment(self):
        """Simula o processamento do pagamento."""
        time.sleep(10)

        # Marcar pagamento como completo
        self.status = 'COMPLETED'
        self.save()
        # Atualiza o status do pedido associado
        self.order.mark_as_completed()
