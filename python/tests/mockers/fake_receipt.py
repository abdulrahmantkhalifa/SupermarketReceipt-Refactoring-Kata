class FakeReceipt:
    def __init__(self):
        self.products = []   # list of tuples (product, quantity, unit_price, price)
        self.discounts = []  # list of discount objects added

    def add_product(self, product, quantity, unit_price, price):
        self.products.append((product, quantity, unit_price, price))

    def add_discount(self, discount):
        self.discounts.append(discount)


class ReceiptStub:
    """Mock Receipt class to supply data to the formatter."""
    def __init__(self, items, discounts, total_price):
        self.items = items
        self.discounts = discounts
        self._total_price = total_price

    def total_price(self):
        return self._total_price


class ReceiptItemStub:
    def __init__(self, product, quantity, price, total_price):
        self.product = product
        self.quantity = quantity
        self.price = price
        self.total_price = total_price