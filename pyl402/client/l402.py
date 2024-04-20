import re
from typing import Optional
from pyl402.token_store import Token, Store
from pyl402.wallet import Wallet
import httpx


class L402Client(httpx.Client):
    def __init__(self, wallet: Wallet, store: Store, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wallet = wallet
        self.store = store

    def send(self, request: httpx.Request, *args, **kwargs) -> httpx.Response:
        # First, try to retrieve and use an L402 token if available
        token = self.store.get(str(request.url))
        if token:
            request.headers['Authorization'] = f"L402 {token.token_string}"

        response = super().send(request, *args, **kwargs)
        # Check for 402 Payment Required status code
        if response.status_code == 402:
            # Handle payment challenge
            auth_header = response.headers.get('WWW-Authenticate', '')
            challenge = self.parse_header(auth_header)
            if challenge and 'invoice' in challenge:
                # Attempt to pay the invoice
                payment_result = self.wallet.pay_invoice(challenge['invoice'])
                if payment_result.success:
                    # If payment is successful, construct and save the L402 token
                    l402_token = f"{challenge['header_key']} {challenge['macaroon']}:{payment_result.preimage}"
                    self.store.put(str(request.url), Token(l402_token))
                    # Retry the request with the new token
                    request.headers['Authorization'] = f"{l402_token}"
                    return super().send(request, *args, **kwargs)
        
        return response

    def parse_header(self, header: str) -> Optional[dict]:
        header_key_match = re.search(r'^(LSAT|L402)', header)
        invoice_match = re.search(r'invoice="([^"]+)"', header)
        macaroon_match = re.search(r'macaroon="([^"]+)"', header)
        if invoice_match and macaroon_match:
            return {
                'header_key': header_key_match.group(0) if header_key_match else '',
                'invoice': invoice_match.group(1),
                'macaroon': macaroon_match.group(1)
            }
        return None