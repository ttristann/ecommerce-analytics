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

if __name__ == "__main__":
    id = 1
    customer_data = generate_single_customer(id)
    print(customer_data['email'])
