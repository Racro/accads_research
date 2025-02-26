import pandas as pd

# Load the CSV file
# Load the TSV file using the given path
# file_path = 'ground_truth.csv'
# file_path_nolinks = 'ground_truth_nolinks.csv'

# dataframes = [pd.read_csv(file_path), pd.read_csv(file_path_nolinks)]

# data = pd.concat(dataframes, ignore_index=True)
data = pd.read_csv('merged_ground_truth.csv')  # Prevent empty strings from being treated as NaN

# Replace NaN values in 'Ground Truth' column with empty strings
data['Ground Truth'] = data['Ground Truth'].fillna('')

# Split the 'Ground Truth' column into lists of labels
data['Ground Truth Split'] = data['Ground Truth'].apply(lambda x: x.split(';'))

# Get unique values in "JSON Filename"
unique_values = data['JSON Filename'].unique()

# Count the number of rows for each unique value in "JSON Filename"
total_entries = data['JSON Filename'].value_counts()

# Initialize a dictionary to store counts for each unique value in 'JSON Filename'
counts = {key: {} for key in unique_values}

# Count occurrences of each label for each unique 'JSON Filename'
for _, row in data.iterrows():
    json_value = row['JSON Filename']
    labels = row['Ground Truth Split']
    for label in labels:
        label = label.strip()  # Remove leading/trailing whitespace
        # Map empty strings to "Non problematic"
        if label == '':
            label = 'Non problematic'
        counts[json_value][label] = counts[json_value].get(label, 0) + 1

# Convert the counts dictionary to a DataFrame
counts_df = pd.DataFrame.from_dict(counts, orient='index').fillna(0).astype(int)

# Add a "Total Entries" column based on the number of rows per unique value
counts_df['Total Entries'] = counts_df.index.map(total_entries)

# Sort rows based on the reverse of the "JSON Filename" column strings
counts_df = counts_df.sort_index(key=lambda idx: idx.str[::-1])

# Check if the total matches the number of rows in the dataset
assert counts_df['Total Entries'].sum() == len(data), "Total entries sum does not match the total number of rows."

counts_df.to_csv('label_frequencies.csv')