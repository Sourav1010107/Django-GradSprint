import requests

from django.conf import settings


class BkashAPIError(Exception):
    pass


def get_bkash_token():

    url = (
        f"{settings.BKASH_BASE_URL}"
        "/tokenized/checkout/token/grant"
    )

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "username": settings.BKASH_USERNAME,
        "password": settings.BKASH_PASSWORD,
    }

    payload = {
        "app_key": settings.BKASH_APP_KEY,
        "app_secret": settings.BKASH_APP_SECRET,
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        data = response.json()

    except requests.RequestException as error:
        raise BkashAPIError(
            f"Could not connect to bKash: {error}"
        )

    except ValueError:
        raise BkashAPIError(
            "bKash returned invalid JSON."
        )

    if not response.ok:
        raise BkashAPIError(
            f"Token request failed: {data}"
        )

    token = data.get("id_token")

    if not token:
        raise BkashAPIError(
            f"No id_token received: {data}"
        )

    return token


def create_bkash_payment(
    amount,
    invoice_number,
    payer_reference="01700000000"
):

    token = get_bkash_token()

    url = (
        f"{settings.BKASH_BASE_URL}"
        "/tokenized/checkout/create"
    )

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": token,
        "X-APP-Key": settings.BKASH_APP_KEY,
    }

    payload = {
        "mode": "0011",
        "payerReference": payer_reference,
        "callbackURL": settings.BKASH_CALLBACK_URL,
        "amount": str(amount),
        "currency": "BDT",
        "intent": "sale",
        "merchantInvoiceNumber": invoice_number,
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        data = response.json()

    except requests.RequestException as error:
        raise BkashAPIError(
            f"Create Payment connection error: {error}"
        )

    except ValueError:
        raise BkashAPIError(
            "Invalid Create Payment response."
        )

    if not response.ok:
        raise BkashAPIError(
            f"Create Payment failed: {data}"
        )

    return data


def execute_bkash_payment(payment_id):

    token = get_bkash_token()

    url = (
        f"{settings.BKASH_BASE_URL}"
        "/tokenized/checkout/execute"
    )

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": token,
        "X-APP-Key": settings.BKASH_APP_KEY,
    }

    payload = {
        "paymentID": payment_id
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        data = response.json()

    except requests.RequestException as error:
        raise BkashAPIError(
            f"Execute Payment connection error: {error}"
        )

    except ValueError:
        raise BkashAPIError(
            "Invalid Execute Payment response."
        )

    if not response.ok:
        raise BkashAPIError(
            f"Execute Payment failed: {data}"
        )

    return data