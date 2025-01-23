import json
import re
import pandas as pd
from collections import defaultdict

keyword = 'control_US'
# Step 1: Load the provided JSON data
file_path = f'./exchange_info_{keyword}.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Step 1: Update the extraction function to remove redundant terms like "parent" and "server"
def clean_and_extract_entities_v4(text, keywords):
    """
    Extract ad exchanges, middle parties, and advertisers from the given text,
    and clean entries by handling unknown labels, unnecessary characters,
    isolated numbers, and redundant terms like "parent" or "server".
    """
    ad_exchanges, middle_parties, advertisers = set(), set(), set()
    
    # Define patterns for "unknown" or "not identifiable" entries
    unknown_patterns = [
        r'not explicitly identifiable',
        r'unknown',
        r'no specific',
        r'not specified',
        r'Various Ad Networks'
    ]
    
    # Define a blacklist of terms to exclude
    blacklist_terms = {'parent', 'server', 'exchange', 'ad exchange', 'middle party', 'middle parties'}
    
    # Split the text into lines for processing
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Extract entities in the format 'Entity (Role, Additional Info)'
        matches = re.findall(r'([^\(]+)\(([^)]+)\)', line)
        for entity, role in matches:
            entity = entity.strip()
            role = role.strip().lower()
            
            # Refined regex to handle additional information separated by commas, colons, or hyphens
            extra_info_matches = re.split(r'[,-;:]', role)
            primary_role = extra_info_matches[0].strip()
            extra_info_list = [info.strip() for info in extra_info_matches[1:]]
            
            # Classify based on the primary role and include extra information
            if 'exchange' in primary_role or 'server' in primary_role:
                ad_exchanges.add(entity)
                ad_exchanges.update(extra_info_list)
            elif 'middle' in primary_role or 'network' in primary_role or 'data' in primary_role or 'tracking' in primary_role:
                middle_parties.add(entity)
                middle_parties.update(extra_info_list)
            elif 'advertiser' in primary_role or 'retailer' in primary_role or 'publisher' in primary_role:
                advertisers.add(entity)
                advertisers.update(extra_info_list)
    
    # Step 2: Clean entries to remove non-alphanumeric characters, handle unknown entries, and remove isolated numbers
    def clean_entities(entities):
        # Remove non-alphanumeric characters and convert to uppercase
        cleaned = {re.sub(r'[^a-zA-Z0-9\s]', '', entity).strip() for entity in entities}
        # Remove isolated numbers (e.g., '1 RFI Hub' -> 'RFI Hub') but keep numbers within words (e.g., 'DV360')
        cleaned = {re.sub(r'\b\d+\b', '', entity).strip() for entity in cleaned}
        # Remove blacklisted terms like "parent" and "server"
        cleaned = {entity for entity in cleaned if entity.lower() not in blacklist_terms}
        # Replace entries that match any unknown pattern with 'N/A'
        cleaned = {'N/A' if any(re.search(pattern, entity.lower()) for pattern in unknown_patterns) else entity for entity in cleaned}
        # Convert the set to a list, join entities into a comma-separated string, and clean up extra commas
        cleaned = {entity for entity in cleaned if entity}
        # cleaned_string = ', '.join(cleaned).replace(',,', ',').strip(', ')
        # return cleaned if cleaned else 'N/A'
        return cleaned

    # Clean each category
    ad_exchanges = clean_entities(ad_exchanges)
    middle_parties = clean_entities(middle_parties)
    advertisers = clean_entities(advertisers)
    
    # Handle cases where no valid entries were found
    ad_exchanges = ad_exchanges if ad_exchanges else {'N/A'}
    middle_parties = middle_parties if middle_parties else {'N/A'}
    advertisers = advertisers if advertisers else {'N/A'}
    
    return list(ad_exchanges), list(middle_parties), list(advertisers)

# Step 2: Extract entities using the refined extraction logic
parsed_data_cleaned_v4 = []
for filename, text in data.items():
    # Extract entities with enhanced handling of unknown entries, character cleanup, and isolated numbers
    ad_exchanges, middle_parties, advertisers = clean_and_extract_entities_v4(text, {})

    # Only include entries with extracted information
    if ad_exchanges or middle_parties or advertisers:
        parsed_data_cleaned_v4.append({
            'File': filename,
            'Ad Exchange/Server': ', '.join(ad_exchanges) if ad_exchanges else 'N/A',
            'Middle Parties': ', '.join(middle_parties) if middle_parties else 'N/A',
            'Advertisers': ', '.join(advertisers) if advertisers else 'N/A'
        })

# Step 3: Convert the results into a DataFrame for better display
df_cleaned_v4 = pd.DataFrame(parsed_data_cleaned_v4)

# Step 4: Generate a JSON with the structured output
output_dict_v4 = {
    entry['File']: {
        'Ad Exchange/Server': entry['Ad Exchange/Server'],
        'Middle Parties': entry['Middle Parties'],
        'Advertisers': entry['Advertisers']
    }
    for entry in parsed_data_cleaned_v4
}

# Define the output file path
output_json_path = f'./cleaned_exchange_info_{keyword}.json'

# Save the structured data to a JSON file
# with open(output_json_path, 'w') as outfile:
#     json.dump(output_dict_v4, outfile, indent=4)

# Display the download link for the JSON file
# output_json_path

