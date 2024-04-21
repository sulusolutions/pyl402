# token_store.py
from abc import ABC, abstractmethod
from urllib.parse import urlparse

class Token:
    def __init__(self, token_string: str):
        self.token_string = token_string

class Store(ABC):
    @abstractmethod
    def put(self, url: str, token: Token):
        """
        Saves a token against a specified host and path.
        """
        pass

    @abstractmethod
    def get(self, url: str):
        """
        Looks for a token that matches the given host and path.
        Returns the most relevant token if available; otherwise, returns None and False.
        """
        pass

    @abstractmethod
    def delete(self, url: str):
        """
        Removes a token that matches the given host and path.
        """
        pass

# Example concrete implementation of the Store
# This implementation will only link tokens to specific paths on specific hosts.
# This does not make it suitable for uses where token can be reused in different paths.
class MemoryTokenStore(Store):
    def __init__(self):
        self.tokens = {}  # Dictionary to store tokens, keys are (host, path) tuples

    def put(self, url_str: str, token: Token):
        parsed_url = urlparse(url_str)
        self.tokens[(parsed_url.hostname, parsed_url.path)] = token

    def get(self, url_str: str):
            parsed_url = urlparse(url_str)
            key = (parsed_url.hostname, parsed_url.path)
            return self.tokens.get(key)

    def delete(self, url_str: str):
        parsed_url = urlparse(url_str)
        key = (parsed_url.hostname, parsed_url.path)
        if key in self.tokens:
            del self.tokens[key]
            return True
        return False
