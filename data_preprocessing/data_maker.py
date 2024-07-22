from faker import Faker
import random
import pandas as pd

fake = Faker()
from datetime import date
from dateutil.relativedelta import relativedelta

six_months = date.today() - relativedelta(months=+6)
three_months = date.today() - relativedelta(months=+3)
months = [three_months, six_months]

def generate_customer_data():
    age = random.randint(20, 70)
    gender = random.choice(['Male', 'Female'])
    marital_status = random.choice(['Single', 'Married', 'Divorced', 'Widowed'])
    income_level = random.choice(['Low', 'Medium', 'High'])
    education = random.choice(['High School', 'College', 'University'])
    occupation = fake.job()
    email = fake.email()
    residential_status = random.choice(['Owns house', 'Rents', 'Living with parents'])
    dependents = random.randint(0, 5)  # Number of dependents
    debt_to_income = round(random.uniform(0.1, 0.5), 2)  # Debt-to-income ratio
    credit_bureau = random.randint(760, 850)
    annual_income = random.randint(100000, 100000000)
    name = fake.name()
    password = fake.password()

    return {
        'Name': name,
        'Password': password,
        'Age': age,
        'Gender': gender,
        'Email' : email,
        'Marital Status': marital_status,
        'Income Level': income_level,
        'Education': education,
        'Occupation': occupation,
        'Residential Status': residential_status,
        'Dependents': dependents,
        'Debt-to-Income': debt_to_income,
        'Credit Bureau': credit_bureau,
        'Annual Income': annual_income
    }

def generate_inquiries(last_months):
    inquiries = []
    today = fake.date_this_month()

    for _ in range(random.randint(1, 5)):
        inquiry_date = fake.date_between(start_date=last_months, end_date=today)
        product_type = random.choice(['Personal Loan', 'Credit Card', 'Home Loan', 'Car Loan', 'Fixed Deposit', 'SIP', 'Insurance'])
        inquiries.append({'product_name': product_type, 'date': inquiry_date})

    return inquiries if inquiries else []

def generate_dataset(num_rows, months):
    data_rows = []

    for _ in range(num_rows):
        customer_data = generate_customer_data()
        last_3_months_inquiries = generate_inquiries(months[0])
        last_6_months_inquiries = generate_inquiries(months[1])

        customer_row = {
            'Customer_ID': fake.uuid4(),
            'Name': customer_data['Name'],
            'Password': customer_data['Password'],
            'Age': customer_data['Age'],
            'email': customer_data['Email'],
            'Gender': customer_data['Gender'],
            'Marital Status': customer_data['Marital Status'],
            'Income Level': customer_data['Income Level'],
            'Education': customer_data['Education'],
            'Occupation': customer_data['Occupation'],
            'Residential Status': customer_data['Residential Status'],
            'Dependents': customer_data['Dependents'],
            'Debt-to-Income': customer_data['Debt-to-Income'],
            'Credit Bureau': customer_data['Credit Bureau'],
            'Annual Income': customer_data['Annual Income']
        }

        for product_type in ['Personal Loan', 'Credit Card', 'Home Loan', 'Car Loan', 'Fixed Deposit', 'SIP', 'Insurance']:
            inq_in_last_3_months = any(inq['product_name'] == product_type for inq in last_3_months_inquiries)
            customer_row[f'last_3months_{product_type.replace(" ", "_").lower()}_inq'] = inq_in_last_3_months

        for product_type in ['Personal Loan', 'Credit Card', 'Home Loan', 'Car Loan', 'Fixed Deposit', 'SIP', 'Insurance']:
            inq_in_last_6_months = any(inq['product_name'] == product_type for inq in last_6_months_inquiries)
            customer_row[f'last_6months_{product_type.replace(" ", "_").lower()}_inq'] = inq_in_last_6_months

        data_rows.append(customer_row)
    return data_rows

if __name__ == '__main__':
    dataset = generate_dataset(50, months)
    excel_file_path = 'data/dataset_customer.xlsx'
    dataset = pd.DataFrame(dataset)
    dataset.to_excel(excel_file_path, index=False)

    print(f"Dataset saved to {excel_file_path}")
