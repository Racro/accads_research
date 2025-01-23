import pandas as pd
import numpy as np
import krippendorff
from itertools import combinations
import sys

# Step 1: Read the CSV data into a pandas DataFrame
df = pd.read_csv('common_csv_prompt2.csv', quotechar='"', skip_blank_lines=False)

# Step 2: Preprocess the Data
def preprocess_annotations(cell):
    if pd.isna(cell) or str(cell).strip() == '':
        return 'No Annotation'  # Represent empty entries as 'No Annotation'
    else:
        labels = [l.strip() for l in str(cell).split(',')]
        # Sort labels to have a consistent representation
        labels.sort()
        # Join labels with a separator to form a unique category
        return '|'.join(labels)

df_processed = df.applymap(preprocess_annotations)

# Step 3: Map annotations to numerical codes
# Create a mapping from unique categories to codes
all_categories = set()
for col in df_processed.columns:
    all_categories.update(df_processed[col].unique())

category_to_code = {category: idx for idx, category in enumerate(sorted(all_categories))}
code_to_category = {idx: category for category, idx in category_to_code.items()}

# sys.exit(0)
# Convert annotations to codes
df_numeric = df_processed.applymap(lambda x: category_to_code[x])

# Step 4: Prepare the reliability data array
data_array = df_numeric.values.T  # Shape: (annotators x items)

# Step 5: Compute Krippendorff's alpha using the nominal metric
alpha_collective = krippendorff.alpha(reliability_data=data_array, level_of_measurement='nominal')
print("Collective Krippendorff's alpha (nominal):", alpha_collective)

# Step 6: Compute pairwise Krippendorff's alpha between annotators
annotators = df_numeric.columns.tolist()
num_annotators = len(annotators)

for i in range(num_annotators):
    for j in range(i + 1, num_annotators):
        pair_data = df_numeric[[annotators[i], annotators[j]]].values.T
        alpha_pair = krippendorff.alpha(reliability_data=pair_data, level_of_measurement='nominal')
        print(f"Krippendorff's alpha between {annotators[i]} and {annotators[j]}:", alpha_pair)
