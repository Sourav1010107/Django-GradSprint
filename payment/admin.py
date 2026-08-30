from django.contrib import admin

# Register your models here.
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "invoice_number",
        "amount",
        "payment_id",
        "trx_id",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "invoice_number",
        "payment_id",
        "trx_id",
    )