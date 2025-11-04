"""
Repository Module - Data Access Layer

This module implements the Repository Pattern for data persistence.
It handles reading and writing domain objects to JSON files.

Classes:
- CustomerRepository: Manages customer data persistence
- ProductRepository: Manages product data persistence
- OrderRepository: Manages order data persistence

Following PEP 8 style guide and Repository Pattern design.
"""

import json
from pathlib import Path
from typing import List, Optional
from src.models import Customer, Product, Order


class CustomerRepository:
    """
    Repository for managing customer data persistence.
    
    Implements CRUD operations (Create, Read, Update, Delete) for customers.
    Uses JSON files as the storage mechanism.
    """
    
    def __init__(self, file_path: Path):
        """
        Initialize CustomerRepository.
        
        Args:
            file_path: Path to the JSON file for storing customers
        """
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Ensure the JSON file exists. Create if it doesn't."""
        if not self.file_path.exists():
            self.file_path.write_text(json.dumps([], indent=2))
    
    def save(self, customer: Customer) -> None:
        """
        Save a customer to the repository.
        
        If customer already exists (same email), update it.
        Otherwise, create a new entry.
        
        Args:
            customer: Customer object to save
        """
        customers = self._load_all()
        
        # Check if customer already exists
        for i, c in enumerate(customers):
            if c.get("email") == customer.email:
                customers[i] = customer.to_dict()
                self._write_all(customers)
                return
        
        # New customer, add it
        customers.append(customer.to_dict())
        self._write_all(customers)
    
    def find_by_email(self, email: str) -> Optional[Customer]:
        """
        Find a customer by email.
        
        Args:
            email: Customer email to search for
            
        Returns:
            Customer object if found, None otherwise
        """
        customers = self._load_all()
        for c in customers:
            if c.get("email") == email:
                return Customer.from_dict(c)
        return None
    
    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        """
        Find a customer by ID.
        
        Args:
            customer_id: Customer ID to search for
            
        Returns:
            Customer object if found, None otherwise
        """
        customers = self._load_all()
        for c in customers:
            if c.get("customer_id") == customer_id:
                return Customer.from_dict(c)
        return None
    
    def get_all(self) -> List[Customer]:
        """
        Get all customers from the repository.
        
        Returns:
            List of all Customer objects
        """
        customers_data = self._load_all()
        return [Customer.from_dict(c) for c in customers_data]
    
    def delete(self, email: str) -> bool:
        """
        Delete a customer by email.
        
        Args:
            email: Email of customer to delete
            
        Returns:
            True if customer was deleted, False if not found
        """
        customers = self._load_all()
        original_count = len(customers)
        customers = [c for c in customers if c.get("email") != email]
        
        if len(customers) < original_count:
            self._write_all(customers)
            return True
        return False
    
    def _load_all(self) -> List[dict]:
        """
        Load all customers from file.
        
        Returns:
            List of customer dictionaries
        """
        try:
            content = self.file_path.read_text()
            return json.loads(content) if content else []
        except json.JSONDecodeError:
            return []
    
    def _write_all(self, customers: List[dict]) -> None:
        """
        Write all customers to file.
        
        Args:
            customers: List of customer dictionaries to write
        """
        self.file_path.write_text(json.dumps(customers, indent=2))


