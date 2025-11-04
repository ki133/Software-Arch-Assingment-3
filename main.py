"""
Main Application Module - Entry Point

This module is the main entry point for the e-commerce system.
It initializes all services, repositories, and starts the main menu loop.

Usage:
    python main.py

Following PEP 8 style guide: https://peps.python.org/pep-0008/
"""

import sys
from pathlib import Path

# Add the project root to the Python path so imports work correctly
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.config import (
    USERS_FILE, PRODUCTS_FILE, ORDERS_FILE,
    TAX_RATE, SHIPPING_COST, APP_NAME, APP_VERSION, CURRENCY
)
from src.repositories import CustomerRepository, ProductRepository, OrderRepository
from src.ui import ApplicationController
from src.init_data import initialize_sample_products, initialize_sample_customers
from src.validators import InputValidator


class MainApplication:
    """
    Main application class that manages the application lifecycle.
    
    This class is responsible for:
    - Initializing repositories and services
    - Managing the main menu loop
    - Handling user interactions
    """
    
    def __init__(self):
        """Initialize the main application."""
        # Initialize repositories with file paths from config
        self.users_repo = CustomerRepository(USERS_FILE)
        self.products_repo = ProductRepository(PRODUCTS_FILE)
        self.orders_repo = OrderRepository(ORDERS_FILE)
        
        # Initialize the application controller
        self.controller = ApplicationController(
            users_repo=self.users_repo,
            products_repo=self.products_repo,
            orders_repo=self.orders_repo,
            tax_rate=TAX_RATE,
            shipping_cost=SHIPPING_COST
        )
        
        self.validator = InputValidator()
        self.running = True
    
    def display_main_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "="*60)
        print(f"{APP_NAME} v{APP_VERSION}")
        print("="*60)
        
        if self.controller.current_user:
            print(f"\n📧 Logged in as: {self.controller.current_user.name}")
            print("\n1.  Browse Products")
            print("2.  View Shopping Cart")
            print("3.  Add to Cart")
            print("4.  Manage Cart Items")
            print("5.  Checkout")
            print("6.  View Order History")
            print("7.  View Order Details")
            print("8.  Track Shipment")
            print("9.  Logout")
            print("0.  Exit")
        else:
            print("\n🔒 You are not logged in")
            print("\n1.  Register")
            print("2.  Login")
            print("0.  Exit")
        
        print("="*60)
    
    def run_authenticated_menu(self) -> None:
        """Run the main menu for authenticated users."""
        while self.running and self.controller.current_user:
            self.display_main_menu()
            
            max_option = 9
            while True:
                choice_str = input("\nSelect an option: ").strip()
                is_valid, choice, error_msg = self.validator.validate_menu_choice(choice_str, max_option + 1)
                if is_valid and (choice == 0 or choice <= max_option):
                    break
                print(f"❌ {error_msg}")
            
            if choice == 0:
                self.running = False
                break
            
            elif choice == 1:
                self.controller.display_products()
            
            elif choice == 2:
                self.controller.view_cart()
            
            elif choice == 3:
                self.controller.add_to_cart()
            
            elif choice == 4:
                self.controller.manage_cart_items()
            
            elif choice == 5:
                self.controller.checkout()
            
            elif choice == 6:
                self.controller.view_order_history()
            
            elif choice == 7:
                self.controller.view_order_details()
            
            elif choice == 8:
                self.controller.track_shipment()
            
            elif choice == 9:
                self.controller.logout_user()
                break
    
    def run_unauthenticated_menu(self) -> None:
        """Run the main menu for unauthenticated users."""
        while self.running and not self.controller.current_user:
            self.display_main_menu()
            
            while True:
                choice_str = input("\nSelect an option: ").strip()
                is_valid, choice, error_msg = self.validator.validate_menu_choice(choice_str, 2)
                if is_valid and (choice == 0 or choice == 1 or choice == 2):
                    break
                print(f"❌ {error_msg}")
            
            if choice == 0:
                self.running = False
                break
            
            elif choice == 1:
                self.controller.register_user()
                # After registration, ask if user wants to login
                login_response = input("\nWould you like to login now? (yes/no): ").strip().lower()
                if login_response in ['yes', 'y']:
                    self.controller.login_user()
                    if self.controller.current_user:
                        break
            
            elif choice == 2:
                self.controller.login_user()
                if self.controller.current_user:
                    break
    
    def run(self) -> None:
        """Run the main application loop."""
        print("\n" + "="*60)
        print("Welcome to the E-Commerce System!")
        print("="*60)
        
        # Initialize sample data
        initialize_sample_products(PRODUCTS_FILE)
        initialize_sample_customers(USERS_FILE)
        
        # Main application loop
        while self.running:
            if self.controller.current_user:
                self.run_authenticated_menu()
            else:
                self.run_unauthenticated_menu()
        
        # Exit message
        print("\n" + "="*60)
        print("Thank you for using the E-Commerce System!")
        print("Goodbye!")
        print("="*60)
        sys.exit(0)


def main() -> None:
    """Entry point for the application."""
    try:
        app = MainApplication()
        app.run()
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("Application interrupted by user.")
        print("Goodbye!")
        print("="*60)
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    """
    Entry point check - this ensures the main() function is only called
    when this script is run directly, not when it's imported as a module.
    """
    main()
