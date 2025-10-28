from abc import ABC, abstractmethod
from catalog import SupermarketCatalog
from models.discounts import Discount


class OfferStrategy(ABC):

    def __init__(self, target_product, required_product_count, discription=None):
        self.target_product = target_product
        self.required_product_count = required_product_count
        self.description = discription

    @abstractmethod
    def calculate_discount(self, cart, catalog):
        pass

    @abstractmethod
    def generate_description(self) -> str:
        """
        Generates the formatted string for the discount, e.g., '3 for 2 (toothbrush)'.
        This method must be implemented by the concrete strategy.
        """
        pass



    def get_applicable_data(self, cart, catalog: SupermarketCatalog):
        """Returns (quantity, unit_price) if product is in cart, otherwise (0, 0.0)"""
            
        # 2. Get data

        # the quantity also represents existence 
        # we used this function as it is less complex using a dict with o(k) instead of looping over keys 
        quantity = cart.get_product_quantity(self.target_product)
        if not quantity:
            return 0, 0.0
        
        unit_price = catalog.get_unit_price(self.target_product)
        
        return quantity, unit_price


class BuyNGetMFreeStrategy(OfferStrategy):
    
    def __init__(self, target_product, required_product_count, charge_m, description=None):
        # N here is the required product count
        super().__init__(target_product, required_product_count)
        self.charge_m = charge_m
        self.free_m = required_product_count - charge_m
        self.description = description
        if not description:
            self.description = self.generate_description()


    def generate_description(self) -> str:
        # Example: 3 for 2 (toothbrush)
        product_name = self.target_product.name
        return f"{self.required_product_count} for {self.charge_m}"


    def calculate_discount(self, cart, catalog):
        quantity, unit_price = self.get_applicable_data(cart, catalog)

        # validate threshold is met
        if quantity < self.required_product_count:
            return []
    
        # Calculate how many full deals were completed, so like buy 2 get 3 , but for 6
        # uses intiger devision
        number_of_deals = quantity // self.required_product_count
        
        # Calculate the total free items and the cash value of the discount
        total_free_items = number_of_deals * self.free_m
        discount_amount = total_free_items * unit_price
        
        if discount_amount > 0:
            return [Discount(
                self.target_product, 
                self.description, 
                -discount_amount
            )]
            
        return []


class PercentDiscountStrategy(OfferStrategy):
    
    def __init__(self, target_product, percentage, description=None):
        super().__init__(target_product, 1, description)
        self.percentage_decimal = percentage / 100.0 # Store as decimal (0.10)
        self.description = description
        if not description:
            self.description = self.generate_description()

    def generate_description(self) -> str:
        # Example: 10.0% off (apples)
        product_name = self.target_product.name
        # Using :.1f for single decimal place precision
        return f"{self.percentage_decimal * 100}% off"


    def calculate_discount(self, cart, catalog) -> list[Discount]:
        quantity, unit_price = self.get_applicable_data(cart, catalog)

        # Validate the threshold is met 
        if quantity < self.required_product_count:
            return []
        
        # Calculate discounted quantity and total discount
        discounted_value = quantity * unit_price * self.percentage_decimal
        
        if discounted_value > 0:
            return [Discount(
                self.target_product, 
                self.description, 
                -discounted_value
            )]
            
        return []


class BuyQuantityForAmountStrategy(OfferStrategy):
    
    def __init__(self, target_product, required_product_count, fixed_price_x, description=None):
        super().__init__(target_product, required_product_count, description)
        self.fixed_price_x = fixed_price_x # e.g., 7.49 (the deal price)
        self.description = description
        if not description:
            self.description = self.generate_description()
            

    def generate_description(self) -> str:
        """
        Generates the formatted string for the discount.
        Example output: "5 for 7.49 (toothpaste)"
        """
        product_name = self.target_product.name
        
        # Format the amount to two decimal places (e.g., 7.49)
        amount_formatted = f"{self.fixed_price_x:.2f}"
        
        # Combine the parts
        return f"{self.required_product_count} for {amount_formatted}"


    def calculate_discount(self, cart, catalog):
        quantity, unit_price = self.get_applicable_data(cart, catalog)
        
        # check threshold is met
        if quantity < self.required_product_count:
            return []
        
        # Calculate full deals and remainder
        number_of_deals = quantity // self.required_product_count
        remaining_items = quantity % self.required_product_count
        
        # Calculate the cost
        cost_of_deals = number_of_deals * self.fixed_price_x
        cost_of_remainder = remaining_items * unit_price
        total_cost_after_deal = cost_of_deals + cost_of_remainder
        
        # Calculate the regular total and the discount amount
        regular_total = quantity * unit_price
        discount_amount = regular_total - total_cost_after_deal
        
        if discount_amount > 0:
            return [Discount(
                self.target_product, 
                self.description, 
                -discount_amount
            )]
            
        return []