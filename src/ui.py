"""
UI Module - Console User Interface Controller

This module implements the main application UI and user interaction logic.
It follows the MVC (Model-View-Controller) pattern where:
- Models: Domain classes in models.py
- Views: Display methods in this module
- Controllers: Business logic coordinated through ui.py

Following PEP 8 style guide with extensive comments.
"""

from typing import Optional
from src.models import Customer, ShoppingCart, Order, OrderLine, Invoice, Shipment
from src.repositories import CustomerRepository, ProductRepository, OrderRepository
from src.services import (
    AuthenticationService, CatalogueService, PricingService,
    PaymentService, CarrierAdapter
)
from src.validators import InputValidator


class ApplicationController:
    """
    Main application controller that coordinates all services.
    
    This class acts as the central hub for all application functionality,
    managing the flow between different services and handling user interactions.
    """
    
    def __init__(self, users_repo: CustomerRepository, products_repo: ProductRepository,
                 orders_repo: OrderRepository, tax_rate: float, shipping_cost: float):
        """
        Initialize the ApplicationController.
        
        Args:
            users_repo: CustomerRepository for user data access
            products_repo: ProductRepository for product data access
            orders_repo: OrderRepository for order data access
            tax_rate: Tax rate for pricing calculations
            shipping_cost: Standard shipping cost
        """
        # Initialize repositories
        self.users_repo = users_repo
        self.products_repo = products_repo
        self.orders_repo = orders_repo
        
        # Initialize services
        self.auth_service = AuthenticationService(users_repo)
        self.catalogue_service = CatalogueService(products_repo)
        self.pricing_service = PricingService(tax_rate, shipping_cost)
        self.payment_service = PaymentService()
        self.carrier_adapter = CarrierAdapter()
        
        # Session management
        self.current_user: Optional[Customer] = None
        self.current_cart: Optional[ShoppingCart] = None
        self.validator = InputValidator()
    
    # ========== AUTHENTICATION METHODS ==========
    
    def register_user(self) -> None:
        """
        Handle user registration flow.
        
        Prompts user for registration details and creates a new account.
        Implements input validation for all fields.
        """
        print("\n" + "="*60)
        print("CUSTOMER REGISTRATION")
        print("="*60)
        
        # Get and validate name
        while True:
            name = input("\nEnter your full name: ").strip()
            is_valid, error_msg = self.validator.validate_name(name)
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        # Get and validate email
        while True:
            email = input("Enter your email address: ").strip()
            is_valid, error_msg = self.validator.validate_email(email)
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        # Get and validate password
        while True:
            password = input("Enter a password (min 6 characters): ").strip()
            is_valid, error_msg = self.validator.validate_password(password)
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        # Get and validate address details
        while True:
            street = input("Enter your street address: ").strip()
            is_valid, error_msg = self.validator.validate_street_address(street)
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        while True:
            city = input("Enter your city: ").strip()
            is_valid, error_msg = self.validator.validate_city(city)
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        while True:
            postal_code = input("Enter your postal code: ").strip()
            is_valid, error_msg = self.validator.validate_postal_code(postal_code)
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        while True:
            country = input("Enter your country: ").strip()
            is_valid, error_msg = self.validator.validate_country(country)
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        # Register the user
        success, message = self.auth_service.register(
            name, email, password, street, city, postal_code, country
        )
        
        if success:
            print(f"\n✅ {message}")
        else:
            print(f"\n❌ {message}")
    
    def login_user(self) -> None:
        """
        Handle user login flow.
        
        Prompts user for email and password, authenticates, and
        initializes session if successful.
        """
        print("\n" + "="*60)
        print("CUSTOMER LOGIN")
        print("="*60)
        
        # Get and validate email
        email = input("\nEnter your email address: ").strip()
        is_valid, error_msg = self.validator.validate_email(email)
        if not is_valid:
            print(f"❌ {error_msg}")
            return
        
        # Get password
        password = input("Enter your password: ").strip()
        
        # Authenticate
        customer, message = self.auth_service.login(email, password)
        
        if customer:
            self.current_user = customer
            self.current_cart = ShoppingCart(customer.customer_id)
            print(f"\n✅ {message}")
            print(f"Welcome back, {customer.name}!")
        else:
            print(f"\n❌ {message}")
    
    def logout_user(self) -> None:
        """Log out the current user and clear session."""
        if self.current_user:
            print(f"\nGoodbye, {self.current_user.name}!")
            self.current_user = None
            self.current_cart = None
        else:
            print("\nYou are not logged in.")
    
    # ========== PRODUCT BROWSING METHODS ==========
    
    def display_products(self) -> None:
        """Display all available products in the catalogue."""
        if not self.current_user:
            print("\n❌ You must be logged in to view products.")
            return
        
        self.catalogue_service.display_catalogue()
    
    # ========== SHOPPING CART METHODS ==========
    
    def add_to_cart(self) -> None:
        """
        Add a product to the shopping cart.
        
        Prompts user for product ID and quantity with validation.
        """
        if not self.current_user or not self.current_cart:
            print("\n❌ You must be logged in to use the shopping cart.")
            return
        
        print("\n" + "="*60)
        print("ADD TO SHOPPING CART")
        print("="*60)
        
        # Get and validate product ID
        while True:
            product_id = input("\nEnter product ID: ").strip()
            is_valid, error_msg = self.validator.validate_product_id(product_id)
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        # Find the product
        product = self.catalogue_service.get_product_by_id(product_id)
        if not product:
            print(f"❌ Product with ID '{product_id}' not found.")
            return
        
        # Get and validate quantity
        while True:
            quantity_str = input(f"Enter quantity (Available: {product.quantity_available}): ").strip()
            is_valid, quantity, error_msg = self.validator.validate_quantity(quantity_str)
            if not is_valid:
                print(f"❌ {error_msg}")
                continue
            
            if quantity > product.quantity_available:
                print(f"❌ Only {product.quantity_available} units available.")
                continue
            
            break
        
        # Add to cart
        self.current_cart.add_item(product, quantity)
        print(f"\n✅ Added {quantity}x {product.name} to cart!")
        print(f"   Subtotal: ${self.current_cart.get_subtotal():.2f}")
    
    def view_cart(self) -> None:
        """Display the contents of the shopping cart."""
        if not self.current_user or not self.current_cart:
            print("\n❌ You must be logged in to view the cart.")
            return
        
        if self.current_cart.is_empty():
            print("\n" + "="*60)
            print("SHOPPING CART")
            print("="*60)
            print("\nYour shopping cart is empty.")
            return
        
        print("\n" + "="*60)
        print("SHOPPING CART")
        print("="*60)
        print(f"\nCustomer: {self.current_user.name}")
        print("-"*60)
        
        for i, item in enumerate(self.current_cart.items, 1):
            print(f"\n[{i}] {item.product.name}")
            print(f"    Quantity: {item.quantity}")
            print(f"    Unit Price: ${item.product.price:.2f}")
            print(f"    Subtotal: ${item.get_subtotal():.2f}")
        
        subtotal = self.current_cart.get_subtotal()
        tax = self.pricing_service.get_tax_amount(subtotal)
        total = subtotal + tax + self.pricing_service.shipping_cost
        
        print("\n" + "-"*60)
        print(f"Subtotal:        ${subtotal:.2f}")
        print(f"Tax (10%):       ${tax:.2f}")
        print(f"Shipping:        ${self.pricing_service.shipping_cost:.2f}")
        print(f"TOTAL:           ${total:.2f}")
        print("="*60)
    
    def manage_cart_items(self) -> None:
        """
        Manage cart items (update quantity or remove).
        
        Allows user to modify or delete items in the cart.
        """
        if not self.current_user or not self.current_cart:
            print("\n❌ You must be logged in to manage cart items.")
            return
        
        if self.current_cart.is_empty():
            print("\n❌ Your shopping cart is empty.")
            return
        
        print("\n" + "="*60)
        print("MANAGE CART ITEMS")
        print("="*60)
        
        # Display items with numbers
        for i, item in enumerate(self.current_cart.items, 1):
            print(f"[{i}] {item.product.name} (x{item.quantity}) - ${item.get_subtotal():.2f}")
        
        # Get item selection
        while True:
            choice_str = input(f"\nSelect item (1-{len(self.current_cart.items)}): ").strip()
            is_valid, choice, error_msg = self.validator.validate_menu_choice(
                choice_str, len(self.current_cart.items)
            )
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        selected_item = self.current_cart.items[choice - 1]
        
        print("\n1. Update Quantity")
        print("2. Remove Item")
        
        while True:
            action_str = input("\nSelect action (1-2): ").strip()
            is_valid, action, error_msg = self.validator.validate_menu_choice(action_str, 2)
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        if action == 1:
            # Update quantity
            while True:
                new_qty_str = input("Enter new quantity: ").strip()
                is_valid, new_qty, error_msg = self.validator.validate_quantity(new_qty_str)
                if not is_valid:
                    print(f"❌ {error_msg}")
                    continue
                break
            
            self.current_cart.update_item_quantity(selected_item.product.product_id, new_qty)
            print(f"✅ Quantity updated to {new_qty}")
        
        elif action == 2:
            # Remove item
            self.current_cart.remove_item(selected_item.product.product_id)
            print(f"✅ Item removed from cart")
    
    # ========== CHECKOUT AND PAYMENT METHODS ==========
    
    def checkout(self) -> None:
        """
        Handle checkout process.
        
        Follows the sequence diagram 7.1:
        ShoppingCart -> Order -> OrderLine -> PricingService -> PaymentService
        """
        if not self.current_user or not self.current_cart:
            print("\n❌ You must be logged in to checkout.")
            return
        
        if self.current_cart.is_empty():
            print("\n❌ Your shopping cart is empty. Add items before checking out.")
            return
        
        print("\n" + "="*60)
        print("CHECKOUT")
        print("="*60)
        
        # Step 1: Create Order from ShoppingCart
        print("\nCreating order...")
        order = Order(self.current_user.customer_id)
        
        # Step 2: Convert CartItems to OrderLines
        for cart_item in self.current_cart.items:
            order_line = OrderLine(
                product=cart_item.product,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price
            )
            order.add_line(order_line)
        
        # Step 3: Calculate totals with PricingService
        self.pricing_service.calculate_order_total(order)
        
        # Display order summary
        print("\nOrder Summary:")
        print("-"*60)
        for line in order.order_lines:
            print(f"  {line}")
        print("-"*60)
        print(f"Subtotal:      ${order.subtotal:.2f}")
        print(f"Tax (10%):     ${order.tax_amount:.2f}")
        print(f"Shipping:      ${order.shipping_cost:.2f}")
        print(f"TOTAL:         ${order.total_amount:.2f}")
        print("-"*60)
        
        # Step 4: Process payment
        print("\nSelect payment method:")
        payment_methods = self.payment_service.get_available_payment_methods()
        for i, method in enumerate(payment_methods, 1):
            print(f"{i}. {method.replace('_', ' ').title()}")
        
        while True:
            choice_str = input(f"\nSelect payment method (1-{len(payment_methods)}): ").strip()
            is_valid, choice, error_msg = self.validator.validate_menu_choice(
                choice_str, len(payment_methods)
            )
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        selected_method = payment_methods[choice - 1]
        
        # Process payment
        print(f"\nProcessing payment with {selected_method.replace('_', ' ').title()}...")
        success, transaction_id = self.payment_service.process_order_payment(order, selected_method)
        
        if not success:
            print("\n❌ Payment failed. Order not completed.")
            return
        
        # Step 5: Update order status
        order.set_status("Paid")
        print("✅ Payment successful!")
        
        # Step 6: Create Invoice
        print("\nGenerating invoice...")
        invoice = Invoice(
            order_id=order.order_id,
            customer_id=order.customer_id,
            order_lines=order.order_lines,
            subtotal=order.subtotal,
            tax_amount=order.tax_amount,
            total_amount=order.total_amount
        )
        order.invoice = invoice
        
        # Step 7: Create Shipment
        print("Creating shipment...")
        shipment = Shipment(order.order_id)
        order.shipment = shipment
        
        # Step 8: Save order to repository
        self.orders_repo.save(order)
        
        # Step 9: Clear shopping cart
        self.current_cart.clear()
        
        print("\n" + "="*60)
        print("✅ ORDER COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"Order ID: {order.order_id}")
        print(f"Invoice ID: {invoice.invoice_id}")
        print(f"Shipment Tracking: {shipment.tracking_number}")
        print("="*60)
    
    # ========== ORDER HISTORY METHODS ==========
    
    def view_order_history(self) -> None:
        """
        View all orders for the current user.
        
        Loads orders from repository and displays them.
        """
        if not self.current_user:
            print("\n❌ You must be logged in to view order history.")
            return
        
        orders = self.orders_repo.find_by_customer_id(self.current_user.customer_id)
        
        if not orders:
            print("\n" + "="*60)
            print("ORDER HISTORY")
            print("="*60)
            print("\nYou have no orders yet.")
            return
        
        print("\n" + "="*60)
        print("ORDER HISTORY")
        print("="*60)
        print(f"\nCustomer: {self.current_user.name}")
        print("-"*60)
        
        for i, order in enumerate(orders, 1):
            print(f"\n[{i}] Order ID: {order.order_id}")
            print(f"    Date: {order.created_at}")
            print(f"    Status: {order.status}")
            print(f"    Total: ${order.total_amount:.2f}")
        
        print("\n" + "="*60)
    
    def view_order_details(self) -> None:
        """
        View details of a specific order.
        
        Allows user to select an order and view full details including
        invoice and shipment information.
        """
        if not self.current_user:
            print("\n❌ You must be logged in to view order details.")
            return
        
        orders = self.orders_repo.find_by_customer_id(self.current_user.customer_id)
        
        if not orders:
            print("\n❌ You have no orders.")
            return
        
        print("\n" + "="*60)
        print("SELECT ORDER")
        print("="*60)
        
        for i, order in enumerate(orders, 1):
            print(f"[{i}] Order {order.order_id} - ${order.total_amount:.2f}")
        
        while True:
            choice_str = input(f"\nSelect order (1-{len(orders)}): ").strip()
            is_valid, choice, error_msg = self.validator.validate_menu_choice(choice_str, len(orders))
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        selected_order = orders[choice - 1]
        
        # Display order details
        print("\n" + "="*60)
        print("ORDER DETAILS")
        print("="*60)
        print(f"\nOrder ID: {selected_order.order_id}")
        print(f"Created: {selected_order.created_at}")
        print(f"Status: {selected_order.status}")
        print("\nItems:")
        print("-"*60)
        
        for line in selected_order.order_lines:
            print(f"  {line}")
        
        print("-"*60)
        print(f"Subtotal:      ${selected_order.subtotal:.2f}")
        print(f"Tax:           ${selected_order.tax_amount:.2f}")
        print(f"Shipping:      ${selected_order.shipping_cost:.2f}")
        print(f"TOTAL:         ${selected_order.total_amount:.2f}")
        
        # Display invoice if available
        if selected_order.invoice:
            print("\n" + "-"*60)
            print("INVOICE")
            print("-"*60)
            print(f"Invoice ID: {selected_order.invoice.invoice_id}")
            print(f"Invoice Date: {selected_order.invoice.invoice_date}")
            print(f"Due Date: {selected_order.invoice.due_date}")
        
        # Display shipment if available
        if selected_order.shipment:
            print("\n" + "-"*60)
            print("SHIPMENT")
            print("-"*60)
            print(f"Tracking Number: {selected_order.shipment.tracking_number}")
            print(f"Status: {selected_order.shipment.status}")
        
        print("\n" + "="*60)
    
    def track_shipment(self) -> None:
        """
        Track shipment of an order.
        
        Displays tracking information and estimated delivery using
        the CarrierAdapter to fetch current status.
        """
        if not self.current_user:
            print("\n❌ You must be logged in to track shipments.")
            return
        
        orders = self.orders_repo.find_by_customer_id(self.current_user.customer_id)
        
        # Filter orders that have shipments
        orders_with_shipments = [o for o in orders if o.shipment]
        
        if not orders_with_shipments:
            print("\n❌ You have no shipments to track.")
            return
        
        print("\n" + "="*60)
        print("TRACK SHIPMENT")
        print("="*60)
        
        for i, order in enumerate(orders_with_shipments, 1):
            print(f"[{i}] Order {order.order_id} - Tracking: {order.shipment.tracking_number}")
        
        while True:
            choice_str = input(f"\nSelect order (1-{len(orders_with_shipments)}): ").strip()
            is_valid, choice, error_msg = self.validator.validate_menu_choice(
                choice_str, len(orders_with_shipments)
            )
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        selected_order = orders_with_shipments[choice - 1]
        shipment = selected_order.shipment
        
        # Get tracking info from carrier adapter
        status, estimated_delivery = self.carrier_adapter.get_tracking_info(shipment.tracking_number)
        
        print("\n" + "="*60)
        print("TRACKING INFORMATION")
        print("="*60)
        print(f"\nOrder ID: {selected_order.order_id}")
        print(f"Tracking Number: {shipment.tracking_number}")
        print(f"Current Status: {status}")
        print(f"Estimated Delivery: {estimated_delivery}")
        print("="*60)
