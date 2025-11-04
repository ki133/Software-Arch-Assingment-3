"""
Models Module - Core Domain Classes

This module defines all core business classes for the e-commerce system:
- Address: Represents a physical address
- Customer: Represents a customer/user
- Product: Represents a product in the catalog
- CartItem: Represents an item in the shopping cart
- ShoppingCart: Manages the shopping cart
- OrderLine: Represents a line item in an order
- Order: Represents a customer order
- Invoice: Represents an invoice for an order
- Shipment: Represents shipment information

Following PEP 8 style guide and implementing design patterns:
- Repository Pattern (for persistence)
- Adapter Pattern (for external services)
- Strategy Pattern (for payment methods)
"""

from datetime import datetime
from typing import List, Optional
import uuid


class Address:
    """
    Represents a physical address.
    
    Attributes:
        street (str): Street address
        city (str): City name
        postal_code (str): Postal/ZIP code
        country (str): Country name
    """
    
    def __init__(self, street: str, city: str, postal_code: str, country: str):
        """
        Initialize an Address object.
        
        Args:
            street: Street address
            city: City name
            postal_code: Postal/ZIP code
            country: Country name
        """
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.country = country
    
    def to_dict(self) -> dict:
        """Convert Address to dictionary for JSON serialization."""
        return {
            "street": self.street,
            "city": self.city,
            "postal_code": self.postal_code,
            "country": self.country
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Address':
        """Create Address from dictionary (for deserialization)."""
        return Address(
            street=data.get("street"),
            city=data.get("city"),
            postal_code=data.get("postal_code"),
            country=data.get("country")
        )
    
    def __str__(self) -> str:
        """String representation of address."""
        return f"{self.street}, {self.city}, {self.postal_code}, {self.country}"


class Customer:
    """
    Represents a customer/user in the system.
    
    Attributes:
        customer_id (str): Unique identifier for the customer
        name (str): Customer's full name
        email (str): Customer's email address
        password (str): Customer's password (should be hashed in production)
        address (Address): Customer's address
        created_at (datetime): Account creation timestamp
    """
    
    def __init__(self, name: str, email: str, password: str, address: Address):
        """
        Initialize a Customer object.
        
        Args:
            name: Customer's full name
            email: Customer's email address
            password: Customer's password
            address: Address object for the customer
        """
        self.customer_id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = password  # In production, this should be hashed
        self.address = address
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convert Customer to dictionary for JSON serialization."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "address": self.address.to_dict(),
            "created_at": self.created_at
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Customer':
        """Create Customer from dictionary (for deserialization)."""
        address = Address.from_dict(data.get("address", {}))
        customer = Customer(
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),
            address=address
        )
        # Restore the original customer_id and created_at
        customer.customer_id = data.get("customer_id", customer.customer_id)
        customer.created_at = data.get("created_at", customer.created_at)
        return customer
    
    def __str__(self) -> str:
        """String representation of customer."""
        return f"{self.name} ({self.email})"


class Product:
    """
    Represents a product in the catalog.
    
    Attributes:
        product_id (str): Unique identifier for the product
        name (str): Product name
        description (str): Product description
        price (float): Product price
        quantity_available (int): Available quantity in stock
    """
    
    def __init__(self, name: str, description: str, price: float, quantity_available: int):
        """
        Initialize a Product object.
        
        Args:
            name: Product name
            description: Product description
            price: Product price
            quantity_available: Available quantity in stock
        """
        self.product_id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.price = price
        self.quantity_available = quantity_available
    
    def to_dict(self) -> dict:
        """Convert Product to dictionary for JSON serialization."""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "quantity_available": self.quantity_available
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Product':
        """Create Product from dictionary (for deserialization)."""
        product = Product(
            name=data.get("name"),
            description=data.get("description"),
            price=float(data.get("price", 0)),
            quantity_available=int(data.get("quantity_available", 0))
        )
        product.product_id = data.get("product_id", product.product_id)
        return product
    
    def __str__(self) -> str:
        """String representation of product."""
        return f"{self.name} - ${self.price:.2f} (Available: {self.quantity_available})"


