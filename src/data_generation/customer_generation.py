"""
This is the script for generating fake customer data
"""

import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

# intialize faker to create a fake data generator
fake = Faker()

# setting a seed for consistency (same seed = same fake data every time)
Faker.seed(42)
random.seed(42)

def generate_single_customer(customer_id: int):
    """
    Generates a single customer's data and organize
    it inside a dictionary efficient look up. 

    Args:
    - customer_id: a unique ID number for the customer

    Returns:
    - dictionary containing customer generated information

    """

    # create dictionary for one customer
    customer = {
        'customer_id': customer_id, 
        'email': fake.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'phone': fake.phone_number(),
        'address': fake.street_address(),
        'city': fake.city(),
        'state': fake.state(),
        'zip_code': fake.zipcode(), 
        'country': 'USA', 
        'registration_date': fake.date_time_between(
            start_date = '-2y',  # 2 years ago
            end_date = 'now'     # up to now
        ),
        'customer_segement': random.choice(['VIP', 'Regular', 'New']),
        'lifetime_value': round(random.uniform(100, 10000), 2) # random money value
    }

    return customer

def generate_customers(num_customers: int):
    """
    Generates multiple customers by calling 
    the single customer generation function
    multiple times based on the input number. 

    Args:
    - num_customers: number of customers to generate

    Returns:
    - pandas DataFrame containing all the newly
    generated customer's information
    """

    print(f"Generating {num_customers} customers...")

    # container for all customers
    customers = list()
    
    # loop through the range of num_customers to generate each customer
    for index in range(num_customers):
        customer_id = index + 1 # ensure customer_id starts from 1
        customer = generate_single_customer(customer_id)
        customers.append(customer)

    print("All customers have been generated")

    # convert the list of customers into a pandas DataFrame
    customers_df = pd.DataFrame(customers)
    print(f"Generated DataFrame with {len(customers_df)} customers")

    return customers_df

def save_to_csv(customers_df: pd.DataFrame, filename: str):
    """
    Saves the generated customers DataFrame to a CSV file. 

    This is to be optional, but will later be updated to use
    a pipeline and store data in a cloud database (Supabase)

    Args:
    - customers_df: pandas DataFrame containing generated customers
    - filename: name of the csv file to save the data to

    """
    customers_df.to_csv(filename, index=False)
    print(f"Customers data has been saved to {filename}")


if __name__ == "__main__":
    num_customers = 100
    print(f"Starting customer data generation for {num_customers} customers...")
    customers = generate_customers(num_customers)
    # print(customers.head(10))
    print(f"Successfully generated all of the customer data")

    # for now, script to save to csv
    import os
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # up two levels to project root
    project_root = os.path.join(script_dir, '..', '..')
    # build path to data folder
    output_dir = os.path.join(project_root, 'data', 'seed_data')
    os.makedirs(output_dir, exist_ok=True)  # create if doesn't exist

    output_file = os.path.join(output_dir, 'customers.csv')

    save_to_csv(customers, output_file)
    print("Customer data generation script has completed.")