"""
Services Module - Business Logic and External Service Integration

This module implements various services that handle business logic:
- AuthenticationService: Handles user registration and login
- CatalogueService: Manages the product catalogue
- PricingService: Calculates order totals with taxes and shipping
- PaymentService: Handles payment processing
- PaymentGateway: Strategy pattern for different payment methods
- CarrierAdapter: Adapter pattern for carrier tracking information

Following PEP 8 style guide and implementing design patterns:
- Strategy Pattern (for payment methods)
- Adapter Pattern (for carrier integration)
- Service Pattern (for business logic)
"""

from typing import List, Optional, Tuple
from abc import ABC, abstractmethod
from src.models import (
    Customer, Product, ShoppingCart, Order, OrderLine, 
    Invoice, Shipment, Address
)
from src.repositories import CustomerRepository, ProductRepository, OrderRepository


class AuthenticationService:
    """
    Service for handling user authentication.
    
    Manages customer registration, login, and session management.
    In production, passwords should be hashed using bcrypt or similar.
    """
    
    def __init__(self, customer_repo: CustomerRepository):
        """
        Initialize AuthenticationService.
        
        Args:
            customer_repo: CustomerRepository instance for data access
        """
        self.customer_repo = customer_repo
    
    def register(self, name: str, email: str, password: str, 
                 street: str, city: str, postal_code: str, country: str) -> Tuple[bool, str]:
        """
        Register a new customer.
        
        Args:
            name: Customer's full name
            email: Customer's email address
            password: Customer's password
            street: Street address
            city: City name
            postal_code: Postal/ZIP code
            country: Country name
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Check if email already exists
        existing_customer = self.customer_repo.find_by_email(email)
        if existing_customer:
            return False, f"Email '{email}' is already registered."
        
        # Create new customer with address
        address = Address(street, city, postal_code, country)
        new_customer = Customer(name, email, password, address)
        
        # Save to repository
        self.customer_repo.save(new_customer)
        
        return True, f"Customer registered successfully! Customer ID: {new_customer.customer_id}"
    
    def login(self, email: str, password: str) -> Tuple[Optional[Customer], str]:
        """
        Authenticate a customer login.
        
        Args:
            email: Customer's email address
            password: Customer's password
            
        Returns:
            Tuple of (customer: Optional[Customer], message: str)
        """
        customer = self.customer_repo.find_by_email(email)
        
        if not customer:
            return None, f"Email '{email}' is not registered."
        
        # Simple password check (in production, use bcrypt)
        if customer.password != password:
            return None, "Incorrect password."
        
        return customer, "Login successful!"


class CatalogueService:
    """
    Service for managing the product catalogue.
    
    Handles browsing, searching, and managing products.
    """
    
    def __init__(self, product_repo: ProductRepository):
        """
        Initialize CatalogueService.
        
        Args:
            product_repo: ProductRepository instance for data access
        """
        self.product_repo = product_repo
    
    def get_all_products(self) -> List[Product]:
        """
        Get all available products.
        
        Returns:
            List of all Product objects
        """
        return self.product_repo.get_all()
    
    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """
        Get a product by its ID.
        
        Args:
            product_id: The product ID to search for
            
        Returns:
            Product object if found, None otherwise
        """
        return self.product_repo.find_by_id(product_id)
    
    def add_product(self, name: str, description: str, price: float, 
                    quantity: int) -> Tuple[Product, str]:
        """
        Add a new product to the catalogue.
        
        Args:
            name: Product name
            description: Product description
            price: Product price
            quantity: Available quantity
            
        Returns:
            Tuple of (product: Product, message: str)
        """
        product = Product(name, description, price, quantity)
        self.product_repo.save(product)
        return product, f"Product '{name}' added successfully!"
    
    def display_catalogue(self) -> None:
        """Display all products in a formatted manner."""
        products = self.get_all_products()
        
        if not products:
            print("No products available in the catalogue.")
            return
        
        print("\n" + "="*60)
        print("PRODUCT CATALOGUE")
        print("="*60)
        
        for i, product in enumerate(products, 1):
            print(f"\n[{i}] {product.name}")
            print(f"    ID: {product.product_id}")
            print(f"    Price: ${product.price:.2f}")
            print(f"    Description: {product.description}")
            print(f"    Available: {product.quantity_available} units")
        
        print("\n" + "="*60)


class PricingService:
    """
    Service for calculating order prices.
    
    Handles tax calculations, shipping costs, and total calculations.
    Implements pricing rules and discounts.
    """
    
    def __init__(self, tax_rate: float, shipping_cost: float):
        """
        Initialize PricingService.
        
        Args:
            tax_rate: Tax rate as a decimal (e.g., 0.10 for 10%)
            shipping_cost: Standard shipping cost
        """
        self.tax_rate = tax_rate
        self.shipping_cost = shipping_cost
    
    def calculate_order_total(self, order: Order) -> None:
        """
        Calculate the total for an order including tax and shipping.
        
        Args:
            order: Order object to calculate totals for
        """
        order.calculate_totals(self.tax_rate, self.shipping_cost)
    
    def get_tax_amount(self, subtotal: float) -> float:
        """
        Calculate tax amount for a subtotal.
        
        Args:
            subtotal: The subtotal amount
            
        Returns:
            Tax amount
        """
        return subtotal * self.tax_rate
    
    def get_total_with_tax_and_shipping(self, subtotal: float) -> float:
        """
        Calculate total including tax and shipping.
        
        Args:
            subtotal: The subtotal amount
            
        Returns:
            Total amount with tax and shipping
        """
        tax = self.get_tax_amount(subtotal)
        return subtotal + tax + self.shipping_cost


class PaymentGateway(ABC):
    """
    Abstract base class for payment gateways.
    
    Implements the Strategy Pattern for different payment methods.
    Subclasses must implement the process_payment method.
    """
    
    @abstractmethod
    def process_payment(self, amount: float, order_id: str) -> Tuple[bool, str]:
        """
        Process a payment.
        
        Args:
            amount: The payment amount
            order_id: The order ID for reference
            
        Returns:
            Tuple of (success: bool, transaction_id: str)
        """
        pass


class CreditCardGateway(PaymentGateway):
    """
    Credit card payment gateway (mock implementation).
    
    In production, this would integrate with a real payment processor
    like Stripe or PayPal.
    """
    
    def process_payment(self, amount: float, order_id: str) -> Tuple[bool, str]:
        """
        Process a credit card payment.
        
        Args:
            amount: The payment amount
            order_id: The order ID for reference
            
        Returns:
            Tuple of (success: bool, transaction_id: str)
        """
        print(f"Processing credit card payment of ${amount:.2f}...")
        # Mock processing
        transaction_id = f"CC-{order_id[:8]}-SUCCESS"
        return True, transaction_id


class DigitalWalletGateway(PaymentGateway):
    """
    Digital wallet payment gateway (mock implementation).
    
    Represents payment methods like Apple Pay, Google Pay, etc.
    """
    
    def process_payment(self, amount: float, order_id: str) -> Tuple[bool, str]:
        """
        Process a digital wallet payment.
        
        Args:
            amount: The payment amount
            order_id: The order ID for reference
            
        Returns:
            Tuple of (success: bool, transaction_id: str)
        """
        print(f"Processing digital wallet payment of ${amount:.2f}...")
        # Mock processing
        transaction_id = f"DW-{order_id[:8]}-SUCCESS"
        return True, transaction_id


class BankTransferGateway(PaymentGateway):
    """
    Bank transfer payment gateway (mock implementation).
    
    Represents payment via bank transfer or wire transfer.
    """
    
    def process_payment(self, amount: float, order_id: str) -> Tuple[bool, str]:
        """
        Process a bank transfer payment.
        
        Args:
            amount: The payment amount
            order_id: The order ID for reference
            
        Returns:
            Tuple of (success: bool, transaction_id: str)
        """
        print(f"Processing bank transfer of ${amount:.2f}...")
        # Mock processing
        transaction_id = f"BT-{order_id[:8]}-SUCCESS"
        return True, transaction_id


class PaymentService:
    """
    Service for handling payment processing.
    
    Coordinates with different payment gateways using the Strategy pattern.
    """
    
    def __init__(self):
        """Initialize PaymentService with available payment methods."""
        self.payment_gateways = {
            "credit_card": CreditCardGateway(),
            "digital_wallet": DigitalWalletGateway(),
            "bank_transfer": BankTransferGateway()
        }
    
    def process_order_payment(self, order: Order, payment_method: str) -> Tuple[bool, str]:
        """
        Process payment for an order using the specified payment method.
        
        Args:
            order: The Order object to pay for
            payment_method: The payment method to use
            
        Returns:
            Tuple of (success: bool, transaction_id: str)
        """
        # Validate payment method
        if payment_method not in self.payment_gateways:
            return False, f"Invalid payment method: {payment_method}"
        
        # Get the appropriate gateway
        gateway = self.payment_gateways[payment_method]
        
        # Process the payment
        success, transaction_id = gateway.process_payment(order.total_amount, order.order_id)
        
        if success:
            print(f"Payment approved! Transaction ID: {transaction_id}")
        else:
            print(f"Payment failed! Transaction ID: {transaction_id}")
        
        return success, transaction_id
    
    def get_available_payment_methods(self) -> List[str]:
        """
        Get list of available payment methods.
        
        Returns:
            List of payment method names
        """
        return list(self.payment_gateways.keys())


class CarrierAdapter:
    """
    Adapter for carrier tracking information.
    
    Adapter Pattern: Adapts external carrier APIs to our internal interface.
    In this mock implementation, it simulates carrier responses.
    In production, this would integrate with real carrier APIs
    like FedEx, UPS, DHL, etc.
    """
    
    def __init__(self):
        """Initialize CarrierAdapter."""
        # Mock carrier statuses
        self.mock_statuses = [
            "Order Confirmed",
            "Processing",
            "Shipped",
            "In Transit",
            "Out for Delivery",
            "Delivered"
        ]
    
    def get_tracking_info(self, tracking_number: str) -> Tuple[str, str]:
        """
        Get tracking information from the carrier.
        
        Args:
            tracking_number: The tracking number to lookup
            
        Returns:
            Tuple of (status: str, estimated_delivery: str)
        """
        # Mock: simulate a carrier lookup
        # In production, this would call real carrier APIs
        
        # Use tracking number to generate consistent mock status
        # (normally would query actual carrier)
        status_index = hash(tracking_number) % len(self.mock_statuses)
        status = self.mock_statuses[status_index]
        
        # Mock estimated delivery date
        estimated_delivery = "2025-11-15"
        
        return status, estimated_delivery
    
    def update_shipment_status(self, shipment: 'Shipment') -> str:
        """
        Update shipment status from carrier.
        
        Args:
            shipment: The Shipment object to update
            
        Returns:
            Updated status string
        """
        status, _ = self.get_tracking_info(shipment.tracking_number)
        shipment.status = status
        return status
