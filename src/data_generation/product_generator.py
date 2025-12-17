"""
Product Catalog and Inventory Generator. 

This generates realistic product and inventory data
necessary for populating an ecommerce platform's database
and conduct various kinds of data analysis.
"""

import os
import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

# initialize faker to get consistent fake data
fake = Faker()
Faker.seed(42)
random.seed(42)

categories = {
    'Electronics': ['Smartphones', 'Laptops', 'Tablets', 'Accessories', 'Cameras' ], 
    'Clothing': ['Men', 'Women', 'Kids', 'Accessrories', 'Shoes'],
    'Home & Garden': ['Furniture', 'Decor', 'Kitchen', 'Outdoor', 'Lighting'], 
    'Sports': ['Fitness', 'Outdoor', 'Team Sports', 'Equipment', 'Apparel'], 
    'Books': ['Fiction', 'Non-Fiction', 'Educational', 'Children', 'Comics'],
    'Beauty': ['Skincare', 'Makeup', 'Haircare', 'Fragrances', 'Tools'],
    'Food & Beverage': ['Snacks', 'Beverages', 'Organic', 'Gourmet', 'Pantry']
}

def generate_product_name(category:str, subcategory:str) -> str:
    """
    Generates a realistic prodiuct name based on category and subcategory.

    Args:
    - category: main product category
    - subcategory: specific product subcategory

    Returns:
    - String representing the product name

    """
    name_patterns = {
        'Electronics': [
            f"{fake.company()} {subcategory}",
            f"Premium {subcategory} Pro",
            f"{subcategory} {random.choice(['X', 'Plus', 'Max', 'Ultra'])}"
        ],
        'Clothing': [
            f"{fake.color_name()} {subcategory} {random.choice(['Shirt', 'Pants', 'Jacket', 'Dress'])}",
            f"Designer {subcategory} {random.choice(['Collection', 'Style', 'Line'])}"
        ],
        'Home & Garden': [
            f"Modern {subcategory} {random.choice(['Set', 'Collection', 'Piece'])}",
            f"{fake.color_name()} {subcategory}"
        ],
        'Sports': [
            f"Pro {subcategory} {random.choice(['Gear', 'Equipment', 'Kit'])}",
            f"{subcategory} Champion"
        ],
        'Books': [
            f"{fake.catch_phrase()}",  # generates book-like titles
            f"The {fake.word().title()} {fake.word().title()}"
        ],
        'Beauty': [
            f"{fake.company()} {subcategory} {random.choice(['Essentials', 'Collection', 'Kit'])}",
            f"Luxury {subcategory}"
        ],
        'Food & Beverage': [
            f"Organic {subcategory}",
            f"{fake.company()} {subcategory} Mix"
        ]
    }

    pattern = name_patterns.get(category, [f"{subcategory} Item"])

    return random.choice(pattern)

def generate_single_product(product_id: int) -> dict:
    """
    Gnerates a single product with realistic attributes and values.

    Args:
    - product_id: unique identifier for the product

    Returns:
    - dictionary containing the generated product's information
    """

    # randomly select category and subcategory
    category = random.choice(list(categories.keys()))
    subcategory = random.choice(categories[category])

    # generate price based on category as some categories are pricier
    price_ranges = {
        'Electronics': (50, 2000), 
        'Clothing': (15, 300), 
        'Home & Garden': (20, 1500),
        'Sports': (10, 500),
        'Books': (5, 50), 
        'Beauty': (10, 200), 
        'Food & Beverage': (3, 100)
    }

    min_price, max_price = price_ranges.get(category, (10, 100))
    price = round(random.uniform(min_price, max_price), 2)
    cost_percentage = random.uniform(0.4, 0.8) # cost is 40% to 80% of price
    cost = round(price * cost_percentage, 2)

    product = {
        'product_id': product_id, 
        'product_name': generate_product_name(category, subcategory), 
        'category': category,
        'subcategory': subcategory,
        'brand': fake.company(),
        'price': price,
        'cost': cost,
        'profit_margin': round(((price - cost) / price) * 100, 2), 
        'description': fake.text(max_nb_chars=200),
        'image_url': fake.image_url(),
        'weight_kg': round(random.uniform(.1, 20), 2),
        'created_at': fake.date_time_between(
            start_date = '-1y',
            end_date = 'now'
        )
    }

    return product

def generate_products(num_products: int) -> pd.DataFrame:
    """
    Generates multiple products and then stores them in
    a pandas DataFrame

    Args:
    - num_products: number of products to generate

    Returns:
    - pandas DataFrame containing all the newly generated
    product data
    """

    print(f'Generating {num_products} products...')
    products = list()

    for i in range(num_products):
        product_id = i + 1 # ensure product_id starts from 1
        product = generate_single_product(product_id)
        products.append(product)

    print("All products have been generated.")

    # convert the list of products into a pandas DataFrame
    products_df = pd.DataFrame(products)

    return products_df

if __name__ == "__main__":
    num_products = 100
    products_df = generate_products(num_products)
    print(products_df.head(10))