import pandas as pd
import json
import glob
from collections import Counter, defaultdict
import sys 

# Load the ground truth CSV file
ground_truth_path = '../ground_truth.csv'
ground_truth_df = pd.read_csv(ground_truth_path)

# Filter problematic ads
non_problematic_ads = ground_truth_df[ground_truth_df['Ground Truth'].isna()]
problematic_ads = ground_truth_df[ground_truth_df['Ground Truth'].notna()]

print("Number of non_problematic ads:", len(non_problematic_ads))
print("Sample problematic ads:")
print(len(problematic_ads))
# sys.exit(0)
# Verify mapping of problematic ads to JSON files
missing_files = 0
missing_entries = 0

problematic_d = {'exchange': {}, 'advertiser': {}}
non_problematic_d = {'exchange': {}, 'advertiser': {}}

for _, row in problematic_ads.iterrows():
    filename = row['Filename'].strip("{}'")  # Clean up filename format
    json_filename = row['JSON Filename'].strip("{}'")  # Clean up JSON filename
    # print(filename, json_filename)
    # Open the corresponding exchange JSON file
    file_path = f'../exchange_info/cleaned_exchange_info_{json_filename}.json'
    try:
        with open(file_path, 'r') as f:
            exchange_data = json.load(f)

            # Check if the filename exists in the JSON data
            if filename not in exchange_data:
                # print(f"Entry {filename} not found in file {file_path}.")
                missing_entries += 1
                continue

            for key in exchange_data[filename].keys():
                if 'advertiser' in key.lower():
                    problematic_d['advertiser'][exchange_data[filename][key]] = problematic_d['advertiser'].get(exchange_data[filename][key], 0) + 1
                else:
                    problematic_d['exchange'][exchange_data[filename][key]] = problematic_d['exchange'].get(exchange_data[filename][key], 0) + 1
                 
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        missing_files += 1

print(f"Total missing files: {missing_files}")
print(f"Total missing entries: {missing_entries}")

missing_files = 0
missing_entries = 0

for _, row in non_problematic_ads.iterrows():
    filename = row['Filename'].strip("{}'")  # Clean up filename format
    json_filename = row['JSON Filename'].strip("{}'")  # Clean up JSON filename
    # print(filename, json_filename)
    # Open the corresponding exchange JSON file
    file_path = f'../exchange_info/cleaned_exchange_info_{json_filename}.json'
    try:
        with open(file_path, 'r') as f:
            exchange_data = json.load(f)

            # Check if the filename exists in the JSON data
            if filename not in exchange_data:
                # print(f"Entry {filename} not found in file {file_path}.")
                missing_entries += 1
                continue

            for key in exchange_data[filename].keys():
                if 'advertiser' in key.lower():
                    non_problematic_d['advertiser'][exchange_data[filename][key]] = non_problematic_d['advertiser'].get(exchange_data[filename][key], 0) + 1
                else:
                    non_problematic_d['exchange'][exchange_data[filename][key]] = non_problematic_d['exchange'].get(exchange_data[filename][key], 0) + 1
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        missing_files += 1

problematic_d['advertiser'] = dict(sorted(problematic_d['advertiser'].items(), key=lambda item: item[1]))
problematic_d['exchange'] = dict(sorted(problematic_d['exchange'].items(), key=lambda item: item[1]))

non_problematic_d['advertiser'] = dict(sorted(non_problematic_d['advertiser'].items(), key=lambda item: item[1]))
non_problematic_d['exchange'] = dict(sorted(non_problematic_d['exchange'].items(), key=lambda item: item[1]))

json.dump(problematic_d, open('problematic_exchanges.json', 'w'))
json.dump(non_problematic_d, open('non_problematic_exchanges.json', 'w'))
print(f"Total missing files: {missing_files}")
print(f"Total missing entries: {missing_entries}")
