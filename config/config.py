"""
Configuration Module for E-Commerce System

This module defines all configuration settings for the e-commerce application.
It includes file paths, data directories, and application constants.

Following PEP 8 style guide: https://peps.python.org/pep-0008/
"""

import os
from pathlib import Path

# Get the project root directory dynamically
# This ensures no hardcoded paths are used
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"
SRC_DIR = PROJECT_ROOT / "src"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# File paths for data persistence (JSON files)
# Using Path objects for cross-platform compatibility
USERS_FILE = DATA_DIR / "users.json"
PRODUCTS_FILE = DATA_DIR / "products.json"
ORDERS_FILE = DATA_DIR / "orders.json"
CARTS_FILE = DATA_DIR / "carts.json"

# Application constants
# Tax rate as a decimal (e.g., 0.10 = 10%)
TAX_RATE = 0.10

# Shipping cost
SHIPPING_COST = 5.00

# Default currency symbol
CURRENCY = "$"

# Application name and version
APP_NAME = "E-Commerce System"
APP_VERSION = "1.0.0"

# Console UI constants
MENU_WIDTH = 50
