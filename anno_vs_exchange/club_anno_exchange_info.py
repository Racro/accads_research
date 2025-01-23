import json
import csv
import os

lst = ['control_US', 'control_germany', 'control_over_18', 'control_under_18', 'accads_US', 'accads_germany', 'accads_over_18', 'accads_under_18']

output_csv = f'/home/ritik/work/pes/accads_research/anno_vs_exchange.csv'

merged_data = []
for keyword in lst:
    # File paths
    exchange_info_file = f'/home/ritik/work/pes/accads_research/cleaned_exchange_info_{keyword}.json'
    annotations_file = f'/home/ritik/Downloads/11_20_anno2/{keyword}.json'


    # Load JSON data
    with open(exchange_info_file, 'r') as f:
        exchange_info = json.load(f)

    with open(annotations_file, 'r') as f:
        annotations = json.load(f)

    # Prepare data for CSV
    
    for record in annotations:
        # Extract filename from path
        filename = os.path.basename(record['data']['image'])
        
        # Extract annotations
        annotation_choices = []
        for annotation in record['annotations']:
            for result in annotation.get('result', []):
                if 'choices' in result.get('value', {}):
                    annotation_choices.append(result['value']['choices'][0].split('(')[0].strip())
        
        # Join multiple choices into one cell
        annotations_combined = ' & '.join(annotation_choices) if annotation_choices else 'NA'
        
        # Fetch exchange info
        exchange_data = exchange_info.get(filename, {})
        ad_exchange = exchange_data.get('Ad Exchange/Server', 'NA')
        middle_parties = exchange_data.get('Middle Parties', 'NA')
        advertisers = exchange_data.get('Advertisers', 'NA')
        
        # Add to merged data
        merged_data.append({
            'Unique Key': keyword,
            'Filename': filename,
            'Annotations': annotations_combined,
            'Ad Exchange/Server': ad_exchange,
            'Middle Parties': middle_parties,
            'Advertisers': advertisers,
        })

# Write to CSV
csv_columns = ['Unique Key', 'Filename', 'Annotations', 'Ad Exchange/Server', 'Middle Parties', 'Advertisers']
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    writer.writerows(merged_data)

print(f"CSV file created at: {output_csv}")
