import unittest
import math


import receipt 
from models.discounts import Discount
from tests.mockers.fake_product import ProductStub
from receipt_printer import ReceiptFormatter 


# --- Inline Mock Strategy for Formatting ---
class FakeFormatter(ReceiptFormatter):
    """Mock formatter that returns a unique string based on its class name."""
    def format_receipt(self, receipt) -> str:
        # Returns a string that confirms this specific strategy was executed.
        return f"--- {type(self).__name__} Output ---"

class TextFormatter(FakeFormatter):
    pass

class TestReceipt(unittest.TestCase):

    def setUp(self):
        """Standard setup: create a clean receipt object and common data."""
        self.reciept = receipt.Receipt()
        self.milk = ProductStub(name="milk")
        self.bread = ProductStub(name="bread")

        # Create line items
        self.reciept.add_product(self.milk, 2.0, 1.50, 3.00)  # Total: 3.00
        self.reciept.add_product(self.bread, 1.0, 2.00, 2.00) # Total: 2.00

        # Create a discount
        self.discount = Discount(self.milk, "Milk special", amount=-0.50)
        self.reciept.add_discount(self.discount) # Total -0.50

    def test_add_product_stores_items_correctly(self):
        """Verifies that line items are correctly stored in the Receipt object."""
        self.assertEqual(len(self.reciept.items), 2)
        
        # Check first item (milk)
        item1 = self.reciept.items[0]
        self.assertIs(item1.product, self.milk)
        self.assertEqual(item1.quantity, 2.0)
        self.assertEqual(item1.price, 1.50)
        self.assertTrue(math.isclose(item1.total_price, 3.00))

    def test_add_discount_stores_discounts_correctly(self):
        """Verifies that discount objects are correctly stored."""
        self.assertEqual(len(self.reciept.discounts), 1)
        d = self.reciept.discounts[0]
        self.assertIs(d, self.discount)
        self.assertEqual(d.description, "Milk special")
        self.assertEqual(d.amount, -0.50)
        
    def test_total_price_calculates_correctly_with_discounts(self):
        """Verifies the final total price calculation."""
        # Expected calculation: (3.00 + 2.00) + (-0.50) = 4.50
        expected_total = 4.50
        actual_total = self.reciept.total_price()
        
        self.assertTrue(math.isclose(actual_total, expected_total, rel_tol=1e-9))

    def test_generate_output_executes_single_formatter_strategy(self):
        """Verifies that a single formatter is correctly executed."""
        formatter = TextFormatter()
        
        # Call the new Context method with a single item list
        output = self.reciept.generate_output(formatter) 

        self.assertEqual(output, "--- TextFormatter Output ---")
        
        
    def test_generate_output_handles_empty_formatter_list(self):
        """Ensures method returns empty dict if no formatters are passed."""
        output_dict = self.reciept.generate_output(None)
        self.assertEqual(output_dict, '')

if __name__ == "__main__":
    unittest.main()