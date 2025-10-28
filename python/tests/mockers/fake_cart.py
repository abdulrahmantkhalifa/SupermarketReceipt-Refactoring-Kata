# FakeCart implementing the expected interface
class FakeCart:
    def __init__(self):
        self._quantities = {}

    def add_item_quantity(self, product, quantity):
        self._quantities[product] = self._quantities.get(product, 0) + quantity

    def set_item_quantity(self, product, quantity):
        self._quantities[product] = quantity

    def get_product_quantity(self, product):
        return self._quantities.get(product, 0)
