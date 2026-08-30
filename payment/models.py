from django.db import models

# Create your models here.

class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "PENDING"),
        ("completed", "COMPLETED"),
        ("failed", "FAILED"),
        ("cancelled", "CANCELLED"),
    ]

    invoice_number = models.CharField( max_length=100, unique=True)
    payment_id = models.CharField( max_length=200, blank=True, null=True, unique=True)
    trx_id = models.CharField( max_length=200, blank=True, null=True)
    currency = models.CharField( max_length=10, default= "BDT")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.invoice_number