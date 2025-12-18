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

def generate_inventory_for_product(product_id, num_warehouses=3) -> list:
    """
    Generates inventory levels for a given product across multiple warehouses.

    Args:
    - product_id: the product identifier for which the inventory is generated
    - num_warehouses: number of warehouses to generate inventory for

    Returns:
    - list of dictionaries containing inventory data for the product
    """
    inventory_records = list()

    for warehouse_id in range(1, num_warehouses + 1):
        # different warehouses might have different stock levels
        # some products are more popular and tbus have higher stock
        popularity = random.choices(['high', 'medium', 'low'])
        if popularity == 'high':
            quantity = random.randint(100, 500)
            reorder_level = random.randint(50, 100)
        elif popularity =='medium':
            quantity = random.randint(20, 100)
            reorder_level = random.randint(20, 50)
        else:
            quantity = random.randint(0, 20)
            reorder_level = random.randint(10, 20)

        inventory = {
            'product_id': product_id, 
            'warehouse_id': warehouse_id,
            'warehouse_name': f"Warehouse {warehouse_id}",
            'quantity': quantity,
            'last_updated': datetime.now(),
            'needs_reorder': reorder_level > quantity
        }

        inventory_records.append(inventory)
        
    return inventory_records

def generate_inventory(products_df: pd.DataFrame, num_warehouses=3) -> pd.DataFrame:
    """
    Generates inventory records for all products in the provided DataFrame.

    Args:
    - products_df: pandas DataFrame containing product data
    - num_warehouses: number of warehouses to generate inventory for

    Returns:
    - pandas DataFrame containing all inventory records
    """
    print(f"Generating inventory for {len(products_df)} products across {num_warehouses} warehouses...")
    all_inventory = list()

    # for each product, create inventory records in each warehouse
    for product_id in products_df['product_id']:
        inventory_records = generate_inventory_for_product(product_id, num_warehouses)
        all_inventory.extend(inventory_records)

    print("All inventory records have been generated.")
    inventory_df = pd.DataFrame(all_inventory)

    return inventory_df

def save_to_csv(dataframe: pd.DataFrame, filename: str):
    """
    Saves the generated product DataFrame to a CSV file. 

    This is to be optional, but will later be updated to use
    a pipeline and store data in a cloud database (Supabase)

    Args:
    - dataframe: pandas DataFrame containing generated customers
    - filename: name of the csv file to save the data to

    """
    dataframe.to_csv(filename, index=False)
    print(f"Products and inventory data has been saved to {filename}") 

def analyze_product_data(products_df: pd.DataFrame, inventory_df: pd.DataFrame):
    """
    Performs basic analysis on the generated product and inventory data
    """
    print("\n" + "=" * 60)
    print("DATA ANALYSIS")
    print("=" * 60)
    
    # Product analysis
    print("\n PRODUCT CATALOG:")
    print(f"  Total products: {len(products_df)}")
    print(f"\n  Products by category:")
    for category, count in products_df['category'].value_counts().items():
        print(f"    {category}: {count}")
    
    print(f"\n  Price statistics:")
    print(f"    Min price: ${products_df['price'].min():.2f}")
    print(f"    Max price: ${products_df['price'].max():.2f}")
    print(f"    Avg price: ${products_df['price'].mean():.2f}")
    print(f"    Median price: ${products_df['price'].median():.2f}")
    
    # inventory analysis
    print("\n INVENTORY:")
    print(f"  Total inventory records: {len(inventory_df)}")
    print(f"  Total units in stock: {inventory_df['quantity'].sum():,}")
    print(f"  Products with low stock: {inventory_df['needs_reorder'].sum()}")
    
    # data quality checks
    print("\n DATA QUALITY CHECKS:")
    print(f"  All products have inventory: {len(products_df) * 3 == len(inventory_df)}")
    print(f"  No negative prices: {(products_df['price'] > 0).all()}")
    print(f"  Price > Cost: {(products_df['price'] > products_df['cost']).all()}")
    print(f"  No duplicate product IDs: {products_df['product_id'].is_unique}\n")



if __name__ == "__main__":
    num_products = 200
    products_df = generate_products(num_products)
    inventory_df = generate_inventory(products_df, num_warehouses=3)
    analyze_product_data(products_df, inventory_df)

    # creating files
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # up two levels to project root
    project_root = os.path.join(script_dir, '..', '..')
    # build path to data folder
    output_dir = os.path.join(project_root, 'data', 'seed_data')
    os.makedirs(output_dir, exist_ok=True)  # create if doesn't exist

    products_file = os.path.join(output_dir, 'products.csv')
    inventory_file = os.path.join(output_dir, 'inventory.csv')

    # sabe to csv files
    save_to_csv(products_df, products_file)
    save_to_csv(inventory_df, inventory_file)


