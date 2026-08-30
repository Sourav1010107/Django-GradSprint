from django.urls import path

from . import views

urlpatterns = [
    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "bkash/create/",
        views.bkash_create,
        name="bkash_create"
    ),

    path(
        "bkash/callback/",
        views.bkash_callback,
        name="bkash_callback"
    ),

    path(
        "success/",
        views.payment_success,
        name="payment_success"
    ),

    path(
        "failed/",
        views.payment_failed,
        name="payment_failed"
    ),
]
