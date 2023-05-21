import argparse
import csv
import json
import os


def get_params() -> dict:
    parser = argparse.ArgumentParser(description='DataTest')
    parser.add_argument('--customers_location', required=False, default="./input_data/starter/customers.csv")
    parser.add_argument('--products_location', required=False, default="./input_data/starter/products.csv")
    parser.add_argument('--transactions_location', required=False, default="./input_data/starter/transactions/")
    parser.add_argument('--output_location', required=False, default="./output_data/outputs/")
    return vars(parser.parse_args())


def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def read_json_lines(file_path):
    with open(file_path, 'r') as file:
        return [json.loads(line) for line in file]


def process_data(customers_location, products_location, transactions_location, output_location):
    # Read customers data
    customers = read_csv(customers_location)
    customer_dict = {customer['customer_id']: customer for customer in customers}

    # Read products data
    products = read_csv(products_location)
    product_dict = {product['product_id']: product for product in products}

    # Process transactions data
    transactions = []
    for subdir, dirs, files in os.walk(transactions_location):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(subdir, file)
                transactions.extend(read_json_lines(file_path))

    # Generate output data
    output_data = []
    for transaction in transactions:
        customer_id = transaction['customer_id']
        basket = transaction['basket']

        if customer_id in customer_dict:
            loyalty_score = customer_dict[customer_id]['loyalty_score']
            for item in basket:
                product_id = item['product_id']
                if product_id in product_dict:
                    product_category = product_dict[product_id]['product_category']
                    product_dict[product_id].setdefault('purchase_count', 0)
                    product_dict[product_id]['purchase_count'] += 1
                    output_data.append({
                        'customer_id': customer_id,
                        'loyalty_score': loyalty_score,
                        'product_id': product_id,
                        'product_category': product_category,
                        'purchase_count': product_dict[product_id]['purchase_count']
                    })

    # Write output data to JSON file
    output_file_path = os.path.join(output_location, 'output.json')
    with open(output_file_path, 'w') as output_file:
        json.dump(output_data, output_file, indent=4)
    print(f"Output data saved to: {output_file_path}")


def main():
    params = get_params()
    customers_location = params['customers_location']
    products_location = params['products_location']
    transactions_location = params['transactions_location']
    output_location = params['output_location']

    process_data(customers_location, products_location, transactions_location, output_location)


if __name__ == "__main__":
    main()
