import unittest
from pyl402.token_store import MemoryTokenStore, Token

class TestMemoryTokenStore(unittest.TestCase):
    def setUp(self):
        """Initialize a new MemoryTokenStore before each test."""
        self.store = MemoryTokenStore()

    def test_put_and_get_token(self):
        """Test storing a token and retrieving it."""
        token = Token("abc123")
        url = "http://example.com/path"
        self.store.put(url, token)
        retrieved_token = self.store.get(url)
        self.assertEqual(retrieved_token.token_string, token.token_string, "Failed to retrieve the correct token.")

    def test_get_nonexistent_token(self):
        """Test retrieving a token that does not exist."""
        url = "http://example.com/nonexistent"
        token = self.store.get(url)
        self.assertIsNone(token, "Retrieved a token where there should be none.")

    def test_delete_token(self):
        """Test deleting an existing token."""
        url = "http://example.com/path"
        token = Token("abc123")
        self.store.put(url, token)
        self.assertTrue(self.store.delete(url), "Failed to delete the token.")
        self.assertIsNone(self.store.get(url), "Token still exists after deletion.")

    def test_delete_nonexistent_token(self):
        """Test deleting a token that does not exist."""
        url = "http://example.com/nonexistent"
        self.assertFalse(self.store.delete(url), "Incorrectly reported deletion of a non-existent token.")

    def test_overwrite_token(self):
        """Test overwriting an existing token."""
        url = "http://example.com/path"
        first_token = Token("abc123")
        second_token = Token("def456")
        self.store.put(url, first_token)
        self.store.put(url, second_token)
        retrieved_token = self.store.get(url)
        self.assertEqual(retrieved_token.token_string, second_token.token_string, "Failed to overwrite the existing token.")

if __name__ == "__main__":
    unittest.main()
