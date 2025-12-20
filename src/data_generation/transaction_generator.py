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

def generate_transaction_id():
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

def generate_transaction_items(transaction_id: int, cart_products: pd.DataFrame) -> list:
    """
    Generate line items for a transaction from the shopping cart

    Args:
    - transaction_id: the parent transaction ID
    - cart_products: DataFrame of products in the shopping cart

    Returns:
    - List of dictionaries, one per item
    """
    items = list()

    for _, product in cart_products.iterrows():
        quantity = random.randint(1, 5)
        unit_price = float(product['price'])

        # applying random discount
        discount_percentage = random.choice([0, 0, 0, 5, 10, 15, 20])
        discount_amount = round(unit_price * quantity * (discount_percentage / 100 ), 2)

        subtotal = round((unit_price * quantity) - discount_amount, 2)

        item = {
            'transaction_id': transaction_id,
            'product_id': product['product_id'], 
            'product_name': product['product_name'],
            'category': product['category'], 
            'quantity': quantity,
            'unit_price': unit_price,
            'discount_amount': discount_amount,
            'subtotal': subtotal
        }

        items.append(item)

    return items

def calculate_transaction_totals(items: list) -> dict:
    """
    Calculate the totals for a transaction from the line items

    Args:
    - items: list of dictionaries representing the line items
    
    Returns:
    - dictionary of transaction totals

    """
    subtotal = sum(item['subtotal'] for item in items)

    # calculate tax with tax rate of 8%
    tax_rate = 0.08
    tax_amount = round(subtotal * tax_rate, 2)

    total_amount = round(subtotal + tax_amount, 2)

    total_discount = sum(item['discount_amount'] for item in items)

    return {
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'total_discount': total_discount,
        'total_items': len(items)
    }

def generate_single_transaction(customers_df: pd.DataFrame, products_df: pd.DataFrame, transaction_date=None):
    """
    Generates a single transaction for a random customer with a shopping cart

    Args:
    - customers_df: pandas DataFrame containing customer data
    - products_df: pandas DataFrame conntaining product data
    - transaction_date: optional date for the transaction

    Returns:
    - Tuple of (transaction_dict, items_list)

    """
    # generating all of the transaction information
    transaction_id = generate_transaction_id()
    customer = select_random_customer(customers_df)
    cart = select_shopping_cart(products_df, min_items=1, max_items=10)
    items = generate_transaction_items(transaction_id, cart)
    totals = calculate_transaction_totals(items)

    if transaction_date is None:
        # randomly generate a date within the last 90 days
        days_ago = random.randint(0, 90)
        transaction_date = datetime.now() - timedelta(days=days_ago)

    payment_methods = ['credit_card', 'debit_card', 'paypal', 'apple_pay', 'google_pay']
    payment_weights = [0.4, 0.3, 0.15, 0.05, 0.05]
    payment_method = random.choices(payment_methods, weights=payment_weights)[0]

    status_options = ['completed', 'pending', 'failed']
    status_weights = [0.92, 0.05, 0.03]
    status = random.choices(status_options, weights=status_weights)[0]

    # building the transaction dictionary
    transaction = {
        'transaction_id': transaction_id,
        'customer_id': int(customer['customer_id']),
        'customer_email': customer['email'], 
        'transaction_date': transaction_date,
        'total_amount': totals['total_amount'],
        'subtotal': totals['subtotal'],
        'tax_amount': totals['tax_amount'],
        'total_discount': totals['total_discount'],
        'payment_method': payment_method,
        'status': status,
        'num_items': totals['total_items'],
        'shipping_address': f"{customer['address']}, {customer['city']}, {customer['state']} {customer['zip_code']}",
        'created_at': datetime.now()
    }

    return transaction, items

def generate_transactions(customers_df: pd.DataFrame, products_df: pd.DataFrame, num_transactions=500):
    """
    Generate multiple transactions for customers and products

    Args:
    - customers_df: DataFrame of customers
    - products_df: DataFrame of products
    - num_transactions: number of transactions to generate

    Returns:
    - Tuple of (transactions_df, items_df)
    """
    print(f"Generating {num_transactions} transactions...")

    all_transactions = list()
    all_items = list()

    for i in range(num_transactions):
        transaction, items = generate_single_transaction(customers_df, products_df)
        all_transactions.append(transaction)
        all_items.extend(items)

    # converting to DataFrames
    transactions_df = pd.DataFrame(all_transactions)
    items_df = pd.DataFrame(all_items)

    print(f"Generated {len(transactions_df)} transactions and {len(items_df)} items")

    return transactions_df, items_df

