import pandas as pd
import json

def flatten_json(nested_json, parent_key='', sep='_', prefix=''):
    items = []
    for k, v in nested_json.items():
        new_key = f'{prefix}{parent_key}{sep}{k}' if parent_key else f'{prefix}{k}'
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for item in enumerate(v):
                items.extend(flatten_json({f'{new_key}': item}, '', sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def process_excel(input_file, output_file, prefix='content_activities_'):
    # Read Excel file
    df = pd.read_excel(input_file)
    
    # Initialize lists for the final data
    final_rows = []
    
    for _, row in df.iterrows():
        json_data = row['JSON_Column']
        try:
            json_dict = json.loads(json_data)
        except json.JSONDecodeError:
            print(f"Error decoding JSON: {json_data}")
            continue
        
        # Flatten JSON data
        if 'items' in json_dict:
            items = json_dict['items']
            for item in items:
                # Flatten JSON data and apply prefix to all keys once
                flat_item = flatten_json(item, prefix=prefix)
                combined_row = {**row.to_dict(), **flat_item}
                # Remove the JSON column as it's now flattened
                del combined_row['JSON_Column']
                final_rows.append(combined_row)
        else:
            print(f"Expected 'items' in JSON but got: {json_dict}")
    
    # Convert to DataFrame and save to CSV
    final_df = pd.DataFrame(final_rows)
    final_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    process_excel('input.xlsx', 'output.csv')