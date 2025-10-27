import unittest
from approvaltests import verify
import sys
import os

# 1. Path Setup: Ensure the project package root is on sys.path
# This is crucial for imports to work when running tests directly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Imports from your source code
# Note: Assuming your imports are correct based on the previous context.
from model_objects import Product, ProductUnit
from teller import Teller
from receipt_printer import ReceiptPrinter
from shopping_cart import ShoppingCart
from tests.fake_catalog import FakeCatalog

class EdgeCaseApprovalTest(unittest.TestCase):
    
    def test_missing_price_error_handling(self):
        """
        Characterizes the existing system's behavior when trying to checkout a product 
        that is in the cart but has no price defined in the catalog.
        
        The approved file will lock in either:
        1. A specific exception message (if the code crashes).
        2. A receipt output showing the item ignored (if the code handles it silently).
        """
        
        # 1. Setup Catalog (The Scenario)
        catalog = FakeCatalog()
        
        good_product = Product("milk", ProductUnit.EACH)
        bad_product = Product("unknown_item", ProductUnit.EACH) # This product is NOT priced
        
        # Add only the price for the good product
        catalog.add_product(good_product, 2.50)
        
        # 2. Setup Teller
        teller = Teller(catalog)
        
        # 3. Fill Cart with both priced and unpriced items
        cart = ShoppingCart()
        cart.add_item_quantity(good_product, 2)    # Should total 5.00
        cart.add_item_quantity(bad_product, 3)     # Expected to cause an error or be ignored
        
        # 4. Generate Output and Capture Error Handling
        
        # We use a try/except block to lock in both success (if it produces a receipt) 
        # or failure (if it throws an exception) behavior.
        try:
            # Note: Using checks_out_articles_from based on your provided file
            receipt = teller.checks_out_articles_from(cart)
            printer = ReceiptPrinter()
            receipt_text = printer.print_receipt(receipt)
            
            # If no exception is thrown, verify the receipt output
            verify(receipt_text)
            
        except Exception as e:
            # If an exception is thrown, verify the exact exception type and message
            # The goal is to lock in this *current* faulty behavior
            error_details = f"EXCEPTION THROWN:\nType: {type(e).__name__}\nMessage: {str(e)}\n\n" \
                            "This test is characterizing the existing error handling for a missing product price."
            verify(error_details)

# This block allows running the test file directly
if __name__ == '__main__':
    unittest.main()