# E-Commerce System

A comprehensive Object-Oriented Python implementation of an e-commerce system demonstrating professional software architecture, design patterns, and coding standards.

## Quick Start

```bash
python main.py
```

## Features

- User Registration & Login
- Product Catalogue Browsing
- Shopping Cart Management
- Checkout & Payment Processing
- Order History & Tracking
- Invoice Generation
- Shipment Tracking

## Design Patterns Implemented

1. **Repository Pattern** - Data persistence layer
2. **Strategy Pattern** - Payment methods
3. **Adapter Pattern** - Carrier tracking
4. **Service Pattern** - Business logic
5. **MVC Pattern** - Application structure

## Coding Standard

**PEP 8**: https://peps.python.org/pep-0008/

## Project Structure

```
Source Code/
├── main.py                 # Application entry point
├── config/config.py        # Configuration (NO hardcoded paths!)
├── data/                   # JSON data storage
├── src/
│   ├── models.py          # Domain classes
│   ├── repositories.py    # Data access layer
│   ├── services.py        # Business logic
│   ├── validators.py      # Input validation
│   ├── ui.py              # User interface
│   └── init_data.py       # Sample data initialization
└── README.md
```

## Requirements

- Python 3.8+
- No external dependencies (standard library only)

## Author

Software Architecture - 2025
