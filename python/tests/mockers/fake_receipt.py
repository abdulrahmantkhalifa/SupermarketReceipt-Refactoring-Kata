class FakeReceipt:
    def __init__(self):
        self.products = []   # list of tuples (product, quantity, unit_price, price)
        self.discounts = []  # list of discount objects added

    def add_product(self, product, quantity, unit_price, price):
        self.products.append((product, quantity, unit_price, price))

    def add_discount(self, discount):
        self.discounts.append(discount)
