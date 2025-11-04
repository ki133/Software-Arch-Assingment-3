"""
Initialization Module - Data Initialization

This module initializes the application with sample data.
It creates sample products that are used for demonstrations.

This module is run once to populate the products.json file with sample data.
"""

import json
from pathlib import Path
from src.models import Product


def initialize_sample_products(products_file: Path) -> None:
    """
    Initialize the products database with sample products.
    
    Only creates sample data if the products file is empty.
    
    Args:
        products_file: Path to the products JSON file
    """
    # Check if products already exist
    try:
        content = products_file.read_text()
        existing_products = json.loads(content) if content else []
        if existing_products:
            print("Products already exist. Skipping initialization.")
            return
    except (json.JSONDecodeError, FileNotFoundError):
        pass
    
    print("Initializing sample products...")
    
    # Create sample products
    sample_products = [
        Product(
            name="Laptop Computer",
            description="High-performance laptop for work and gaming",
            price=1299.99,
            quantity_available=15
        ),
        Product(
            name="Wireless Mouse",
            description="Ergonomic wireless mouse with silent clicking",
            price=29.99,
            quantity_available=50
        ),
        Product(
            name="USB-C Keyboard",
            description="Mechanical keyboard with USB-C connection",
            price=79.99,
            quantity_available=30
        ),
        Product(
            name="Monitor 27-inch",
            description="4K LED monitor with HDR support",
            price=349.99,
            quantity_available=20
        ),
        Product(
            name="Webcam HD",
            description="1080p HD webcam with auto-focus",
            price=59.99,
            quantity_available=40
        ),
        Product(
            name="Headphones",
            description="Noise-cancelling wireless headphones",
            price=149.99,
            quantity_available=25
        ),
        Product(
            name="Phone Stand",
            description="Adjustable phone stand for desk",
            price=14.99,
            quantity_available=100
        ),
        Product(
            name="USB Hub",
            description="7-port USB 3.0 hub with power adapter",
            price=39.99,
            quantity_available=35
        ),
    ]
    
    # Convert to dictionaries for JSON serialization
    products_data = [product.to_dict() for product in sample_products]
    
    # Write to file
    products_file.write_text(json.dumps(products_data, indent=2))
    
    print(f"{len(sample_products)} sample products created successfully!")


def initialize_sample_customers(customers_file: Path) -> None:
    """
    Initialize the customers database with a sample customer (optional).
    
    This is optional - users can register during normal operation.
    
    Args:
        customers_file: Path to the customers JSON file
    """
    # Check if customers already exist
    try:
        content = customers_file.read_text()
        existing_customers = json.loads(content) if content else []
        if existing_customers:
            print("Customers already exist. Skipping initialization.")
            return
    except (json.JSONDecodeError, FileNotFoundError):
        pass
    
    print("No sample customers created. Users can register during normal operation.")
