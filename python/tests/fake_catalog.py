from catalog import SupermarketCatalog


class FakeCatalog(SupermarketCatalog):
    def __init__(self):
        self.products = {}
        self.prices = {}

    def add_product(self, product, price):
        self.products[product.name] = product
        self.prices[product.name] = price

    def unit_price(self, product):
        try:
            return self.prices[product.name]
        except KeyError as e:
            raise KeyError("Missing product in prices list") from e

