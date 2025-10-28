
class SupermarketCatalog:

    def add_product(self, product, price):
        raise Exception("cannot be called from a unit test - it accesses the database")

    def get_unit_price(self, product):
        raise Exception("cannot be called from a unit test - it accesses the database")