def analyze_transaction_data(transactions_df, items_df):
    """
    Analyze and validate the generated transaction data
    """
    print("\n" + "=" * 70)
    print("TRANSACTION DATA ANALYSIS")
    print("=" * 70)
    
    # transaction analysis
    print("\n TRANSACTIONS:")
    print(f"  Total transactions: {len(transactions_df)}")
    print(f"  Total revenue: ${transactions_df['total_amount'].sum():,.2f}")
    print(f"  Average order value: ${transactions_df['total_amount'].mean():.2f}")
    print(f"  Median order value: ${transactions_df['total_amount'].median():.2f}")
    
    print(f"\n  Transaction status breakdown:")
    for status, count in transactions_df['status'].value_counts().items():
        pct = (count / len(transactions_df)) * 100
        print(f"    {status}: {count} ({pct:.1f}%)")
    
    print(f"\n  Payment method breakdown:")
    for method, count in transactions_df['payment_method'].value_counts().items():
        pct = (count / len(transactions_df)) * 100
        print(f"    {method}: {count} ({pct:.1f}%)")
    
    # items analysis
    print("\n TRANSACTION ITEMS:")
    print(f"  Total items sold: {len(items_df)}")
    print(f"  Average items per transaction: {len(items_df) / len(transactions_df):.2f}")
    print(f"  Total revenue from items: ${items_df['subtotal'].sum():,.2f}")
    print(f"  Total discounts given: ${items_df['discount_amount'].sum():,.2f}")
    
    print(f"\n  Top 5 products by quantity sold:")
    top_products = items_df.groupby(['product_id', 'product_name'])['quantity'].sum()
    top_products = top_products.sort_values(ascending=False).head()
    for (prod_id, prod_name), qty in top_products.items():
        print(f"    {prod_name}: {qty} units")
    
    print(f"\n  Top 5 categories by revenue:")
    category_revenue = items_df.groupby('category')['subtotal'].sum()
    category_revenue = category_revenue.sort_values(ascending=False).head()
    for category, revenue in category_revenue.items():
        print(f"    {category}: ${revenue:,.2f}")
    
    # customer analysis
    print("\n CUSTOMER BEHAVIOR:")
    transactions_per_customer = transactions_df.groupby('customer_id').size()
    print(f"  Unique customers who purchased: {len(transactions_per_customer)}")
    print(f"  Average transactions per customer: {transactions_per_customer.mean():.2f}")
    print(f"  Max transactions by one customer: {transactions_per_customer.max()}")
    
    # data quality checks
    print("\n DATA QUALITY CHECKS:")
    print(f"  All transactions have items: {len(transactions_df) <= len(items_df)}")
    print(f"  No negative amounts: {(transactions_df['total_amount'] >= 0).all()}")
    print(f"  Unique transaction IDs: {transactions_df['transaction_id'].is_unique}")
    print(f"  Items link to transactions: {items_df['transaction_id'].isin(transactions_df['transaction_id']).all()}")
    
    # Calculate some business metrics
    print("\n BUSINESS METRICS:")
    completed_txns = transactions_df[transactions_df['status'] == 'completed']
    if len(completed_txns) > 0:
        print(f"  Completed revenue: ${completed_txns['total_amount'].sum():,.2f}")
        conversion_rate = (len(completed_txns) / len(transactions_df)) * 100
        print(f"  Conversion rate: {conversion_rate:.1f}%")
        avg_discount_per_order = transactions_df['total_discount'].mean()
        print(f"  Average discount per order: ${avg_discount_per_order:.2f}")


def save_to_csv(dataframe, filename):
    """
    Save DataFrame to CSV file
    
    Args:
        dataframe: pandas DataFrame to save
        filename: Full path to output file
    """
    dataframe.to_csv(filename, index=False)
    print(f" Saved to {filename}")

if __name__ == "__main__": 
    print("=" * 70)
    print("E-COMMERCE TRANSACTION GENERATOR")
    print("=" * 70)

    
    # setup data directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '..', '..')
    data_dir = os.path.join(project_root, 'data', 'seed_data')

    # load existing data
    customers_df, products_df = load_seed_data(data_dir)

    # generate transactions
    transactions_df, items_df = generate_transactions(customers_df, products_df, num_transactions=500)

    # show sample data
    print("\n" + "=" * 70)
    print("SAMPLE TRANSACTION DATA")
    print("=" * 70)

    print("\nSample Transactions:")
    sample_cols = ["transaction_id", "customer_id", "transaction_date", "total_amount", "status", "payment_method"]
    print(transactions_df[sample_cols].head(10))

    print("\nSample Transaction Items:")
    item_cols = ["transaction_id", "product_name", "quantity", "unit_price", "discount_amount", "subtotal"]
    print(items_df[item_cols].head(10))

    # save to CSV
    print("\n" + "=" * 70)
    print("SAVING DATA TO FILES")
    print("=" * 70)

    transactions_file = os.path.join(data_dir, "transactions.csv")
    items_file = os.path.join(data_dir, "transaction_items.csv")

    save_to_csv(transactions_df, transactions_file)
    save_to_csv(items_df, items_file)

    print("Files have been saved successsfully insde the data directory")