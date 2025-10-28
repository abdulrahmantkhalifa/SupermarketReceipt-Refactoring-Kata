from abc import ABC, abstractmethod

from models.products import ProductUnit
from models.discounts import Discount
from receipt import Receipt, ReceiptItem

class ReceiptFormatter(ABC):
    """
    Abstract Base Class defining the interface for all receipt presentation strategies.
    """
    
    def __init__(self, columns=40):
        self.columns = columns
        
    @abstractmethod
    def format_receipt(self, receipt) -> str:
        """
        Takes a Receipt object and returns its fully formatted string representation.
        """
        pass

class TextReceiptFormatter(ReceiptFormatter):
    """
    Concrete Strategy for generating the plain-text, console-ready receipt format.
    """
    
    # __init__ inherited from ReceiptFormatter (self.columns is set)

    def format_receipt(self, receipt: Receipt) -> str:
        """
        Orchestrates the printing process for the text format.
        This method replaces the old ReceiptPrinter.print_receipt.
        """
        result = ""
        
        # 1. Print Items
        for item in receipt.items:
            result += self._print_receipt_item(item)

        # 2. Print Discounts
        for discount in receipt.discounts:
            result += self._print_discount(discount)

        # 3. Print Total
        result += "\n"
        result += self._present_total(receipt)
        
        return str(result)

    # --- Private Helper Methods (Refactored from old class) ---

    def _print_receipt_item(self, item: ReceiptItem) -> str:
        total_price_printed = self._print_price(item.total_price)
        name = item.product.name
        line = self._format_line_with_whitespace(name, total_price_printed)
        if item.quantity != 1:
            line += f"  {self._print_price(item.price)} * {self._print_quantity(item)}\n"
        return line

    def _format_line_with_whitespace(self, name: str, value: str) -> str:
        line = name
        whitespace_size = self.columns - len(name) - len(value)
        # Ensure whitespace_size is non-negative
        whitespace_size = max(0, whitespace_size) 
        
        line += " " * whitespace_size
        line += value
        line += "\n"
        return line

    def _print_price(self, price: float) -> str:
        return "%.2f" % price

    def _print_quantity(self, item: ReceiptItem) -> str:
        if ProductUnit.EACH == item.product.unit:
            return str(item.quantity)
        else:
            return '%.3f' % item.quantity

    def _print_discount(self, discount: Discount) -> str:
        name = f"{discount.description} ({discount.product.name})"
        value = self._print_price(discount.amount) # Using the actual discount amount
        return self._format_line_with_whitespace(name, value)

    def _present_total(self, receipt: Receipt) -> str:
        name = "Total: "
        value = self._print_price(receipt.total_price())
        return self._format_line_with_whitespace(name, value)




