import pytest
import httpx
from unittest.mock import Mock, patch
from pyl402.token_store import Token, Store
from pyl402.wallet import Wallet, PaymentResult
from pyl402.client import L402Client  # Adjust import path as necessary

@pytest.fixture
def mock_wallet():
    wallet = Mock(spec=Wallet)
    wallet.pay_invoice = Mock(return_value=PaymentResult(preimage='preimage_test', success=True))
    return wallet

@pytest.fixture
def mock_store():
    store = Mock(spec=Store)
    store.get = Mock(return_value=None)
    store.put = Mock()
    return store

@pytest.fixture
def client(mock_wallet, mock_store):
    return L402Client(wallet=mock_wallet, store=mock_store)

def test_send_no_token(client, mock_wallet, mock_store):
    with patch.object(httpx.Client, 'send', return_value=httpx.Response(status_code=200)) as mock_send:
        url = "http://example.com"
        request = httpx.Request(method="GET", url=url)
        response = client.send(request)

        mock_send.assert_called_once()
        assert response.status_code == 200
        mock_store.get.assert_called_with(url)
        mock_wallet.pay_invoice.assert_not_called()

def test_send_with_token_found(client, mock_wallet, mock_store):
    mock_store.get = Mock(return_value=Token(token_string="token123"))
    with patch.object(httpx.Client, 'send', return_value=httpx.Response(status_code=200)) as mock_send:
        url = "http://example.com"
        request = httpx.Request(method="GET", url=url)
        response = client.send(request)

        mock_send.assert_called_once()
        assert "Authorization" in request.headers
        assert request.headers["Authorization"] == "L402 token123"
        assert response.status_code == 200

def test_handle_402_payment_required(client, mock_wallet, mock_store):
    mock_response = httpx.Response(status_code=402)
    mock_response.headers = {'WWW-Authenticate': 'LSAT invoice="123", macaroon="macaroon_test"'}
    with patch.object(httpx.Client, 'send', side_effect=[mock_response, httpx.Response(status_code=200)]) as mock_send:
        url = "http://example.com"
        request = httpx.Request(method="GET", url=url)
        response = client.send(request)

        assert mock_send.call_count == 2
        assert mock_wallet.pay_invoice.call_args[0][0] == "123"
        assert response.status_code == 200
        args, kwargs = mock_store.put.call_args
        assert args[0] == url
        assert isinstance(args[1], Token)
        assert args[1].token_string == "LSAT macaroon_test:preimage_test"

def test_parse_header(client):
    header = 'LSAT invoice="123", macaroon="macaroon_test"'
    result = client.parse_header(header)
    assert result == {'header_key': 'LSAT', 'invoice': '123', 'macaroon': 'macaroon_test'}