class CartItem:
    """
    Represents an item in the shopping cart.
    
    Attributes:
        product (Product): The product being purchased
        quantity (int): The quantity of the product
    """
    
    def __init__(self, product: Product, quantity: int):
        """
        Initialize a CartItem object.
        
        Args:
            product: Product object
            quantity: Quantity of the product
        """
        self.product = product
        self.quantity = quantity
    
    def get_subtotal(self) -> float:
        """Calculate the subtotal for this cart item (price * quantity)."""
        return self.product.price * self.quantity
    
    def __str__(self) -> str:
        """String representation of cart item."""
        return f"{self.product.name} x{self.quantity} = ${self.get_subtotal():.2f}"


class ShoppingCart:
    """
    Represents a shopping cart for a customer.
    
    Attributes:
        items (List[CartItem]): List of items in the cart
        customer_id (str): The ID of the customer who owns this cart
    """
    
    def __init__(self, customer_id: str):
        """
        Initialize a ShoppingCart object.
        
        Args:
            customer_id: The ID of the customer who owns this cart
        """
        self.items: List[CartItem] = []
        self.customer_id = customer_id
    
    def add_item(self, product: Product, quantity: int) -> None:
        """
        Add an item to the shopping cart.
        
        If the product is already in the cart, increase its quantity.
        
        Args:
            product: Product to add
            quantity: Quantity to add
        """
        # Check if product already exists in cart
        for item in self.items:
            if item.product.product_id == product.product_id:
                item.quantity += quantity
                return
        
        # Product not found, add as new item
        self.items.append(CartItem(product, quantity))
    
    def remove_item(self, product_id: str) -> bool:
        """
        Remove an item from the shopping cart.
        
        Args:
            product_id: The ID of the product to remove
            
        Returns:
            True if item was removed, False if item not found
        """
        for i, item in enumerate(self.items):
            if item.product.product_id == product_id:
                self.items.pop(i)
                return True
        return False
    
    def update_item_quantity(self, product_id: str, new_quantity: int) -> bool:
        """
        Update the quantity of an item in the cart.
        
        Args:
            product_id: The ID of the product to update
            new_quantity: The new quantity
            
        Returns:
            True if item was updated, False if item not found
        """
        for item in self.items:
            if item.product.product_id == product_id:
                item.quantity = new_quantity
                return True
        return False
    
    def get_subtotal(self) -> float:
        """Calculate the subtotal (sum of all items before tax and shipping)."""
        return sum(item.get_subtotal() for item in self.items)
    
    def clear(self) -> None:
        """Clear all items from the cart."""
        self.items = []
    
    def is_empty(self) -> bool:
        """Check if the cart is empty."""
        return len(self.items) == 0
    
    def __str__(self) -> str:
        """String representation of shopping cart."""
        if self.is_empty():
            return "Shopping Cart (empty)"
        return f"Shopping Cart ({len(self.items)} items, Subtotal: ${self.get_subtotal():.2f})"


class OrderLine:
    """
    Represents a line item in an order.
    
    Attributes:
        product (Product): The product on this order line
        quantity (int): The quantity ordered
        unit_price (float): The price per unit at the time of order
    """
    
    def __init__(self, product: Product, quantity: int, unit_price: float):
        """
        Initialize an OrderLine object.
        
        Args:
            product: Product object
            quantity: Quantity ordered
            unit_price: Price per unit at the time of order
        """
        self.product = product
        self.quantity = quantity
        self.unit_price = unit_price
    
    def get_line_total(self) -> float:
        """Calculate the total for this order line."""
        return self.unit_price * self.quantity
    
    def to_dict(self) -> dict:
        """Convert OrderLine to dictionary for JSON serialization."""
        return {
            "product_id": self.product.product_id,
            "product_name": self.product.name,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "line_total": self.get_line_total()
        }
    
    def __str__(self) -> str:
        """String representation of order line."""
        return f"{self.product.name} x{self.quantity} @ ${self.unit_price:.2f} = ${self.get_line_total():.2f}"


