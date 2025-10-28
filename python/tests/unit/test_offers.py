import unittest

from models.offers import OfferStrategy, BuyNGetMFreeStrategy, PercentDiscountStrategy, BuyQuantityForAmountStrategy
from tests.mockers.fake_cart import FakeCart
from tests.mockers.fake_catalog import FakeCatalog 
from tests.mockers.fake_product import ProductStub

# Minimal concrete subclass so we can instantiate OfferStrategy
class ConcreteOffer(OfferStrategy):
    def generate_description(self) -> str:
        return "concrete offer"

    def calculate_discount(self, cart, catalog):
        return []





class OfferGetApplicableDataTests(unittest.TestCase):

    def test_get_applicable_data_returns_zero_when_product_not_in_cart(self):
        product = ProductStub("apple")
        cart = FakeCart()
        catalog = FakeCatalog()
        catalog.add_product(product, 1.99)

        offer = ConcreteOffer(product, required_product_count=1)
        qty, price = offer.get_applicable_data(cart, catalog)

        self.assertEqual((qty, price), (0, 0.0))

    def test_get_applicable_data_returns_quantity_and_price_when_in_cart(self):
        product = ProductStub("banana")
        cart = FakeCart()
        cart.add_item_quantity(product, 3)
        catalog = FakeCatalog()
        catalog.add_product(product, 0.89)

        offer = ConcreteOffer(product, required_product_count=1)
        qty, price = offer.get_applicable_data(cart, catalog)

        self.assertEqual((qty, price), (3, 0.89))

    def test_get_applicable_data_returns_zero_when_quantity_is_zero(self):
        product = ProductStub("orange")
        cart = FakeCart()
        cart.set_item_quantity(product, 0)
        catalog = FakeCatalog()
        catalog.add_product(product, 2.50)

        offer = ConcreteOffer(product, required_product_count=1)
        qty, price = offer.get_applicable_data(cart, catalog)

        self.assertEqual((qty, price), (0, 0.0))


class TestOfferStrategyDescriptions(unittest.TestCase):

    def test_buy_n_get_m_free_generate_description(self):
        product = ProductStub(name="toothbrush")
        strategy = BuyNGetMFreeStrategy(product, required_product_count=3, charge_m=2)
        self.assertEqual(strategy.generate_description(), "3 for 2")
        self.assertEqual(strategy.description, "3 for 2")

    def test_percent_discount_generate_description(self):
        product = ProductStub(name="apples")
        strategy = PercentDiscountStrategy(product, percentage=10)
        self.assertEqual(strategy.generate_description(), "10.0% off")
        self.assertEqual(strategy.description, "10.0% off")

    def test_buy_quantity_for_amount_generate_description(self):
        product = ProductStub(name="toothpaste")
        strategy = BuyQuantityForAmountStrategy(product, required_product_count=5, fixed_price_x=7.49)
        self.assertEqual(strategy.generate_description(), "5 for 7.49")
        self.assertEqual(strategy.description, "5 for 7.49")


class TestOfferStrategyDiscounts(unittest.TestCase):

    def test_buy_n_get_m_free_calculate_discount_hit(self):
        product = ProductStub(name="toothbrush")
        strategy = BuyNGetMFreeStrategy(product, required_product_count=3, charge_m=2)
        catalog = FakeCatalog()
        catalog.add_product(product, 10.0)
        cart = FakeCart()
        cart.set_item_quantity(product, 6)
        discounts = strategy.calculate_discount(cart, catalog)
        self.assertEqual(len(discounts), 1)
        d = discounts[0]
        self.assertIs(d.product, product)
        self.assertEqual(d.description, "3 for 2")
        self.assertAlmostEqual(d.amount, -20.0, places=6)

    def test_buy_n_get_m_free_calculate_discount_miss(self):
        product = ProductStub(name="toothbrush")
        strategy = BuyNGetMFreeStrategy(product, required_product_count=3, charge_m=2)
        catalog = FakeCatalog()
        catalog.add_product(product, 10.0)
        cart = FakeCart()
        cart.set_item_quantity(product, 2)
        self.assertEqual(strategy.calculate_discount(cart, catalog), [])

    def test_percent_discount_calculate_discount_hit(self):
        product = ProductStub(name="apples")
        strategy = PercentDiscountStrategy(product, percentage=10)
        catalog = FakeCatalog()
        catalog.add_product(product, 2.5)
        cart = FakeCart()
        cart.set_item_quantity(product, 3)
        discounts = strategy.calculate_discount(cart, catalog)
        self.assertEqual(len(discounts), 1)
        d = discounts[0]
        self.assertIs(d.product, product)
        self.assertEqual(d.description, "10.0% off")
        self.assertAlmostEqual(d.amount, -0.75, places=6)

    def test_percent_discount_calculate_discount_miss(self):
        product = ProductStub(name="apples")
        strategy = PercentDiscountStrategy(product, percentage=10)
        catalog = FakeCatalog()
        catalog.add_product(product, 2.5)
        cart = FakeCart()
        cart.set_item_quantity(product, 0)
        self.assertEqual(strategy.calculate_discount(cart, catalog), [])

    def test_buy_quantity_for_amount_calculate_discount_hit(self):
        product = ProductStub(name="toothpaste")
        strategy = BuyQuantityForAmountStrategy(product, required_product_count=5, fixed_price_x=7.49)
        catalog = FakeCatalog()
        catalog.add_product(product, 2.0)
        cart = FakeCart()
        cart.set_item_quantity(product, 7)
        discounts = strategy.calculate_discount(cart, catalog)
        self.assertEqual(len(discounts), 1)
        d = discounts[0]
        self.assertIs(d.product, product)
        self.assertEqual(d.description, "5 for 7.49")
        self.assertAlmostEqual(d.amount, -2.51, places=3)

    def test_buy_quantity_for_amount_calculate_discount_miss(self):
        product = ProductStub(name="toothpaste")
        strategy = BuyQuantityForAmountStrategy(product, required_product_count=5, fixed_price_x=7.49)
        catalog = FakeCatalog()
        catalog.add_product(product, 2.0)
        cart = FakeCart()
        cart.set_item_quantity(product, 4)
        self.assertEqual(strategy.calculate_discount(cart, catalog), [])

if __name__ == "__main__":
    unittest.main()