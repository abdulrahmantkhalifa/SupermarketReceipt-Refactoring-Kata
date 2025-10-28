from models.products import ProductQuantity, Product


class ShoppingCart:

    def __init__(self):
        self._items = []
        self._product_quantities = {}

    @property
    def items(self):
        return self._items

    def add_item(self, product: Product):
        self.add_item_quantity(product, 1.0)

    def get_product_quantity(self, product: Product):
        return self._product_quantities.get(product.name, 0)

    @property
    def product_quantities(self):
        return self._product_quantities

    def add_item_quantity(self, product: Product, quantity: int | float):
        self._items.append(ProductQuantity(product, quantity))
        if product.name in self._product_quantities.keys():
            # this will probably cause issues with float quantities
            self._product_quantities[product.name] = self._product_quantities[product.name] + quantity
        else:
            self._product_quantities[product.name] = quantity
