import json
import os
import pandas

def print_tree(data, indent=""):
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{indent}├── {key}")
            print_tree(value, indent + "│   ")
    elif isinstance(data, list):
        for item in data:
            print_tree(item, indent + "│   ")
    else:
        print(f"{indent}└── {data}")

def read_json_tree(base_path):
    try:
        with open(os.path.join(base_path, r"shiftControl\shiftResults\920\shiftResult-920.json"), 'r') as file:
            data = json.load(file)
            print(data)
            # print("JSON Tree Structure:")
            #print_tree(data)
        df = pandas.json_normalize(data)
        csv_file_name = "example_pandas.csv"
        df.to_csv(os.path.join(base_path, csv_file_name), index=False)
        print(f"DataFrame saved to {csv_file_name}")

    except FileNotFoundError:
        print(f"Error: File not found at {base_path}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")

# Example usage
base_path = r"C:\Users\oscar.gonzalez\Desktop\python-park-tickets\dataBilling"  # Replace with your JSON file path
read_json_tree(base_path)