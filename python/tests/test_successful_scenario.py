# test_acceptance_receipt.py

import unittest
from approvaltests import verify
### ensure project package root is on sys.path so imports work when running tests directly
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model_objects import Product, SpecialOfferType, ProductUnit
from teller import Teller
from receipt_printer import ReceiptPrinter
# from catalog import SupermarketCatalog
from shopping_cart import ShoppingCart
from tests.fake_catalog import FakeCatalog

class ReceiptApprovalTest(unittest.TestCase):
    
    def test_full_complex_receipt_generation(self):
        """
        Creates a maximally complex scenario to generate a Golden Master receipt.
        This tests the full integration of catalog, cart, teller, and all offers.
        """
        
        # 1. Setup Catalog
        catalog = FakeCatalog()
        
        # Define Products (Assumed ProductUnit enum exists in model.py)
        toothbrush = Product("toothbrush", ProductUnit.EACH)
        toothpaste = Product("toothpaste", ProductUnit.EACH)
        apples = Product("apples", ProductUnit.KILO)
        rice = Product("rice", ProductUnit.EACH)
        
        # Add products and prices to catalog
        catalog.add_product(toothbrush, 0.99)
        catalog.add_product(toothpaste, 1.79)
        catalog.add_product(apples, 1.99)
        catalog.add_product(rice, 2.49)
        
        # 2. Setup Teller and Offers
        teller = Teller(catalog)
        
        # Buy two toothbrushes, get one free (3-for-2 logic)
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0.0) 
        
        # 20% discount on apples (Percentage discount)
        teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0) 

        ## since not implemented will be commented 
        ## 20% discount on apples (Percentage discount)
        # teller.add_special_offer(SpecialOfferType.PERCENT_DISCOUNT, apples, 20.0)
        
        # Five tubes of toothpaste for 7.49 (N for X price logic)
        teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)
        
        # 3. Fill Cart (The input that generates the Golden Master)
        cart = ShoppingCart()
        cart.add_item_quantity(apples, 2.5)      # Weight: 20% off 2.5kg of apples
        cart.add_item_quantity(rice, 1)          # Unit: No discount
        cart.add_item_quantity(toothbrush, 5)    # Unit: Triggers 3-for-2 discount (1 free, 2 at full price)
        cart.add_item_quantity(toothpaste, 6)    # Unit: Triggers 5-for-X, 1 at regular price
        
        # 4. Generate Output
        receipt = teller.checks_out_articles_from(cart)
        printer = ReceiptPrinter()
        receipt_text = printer.print_receipt(receipt)
        
        # 5. Approval Assertion
        # The single line that captures the complex output for verification
        verify(receipt_text)

if __name__ == '__main__':
    unittest.main()