class Order:
    """
    Represents a customer order.
    
    Attributes:
        order_id (str): Unique order identifier
        customer_id (str): The customer who placed this order
        order_lines (List[OrderLine]): Line items in the order
        subtotal (float): Subtotal before tax and shipping
        tax_amount (float): Tax amount
        shipping_cost (float): Shipping cost
        total_amount (float): Final total amount
        status (str): Order status (e.g., "Pending", "Paid", "Shipped")
        created_at (datetime): Order creation timestamp
        invoice (Invoice): Associated invoice (if any)
        shipment (Shipment): Associated shipment (if any)
    """
    
    def __init__(self, customer_id: str):
        """
        Initialize an Order object.
        
        Args:
            customer_id: The ID of the customer placing the order
        """
        self.order_id = str(uuid.uuid4())
        self.customer_id = customer_id
        self.order_lines: List[OrderLine] = []
        self.subtotal = 0.0
        self.tax_amount = 0.0
        self.shipping_cost = 0.0
        self.total_amount = 0.0
        self.status = "Pending"
        self.created_at = datetime.now().isoformat()
        self.invoice: Optional['Invoice'] = None
        self.shipment: Optional['Shipment'] = None
    
    def add_line(self, order_line: OrderLine) -> None:
        """
        Add a line item to the order.
        
        Args:
            order_line: OrderLine object to add
        """
        self.order_lines.append(order_line)
    
    def calculate_totals(self, tax_rate: float, shipping_cost: float) -> None:
        """
        Calculate order totals including tax and shipping.
        
        Args:
            tax_rate: Tax rate as a decimal (e.g., 0.10 for 10%)
            shipping_cost: Shipping cost amount
        """
        self.subtotal = sum(line.get_line_total() for line in self.order_lines)
        self.tax_amount = self.subtotal * tax_rate
        self.shipping_cost = shipping_cost
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_cost
    
    def set_status(self, status: str) -> None:
        """
        Update the order status.
        
        Args:
            status: New status value
        """
        self.status = status
    
    def to_dict(self) -> dict:
        """Convert Order to dictionary for JSON serialization."""
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "order_lines": [line.to_dict() for line in self.order_lines],
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "shipping_cost": self.shipping_cost,
            "total_amount": self.total_amount,
            "status": self.status,
            "created_at": self.created_at,
            "invoice": self.invoice.to_dict() if self.invoice else None,
            "shipment": self.shipment.to_dict() if self.shipment else None
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Order':
        """Create Order from dictionary (for deserialization)."""
        order = Order(customer_id=data.get("customer_id"))
        order.order_id = data.get("order_id", order.order_id)
        order.status = data.get("status", "Pending")
        order.created_at = data.get("created_at", order.created_at)
        order.subtotal = float(data.get("subtotal", 0))
        order.tax_amount = float(data.get("tax_amount", 0))
        order.shipping_cost = float(data.get("shipping_cost", 0))
        order.total_amount = float(data.get("total_amount", 0))
        
        # Restore invoice if present
        if data.get("invoice"):
            order.invoice = Invoice.from_dict(data.get("invoice"))
        
        # Restore shipment if present
        if data.get("shipment"):
            order.shipment = Shipment.from_dict(data.get("shipment"))
        
        return order
    
    def __str__(self) -> str:
        """String representation of order."""
        return f"Order {self.order_id} - Status: {self.status} - Total: ${self.total_amount:.2f}"


