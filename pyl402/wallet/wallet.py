from abc import ABC, abstractmethod
from typing import Optional

class PaymentResult:
    def __init__(self, preimage: str, success: bool, error: Optional[str] = None):
        self.preimage = preimage
        self.success = success
        self.error = error

class Wallet(ABC):
    @abstractmethod
    def pay_invoice(self, invoice: str) -> PaymentResult:
        """
        Attempts to pay the given invoice and returns the result.
        Should handle necessary logic like decoding the invoice, making the payment through the wallet's API,
        and returning the preimage if successful.
        """
        pass