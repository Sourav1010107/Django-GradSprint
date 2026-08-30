import uuid

from decimal import Decimal

from django.contrib import messages

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .models import Payment

from .services import (
    BkashAPIError,
    create_bkash_payment,
    execute_bkash_payment,
)


def checkout(request):

    return render(
        request,
        "payments/checkout.html"
    )


def bkash_create(request):

    if request.method != "POST":
        return redirect("checkout")

    amount = Decimal("999.00")

    invoice_number = (
        "GRE-"
        + uuid.uuid4().hex[:12].upper()
    )

    payment = Payment.objects.create(
        invoice_number=invoice_number,
        amount=amount,
        status="PENDING"
    )

    try:

        result = create_bkash_payment(
            amount=amount,
            invoice_number=invoice_number,
        )

    except BkashAPIError as error:

        payment.status = "FAILED"
        payment.save()

        messages.error(
            request,
            str(error)
        )

        return redirect("payment_failed")

    payment_id = result.get("paymentID")
    bkash_url = result.get("bkashURL")

    if not payment_id or not bkash_url:

        payment.status = "FAILED"
        payment.save()

        messages.error(
            request,
            f"Invalid bKash response: {result}"
        )

        return redirect("payment_failed")

    payment.payment_id = payment_id
    payment.save()

    return redirect(bkash_url)


def bkash_callback(request):

    payment_id = request.GET.get("paymentID")
    status = request.GET.get("status")

    if not payment_id:

        messages.error(
            request,
            "Payment ID was not provided."
        )

        return redirect("payment_failed")

    payment = get_object_or_404(
        Payment,
        payment_id=payment_id
    )

    if status == "cancel":

        payment.status = "CANCELLED"
        payment.save()

        return redirect("payment_cancelled")

    if status != "success":

        payment.status = "FAILED"
        payment.save()

        return redirect("payment_failed")

    try:

        result = execute_bkash_payment(
            payment_id
        )

    except BkashAPIError as error:

        payment.status = "FAILED"
        payment.save()

        messages.error(
            request,
            str(error)
        )

        return redirect("payment_failed")

    transaction_status = result.get(
        "transactionStatus"
    )

    trx_id = result.get("trxID")

    if transaction_status == "Completed":

        payment.status = "COMPLETED"
        payment.trx_id = trx_id
        payment.save()

        request.session[
            "successful_payment_id"
        ] = payment.id

        return redirect("payment_success")

    payment.status = "FAILED"
    payment.save()

    messages.error(
        request,
        f"Payment was not completed: {result}"
    )

    return redirect("payment_failed")


def payment_success(request):

    payment_id = request.session.get(
        "successful_payment_id"
    )

    payment = None

    if payment_id:

        payment = Payment.objects.filter(
            id=payment_id,
            status="COMPLETED"
        ).first()

    return render(
        request,
        "payments/success.html",
        {
            "payment": payment
        }
    )


def payment_failed(request):

    return render(
        request,
        "payments/failed.html"
    )


def payment_cancelled(request):

    return render(
        request,
        "payments/cancelled.html"
    )