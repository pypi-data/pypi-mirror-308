import unittest
from lovadira.generator import generate_quote
from lovadira.utils import quotes_list  # Mengimpor quotes_list dari utils.py


class TestQuoteGenerator(unittest.TestCase):
    def test_generate_quote(self):
        # Pastikan generate_quote mengembalikan quote yang valid
        quote = generate_quote()
        self.assertIn(quote, quotes_list)


if __name__ == "__main__":
    unittest.main()
