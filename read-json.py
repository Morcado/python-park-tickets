import json

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

def read_json_tree(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            print("JSON Tree Structure:")
            print_tree(data)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")

# Example usage
file_path = r"C:\Users\oscar.gonzalez\Downloads\shiftResults\921\Ferchaz64023.json"  # Replace with your JSON file path
read_json_tree(file_path)