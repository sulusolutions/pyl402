import pytest
import httpx
from httpx import Response
from unittest.mock import patch

from pyl402.wallet.alby import AlbyWallet, PaymentResult

def custom_response(request):
    # Mock different responses based on the request URL or headers
    if request.url.path == "/payments/bolt11":
        if 'Bad Request' in request.headers.get('Authorization', ''):
            return httpx.Response(status_code=400, json={'detail': 'Error occurred'})
        elif 'Internal Server Error' in request.headers.get('Authorization', ''):
            return httpx.Response(status_code=500, json={'detail': 'Error occurred'})
        return httpx.Response(status_code=200, json={"payment_preimage": "preimage123", "success": True})
    return httpx.Response(status_code=404)

@pytest.fixture
def alby_wallet():
    return AlbyWallet(token="fake_token")

@pytest.mark.parametrize("auth_header, expected_success, expected_preimage, expected_error", [
    ("Good Request", True, "preimage123", None),
    ("Bad Request", False, '', 'HTTP error: 400 Bad Request'),
    ("Internal Server Error", False, '', 'HTTP error: 500 Internal Server Error')
])
def test_pay_invoice(alby_wallet, auth_header, expected_success, expected_preimage, expected_error):
    # Use HTTPX's MockTransport to simulate the API responses
    with httpx.Client(transport=httpx.MockTransport(custom_response)) as client:
        alby_wallet.client = client  # Assuming you modify AlbyWallet to accept an external client for testing
        alby_wallet.credentials = auth_header
        invoice = "test_invoice_string"
        result = alby_wallet.pay_invoice(invoice)

        # Assertions to verify the behavior
        assert result.success == expected_success
        if result.success:
            assert result.preimage == expected_preimage
        else:
            assert result.error == expected_error
