from receipt import Receipt


class Teller:

    def __init__(self, catalog):
        self.catalog = catalog
        self.offers = []

    def add_special_offer(self, offer_strategy):
        self.offers.append(offer_strategy)

    def checks_out_articles_from(self, cart):
        receipt = Receipt()
        product_quantities = cart.items
        for pq in product_quantities:
            p = pq.product
            quantity = pq.quantity
            unit_price = self.catalog.get_unit_price(p)
            price = quantity * unit_price
            receipt.add_product(p, quantity, unit_price, price)

        # the_cart no longer needs the offers or catalog arguments
        self._apply_offers(receipt, cart)

        return receipt

    def _apply_offers(self, receipt, cart):
        # this is the Context loop for the strategy pattern 
        for strategy in self.offers:
            # Each strategy returns a list of Discount objects (or an empty list)
            discounts = strategy.calculate_discount(cart, self.catalog)
            
            # Add all resulting discounts to the receipt
            for discount in discounts:
                receipt.add_discount(discount)
