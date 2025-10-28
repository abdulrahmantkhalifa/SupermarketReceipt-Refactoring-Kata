import unittest
import math
from unittest.mock import patch

# reuse existing mockers
from tests.mockers.fake_catalog import FakeCatalog
from tests.mockers.fake_cart import FakeCart
from tests.mockers.fake_product import ProductQuantityStub, ProductStub
from tests.mockers.fake_receipt import FakeReceipt
from models.discounts import Discount

import teller


class InlineFakeStrategy:
    def __init__(self, discounts_to_return):
        self._discounts = discounts_to_return

    def calculate_discount(self, cart, catalog):
        return self._discounts


class TestTeller(unittest.TestCase):

    def test_add_special_offer_appends(self):
        catalog = FakeCatalog()
        t = teller.Teller(catalog)
        strat = InlineFakeStrategy(discounts_to_return=[])
        self.assertEqual(len(t.offers), 0)
        t.add_special_offer(strat)
        self.assertEqual(len(t.offers), 1)
        self.assertIs(t.offers[0], strat)

    def test_checks_out_articles_from_adds_products(self):
        # Patch Teller's Receipt to our FakeReceipt to capture calls
        with patch.object(teller, "Receipt", FakeReceipt):
            product = ProductStub(name="banana")
            pq = ProductQuantityStub(product, 3)

            cart = FakeCart()
            cart.items = [pq]  # Teller expects cart.items list of ProductQuantity
            # Configure catalog to return unit price for the product
            catalog = FakeCatalog()
            catalog.add_product(product, 0.5)

            t = teller.Teller(catalog)
            receipt = t.checks_out_articles_from(cart)

            self.assertIsInstance(receipt, FakeReceipt)
            self.assertEqual(len(receipt.products), 1)
            prod, qty, unit_price, price = receipt.products[0]
            self.assertIs(prod, product)
            self.assertEqual(qty, 3)
            self.assertEqual(unit_price, 0.5)
            self.assertTrue(math.isclose(price, 3 * 0.5, rel_tol=1e-9))

    def test_checks_out_articles_from_applies_offers(self):
        with patch.object(teller, "Receipt", FakeReceipt):
            product = ProductStub(name="soap")
            pq = ProductQuantityStub(product, 2)

            cart = FakeCart()
            cart.items = [pq]
            # ensure get_product_quantity will return expected quantity for strategies
            cart.set_item_quantity(product, 2)

            catalog = FakeCatalog()
            catalog.add_product(product, 1.25)

            fake_discount = Discount(product=product, description="special", amount=-1.25)
            strat = InlineFakeStrategy(discounts_to_return=[fake_discount])

            t = teller.Teller(catalog)
            t.add_special_offer(strat)

            receipt = t.checks_out_articles_from(cart)

            self.assertIsInstance(receipt, FakeReceipt)
            self.assertEqual(len(receipt.discounts), 1)
            d = receipt.discounts[0]
            self.assertIs(d, fake_discount)
            self.assertIs(d.product, product)
            self.assertEqual(d.description, "special")
            self.assertEqual(d.amount, -1.25)


if __name__ == "__main__":
    unittest.main()