class Invoice:
    """
    Represents an invoice for an order.
    
    Attributes:
        invoice_id (str): Unique invoice identifier
        order_id (str): The associated order ID
        customer_id (str): The customer ID
        invoice_date (datetime): Date the invoice was created
        due_date (datetime): Due date for payment
        items (List[OrderLine]): Line items on the invoice
        subtotal (float): Subtotal amount
        tax_amount (float): Tax amount
        total_amount (float): Total amount due
    """
    
    def __init__(self, order_id: str, customer_id: str, order_lines: List[OrderLine],
                 subtotal: float, tax_amount: float, total_amount: float):
        """
        Initialize an Invoice object.
        
        Args:
            order_id: The associated order ID
            customer_id: The customer ID
            order_lines: Line items from the order
            subtotal: Subtotal amount
            tax_amount: Tax amount
            total_amount: Total amount due
        """
        self.invoice_id = str(uuid.uuid4())
        self.order_id = order_id
        self.customer_id = customer_id
        self.invoice_date = datetime.now().isoformat()
        # Due date is 30 days from invoice date (simplified)
        self.due_date = datetime.now().isoformat()
        self.items = order_lines
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.total_amount = total_amount
    
    def to_dict(self) -> dict:
        """Convert Invoice to dictionary for JSON serialization."""
        return {
            "invoice_id": self.invoice_id,
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "invoice_date": self.invoice_date,
            "due_date": self.due_date,
            "items": [item.to_dict() for item in self.items],
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "total_amount": self.total_amount
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Invoice':
        """Create Invoice from dictionary (for deserialization)."""
        invoice = Invoice(
            order_id=data.get("order_id"),
            customer_id=data.get("customer_id"),
            order_lines=[],
            subtotal=float(data.get("subtotal", 0)),
            tax_amount=float(data.get("tax_amount", 0)),
            total_amount=float(data.get("total_amount", 0))
        )
        invoice.invoice_id = data.get("invoice_id", invoice.invoice_id)
        invoice.invoice_date = data.get("invoice_date", invoice.invoice_date)
        invoice.due_date = data.get("due_date", invoice.due_date)
        return invoice
    
    def __str__(self) -> str:
        """String representation of invoice."""
        return f"Invoice {self.invoice_id} - Order {self.order_id} - ${self.total_amount:.2f}"


class Shipment:
    """
    Represents shipment information for an order.
    
    Attributes:
        shipment_id (str): Unique shipment identifier
        order_id (str): The associated order ID
        tracking_number (str): Tracking number for shipment
        status (str): Current shipment status
        created_at (datetime): When shipment was created
    """
    
    def __init__(self, order_id: str):
        """
        Initialize a Shipment object.
        
        Args:
            order_id: The associated order ID
        """
        self.shipment_id = str(uuid.uuid4())
        self.order_id = order_id
        # Generate a mock tracking number
        self.tracking_number = f"TRACK-{self.shipment_id[:8].upper()}"
        self.status = "Pending"
        self.created_at = datetime.now().isoformat()
    
    def get_latest_status(self) -> str:
        """
        Get the latest status from the carrier (using CarrierAdapter).
        
        In this mock implementation, we return a fixed status.
        In production, this would call an actual carrier API through the adapter.
        
        Returns:
            Current shipment status
        """
        # This will be enhanced by CarrierAdapter in services module
        return self.status
    
    def to_dict(self) -> dict:
        """Convert Shipment to dictionary for JSON serialization."""
        return {
            "shipment_id": self.shipment_id,
            "order_id": self.order_id,
            "tracking_number": self.tracking_number,
            "status": self.status,
            "created_at": self.created_at
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Shipment':
        """Create Shipment from dictionary (for deserialization)."""
        shipment = Shipment(order_id=data.get("order_id"))
        shipment.shipment_id = data.get("shipment_id", shipment.shipment_id)
        shipment.tracking_number = data.get("tracking_number", shipment.tracking_number)
        shipment.status = data.get("status", "Pending")
        shipment.created_at = data.get("created_at", shipment.created_at)
        return shipment
    
    def __str__(self) -> str:
        """String representation of shipment."""
        return f"Shipment {self.shipment_id} - Tracking: {self.tracking_number} - Status: {self.status}"
