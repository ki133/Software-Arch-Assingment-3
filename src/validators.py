"""
Validation Module - Input Validation and Error Handling

This module provides input validation for all user inputs.
It ensures data integrity and handles invalid inputs gracefully.

Following PEP 8 style guide.
"""

import re
from typing import Tuple


class InputValidator:
    """
    Utility class for validating user inputs.
    
    Provides methods for validating various types of inputs
    such as email, name, price, quantity, etc.
    """
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """Validate a name input."""
        if not name or not name.strip():
            return False, "Name cannot be blank."
        name = name.strip()
        if len(name) < 2:
            return False, "Name must be at least 2 characters long."
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            return False, "Name can only contain letters, spaces, hyphens, and apostrophes."
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate an email address."""
        if not email or not email.strip():
            return False, "Email cannot be blank."
        email = email.strip()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format."
        return True, ""
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """Validate a password."""
        if not password:
            return False, "Password cannot be blank."
        if len(password) < 6:
            return False, "Password must be at least 6 characters long."
        return True, ""
    
    @staticmethod
    def validate_street_address(street: str) -> Tuple[bool, str]:
        """Validate a street address."""
        if not street or not street.strip():
            return False, "Street address cannot be blank."
        if len(street.strip()) < 5:
            return False, "Street address must be at least 5 characters long."
        return True, ""
    
    @staticmethod
    def validate_city(city: str) -> Tuple[bool, str]:
        """Validate a city name."""
        if not city or not city.strip():
            return False, "City cannot be blank."
        city = city.strip()
        if len(city) < 2:
            return False, "City name must be at least 2 characters long."
        if not re.match(r"^[a-zA-Z\s\-']+$", city):
            return False, "City name can only contain letters, spaces, and hyphens."
        return True, ""
    
    @staticmethod
    def validate_postal_code(postal_code: str) -> Tuple[bool, str]:
        """Validate a postal code."""
        if not postal_code or not postal_code.strip():
            return False, "Postal code cannot be blank."
        postal_code = postal_code.strip()
        if len(postal_code) < 3 or len(postal_code) > 10:
            return False, "Postal code must be between 3 and 10 characters."
        if not re.match(r"^[a-zA-Z0-9\s\-]+$", postal_code):
            return False, "Postal code can only contain letters, numbers, spaces, and hyphens."
        return True, ""
    
    @staticmethod
    def validate_country(country: str) -> Tuple[bool, str]:
        """Validate a country name."""
        if not country or not country.strip():
            return False, "Country cannot be blank."
        if len(country.strip()) < 3:
            return False, "Country name must be at least 3 characters long."
        if not re.match(r"^[a-zA-Z\s\-']+$", country.strip()):
            return False, "Country name can only contain letters, spaces, and hyphens."
        return True, ""
    
    @staticmethod
    def validate_price(price_str: str) -> Tuple[bool, float, str]:
        """Validate a price input."""
        if not price_str or not price_str.strip():
            return False, 0.0, "Price cannot be blank."
        try:
            price = float(price_str.strip())
            if price <= 0:
                return False, 0.0, "Price must be a positive number."
            return True, price, ""
        except ValueError:
            return False, 0.0, "Price must be a valid number."
    
    @staticmethod
    def validate_quantity(quantity_str: str) -> Tuple[bool, int, str]:
        """Validate a quantity input."""
        if not quantity_str or not quantity_str.strip():
            return False, 0, "Quantity cannot be blank."
        try:
            quantity = int(quantity_str.strip())
            if quantity <= 0:
                return False, 0, "Quantity must be greater than zero."
            return True, quantity, ""
        except ValueError:
            return False, 0, "Quantity must be a valid integer."
    
    @staticmethod
    def validate_menu_choice(choice_str: str, max_option: int) -> Tuple[bool, int, str]:
        """Validate a menu choice input."""
        if not choice_str or not choice_str.strip():
            return False, 0, "Choice cannot be blank."
        try:
            choice = int(choice_str.strip())
            if choice < 0 or choice > max_option:
                return False, 0, f"Please enter a number between 0 and {max_option}."
            return True, choice, ""
        except ValueError:
            return False, 0, "Please enter a valid number."
    
    @staticmethod
    def validate_product_id(product_id: str) -> Tuple[bool, str]:
        """Validate a product ID input."""
        if not product_id or not product_id.strip():
            return False, "Product ID cannot be blank."
        return True, ""
    
    @staticmethod
    def validate_non_empty_input(input_str: str, field_name: str = "Input") -> Tuple[bool, str]:
        """Validate that an input is not empty."""
        if not input_str or not input_str.strip():
            return False, f"{field_name} cannot be blank."
        return True, ""
