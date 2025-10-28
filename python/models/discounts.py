from models.products import Product

class Discount:
    def __init__(self, product: Product, description, amount: float) -> None:
        self.product = product
        self.description = description
        self.amount = amount