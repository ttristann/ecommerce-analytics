"""
Transaction Generator

Generates realistic e-commerce transationns with shopping cart items.
This combines customer and product data to create realistic
customer purchace transactions and history.
"""

import os
import uuid
import random
import pandas as pd
from datetime import datetime, timedelta

# seeds for data consistency
random.seed(42)

def load_seed_data(data_dir: str):
    """
    Loads customer and product data that was generated and saved. 

    Args:
    - data_dir: directory where the seed data CSV files are stored

    Returns:
    - tuple of (customers_df, products_df)

    """
    print(f"Loading seed data from {data_dir}...")

    customers_file = os.path.join(data_dir, "customers.csv")
    products_file = os.path.join(data_dir, "products.csv")

    # load data and convert to DataFrames
    customers_df = pd.read_csv(customers_file)
    products_df = pd.read_csv(products_file)

    print(f"Loaded {len(customers_df)} customers and {len(products_df)} products")

    return customers_df, products_df

def generate_transactions_id():
    """
    Generates a unique transaction ID using UUID4

    Returns:
    - str: unique transaction ID (TXN-xxxxxx)

    """
    return f"TXN-{str(uuid.uuid4())[:8]}"

def select_random_customer(customers_df: pd.DataFrame, customer_segment_weights=None):
    """
    Selects a random customer from the customers DataFrame and 
    assigns a customer segment based on provided weights

    Args:
    - customers_df: pandas DataFrame containing customer data
    - customer_segment_weights: optional dictionary of weights by segment

    Returns:
    - pandas Series representing the selected customer
    """
    # if customer_segment_weights is None:
    #     customer_segment_weights = {
    #         'Regular': 0.7,
    #         'Premium': 0.2,
    #         'VIP': 0.1
    #     }

    # segments = list(customer_segment_weights.keys())
    # weights = list(customer_segment_weights.values())

    # selected_customer = customers_df.sample(n=1).iloc[0]
    # selected_customer['customer_segment'] = random.choices(segments, weights=weights, k=1)[0]
    if customer_segment_weights:
        # VIP customers shop more often
        # will be implmented later
        # TODO: implement customer segment based selection
        pass
    
    return customers_df.sample(n=1).iloc[0]

def select_shopping_cart(products_df: pd.DataFrame, min_items=1, max_items=10):
    """
    Generates a shopping cart by randomly selecting products

    Args:
    - products_df: pandas DataFrame containing product
    - min_items: minimum number of items in the cart
    - max_items: maximum number of items in the cart

    Returns:
    - DataFrame representing the shopping cart items
    """
    # the amount of items in the cart
    num_items = random.randint(min_items, max_items)

    # selects random products for the cart
    # cannot have the same products twice in the cart
    cart = products_df.sample(n=num_items)

    return cart