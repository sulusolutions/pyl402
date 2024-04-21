import httpx
from .wallet import Wallet, PaymentResult

class AlbyPaymentResponse:
    def __init__(self, amount, description, destination, fee, payment_hash, payment_preimage, payment_request):
        self.amount = amount
        self.description = description
        self.destination = destination
        self.fee = fee
        self.payment_hash = payment_hash
        self.payment_preimage = payment_preimage
        self.payment_request = payment_request

class AlbyWallet(Wallet):
    def __init__(self, token: str, client: httpx.Client = None):
        self.base_url = "https://api.getalby.com"
        self.credentials = token
        self.client = client if client else httpx.Client()

    def pay_invoice(self, invoice: str) -> PaymentResult:
        url = f"{self.base_url}/payments/bolt11"
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.credentials}",
            'User-Agent': 'alby-python'
        }
        body = {
            "invoice": invoice  # Include "amount" if necessary
        }

        try:
            response = self.client.post(url, json=body, headers=headers)
            response.raise_for_status()  # Check for HTTP request errors

            alby_response = response.json()
            return PaymentResult(preimage=alby_response.get('payment_preimage', ''),
                                    success=True)
        except httpx.HTTPStatusError as e:
                return PaymentResult(preimage='', success=False, error=f'HTTP error: {e.response.status_code} {e.response.reason_phrase}')
        except httpx.RequestError as e:
            return PaymentResult(preimage='', success=False, error=f'Request error: {str(e)}')
        except ValueError:
            return PaymentResult(preimage='', success=False, error='Failed to decode JSON')

# Example usage:
# if __name__ == "__main__":
#     wallet = AlbyWallet("your_token_here")
#     invoice = Invoice("example_invoice")
#     result = wallet.pay_invoice(invoice)
#     if result.success:
#         print("Payment succeeded:", result.preimage)
#     else:
#         print("Error:", result.error)
