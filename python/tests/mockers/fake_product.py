class ProductQuantityStub:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

# Simple product stub
class ProductStub:
    def __init__(self, name, unit=None):
        self.name = name
        self.unit = unit