class ProductRepository:
    """
    Repository for managing product data persistence.
    
    Implements CRUD operations for products.
    Uses JSON files as the storage mechanism.
    """
    
    def __init__(self, file_path: Path):
        """
        Initialize ProductRepository.
        
        Args:
            file_path: Path to the JSON file for storing products
        """
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Ensure the JSON file exists. Create if it doesn't."""
        if not self.file_path.exists():
            self.file_path.write_text(json.dumps([], indent=2))
    
    def save(self, product: Product) -> None:
        """
        Save a product to the repository.
        
        If product already exists (same product_id), update it.
        Otherwise, create a new entry.
        
        Args:
            product: Product object to save
        """
        products = self._load_all()
        
        # Check if product already exists
        for i, p in enumerate(products):
            if p.get("product_id") == product.product_id:
                products[i] = product.to_dict()
                self._write_all(products)
                return
        
        # New product, add it
        products.append(product.to_dict())
        self._write_all(products)
    
    def find_by_id(self, product_id: str) -> Optional[Product]:
        """
        Find a product by ID.
        
        Args:
            product_id: Product ID to search for
            
        Returns:
            Product object if found, None otherwise
        """
        products = self._load_all()
        for p in products:
            if p.get("product_id") == product_id:
                return Product.from_dict(p)
        return None
    
    def get_all(self) -> List[Product]:
        """
        Get all products from the repository.
        
        Returns:
            List of all Product objects
        """
        products_data = self._load_all()
        return [Product.from_dict(p) for p in products_data]
    
    def delete(self, product_id: str) -> bool:
        """
        Delete a product by ID.
        
        Args:
            product_id: ID of product to delete
            
        Returns:
            True if product was deleted, False if not found
        """
        products = self._load_all()
        original_count = len(products)
        products = [p for p in products if p.get("product_id") != product_id]
        
        if len(products) < original_count:
            self._write_all(products)
            return True
        return False
    
    def _load_all(self) -> List[dict]:
        """
        Load all products from file.
        
        Returns:
            List of product dictionaries
        """
        try:
            content = self.file_path.read_text()
            return json.loads(content) if content else []
        except json.JSONDecodeError:
            return []
    
    def _write_all(self, products: List[dict]) -> None:
        """
        Write all products to file.
        
        Args:
            products: List of product dictionaries to write
        """
        self.file_path.write_text(json.dumps(products, indent=2))


class OrderRepository:
    """
    Repository for managing order data persistence.
    
    Implements CRUD operations for orders.
    Uses JSON files as the storage mechanism.
    """
    
    def __init__(self, file_path: Path):
        """
        Initialize OrderRepository.
        
        Args:
            file_path: Path to the JSON file for storing orders
        """
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Ensure the JSON file exists. Create if it doesn't."""
        if not self.file_path.exists():
            self.file_path.write_text(json.dumps([], indent=2))
    
    def save(self, order: Order) -> None:
        """
        Save an order to the repository.
        
        If order already exists (same order_id), update it.
        Otherwise, create a new entry.
        
        Args:
            order: Order object to save
        """
        orders = self._load_all()
        
        # Check if order already exists
        for i, o in enumerate(orders):
            if o.get("order_id") == order.order_id:
                orders[i] = order.to_dict()
                self._write_all(orders)
                return
        
        # New order, add it
        orders.append(order.to_dict())
        self._write_all(orders)
    
    def find_by_id(self, order_id: str) -> Optional[Order]:
        """
        Find an order by ID.
        
        Args:
            order_id: Order ID to search for
            
        Returns:
            Order object if found, None otherwise
        """
        orders = self._load_all()
        for o in orders:
            if o.get("order_id") == order_id:
                return Order.from_dict(o)
        return None
    
    def find_by_customer_id(self, customer_id: str) -> List[Order]:
        """
        Find all orders for a specific customer.
        
        Args:
            customer_id: Customer ID to search for
            
        Returns:
            List of Order objects for the customer
        """
        orders = self._load_all()
        customer_orders = []
        for o in orders:
            if o.get("customer_id") == customer_id:
                customer_orders.append(Order.from_dict(o))
        return customer_orders
    
    def get_all(self) -> List[Order]:
        """
        Get all orders from the repository.
        
        Returns:
            List of all Order objects
        """
        orders_data = self._load_all()
        return [Order.from_dict(o) for o in orders_data]
    
    def _load_all(self) -> List[dict]:
        """
        Load all orders from file.
        
        Returns:
            List of order dictionaries
        """
        try:
            content = self.file_path.read_text()
            return json.loads(content) if content else []
        except json.JSONDecodeError:
            return []
    
    def _write_all(self, orders: List[dict]) -> None:
        """
        Write all orders to file.
        
        Args:
            orders: List of order dictionaries to write
        """
        self.file_path.write_text(json.dumps(orders, indent=2))
