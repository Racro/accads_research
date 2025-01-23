import os
import json
import pandas as pd
import numpy as np
import sys

# Set the display options to show all columns and rows
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None) # This is the key line for showing full lines

def preprocess_annotations(cell):
    """Process individual cell annotations by splitting and stripping."""
    if pd.isna(cell) or cell.strip() == "DNA":
        return None  # DNA treated as invalid and removed from agreement process
    elif cell.strip() == "":
        return set()  # Empty string treated as legitimate empty set
    else:
        labels = [l.strip() for l in str(cell).split(';')]  # Split by ';' for multiple labels
        return set(labels)

def load_data(file_path):
    """Load data from either a JSON or CSV file."""
    if file_path.endswith('.json'):
        with open(file_path, 'r') as file:
            data = json.load(file)
            df = pd.DataFrame(data).fillna("DNA")
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path, sep='|', quotechar='"', skip_blank_lines=False).fillna("DNA")
    else:
        raise ValueError("Unsupported file format. Please provide a JSON or CSV file.")
    
    # Drop the 'Remarks' column if it exists
    if 'Remarks' in df.columns:
        df = df.drop(columns=['Remarks'])
    return df

def calculate_jaccard_distance_matrix(df):
    """Calculate Jaccard distance matrix for the given dataframe."""
    # Preprocess the dataframe
    df_sets = df.applymap(preprocess_annotations)
    # print(df_sets)

    # Map annotations to indices
    all_annotations = []
    for col in df_sets.columns:
        all_annotations.extend(df_sets[col].tolist())

    annotation_to_index = {frozenset(ann): idx for idx, ann in enumerate(set(frozenset(ann) for ann in all_annotations if ann is not None))}
    index_to_annotation = {idx: ann for ann, idx in annotation_to_index.items()}

    df_indices = df_sets.applymap(lambda ann: annotation_to_index[frozenset(ann)] if ann is not None else np.nan)

    # Compute the disagreement matrix
    n_annotations = len(annotation_to_index)
    disagreement_matrix = np.zeros((n_annotations, n_annotations))

    for i in range(n_annotations):
        ann_i = index_to_annotation[i]
        for j in range(i, n_annotations):
            ann_j = index_to_annotation[j]
            if not ann_i and not ann_j:
                distance = 0.0
            elif not ann_i or not ann_j:
                distance = 1.0
            else:
                intersection = len(ann_i & ann_j)
                union = len(ann_i | ann_j)
                distance = 1.0 - intersection / union
            disagreement_matrix[i, j] = distance
            disagreement_matrix[j, i] = distance

    return df_indices, disagreement_matrix, annotation_to_index

def calculate_krippendorffs_alpha(df_indices, disagreement_matrix):
    """Calculate Krippendorff's alpha for the given dataframe indices."""
    Do_num = 0.0
    Do_den = 0.0
    n_items = df_indices.shape[0]
    # print(n_items)
    for i in range(n_items):
        annotations = df_indices.iloc[i, :].dropna().values
        print(annotations)
        annotations = [int(a) for a in annotations if not np.isnan(a)]
        print(annotations)
        sys.exit(0)
        n = len(annotations)
        if n <= 1:
            continue
        for m in range(n):
            for n_ in range(m + 1, n):
                ann_m = annotations[m]
                ann_n = annotations[n_]
                Do_num += disagreement_matrix[ann_m, ann_n]
        Do_den += n * (n - 1) / 2

    Do = Do_num / Do_den if Do_den != 0 else 0.0

    annotation_counts = np.zeros(disagreement_matrix.shape[0])
    for ann_list in df_indices.values.flatten():
        if not np.isnan(ann_list):
            annotation_counts[int(ann_list)] += 1

    total_annotations = np.sum(annotation_counts)
    probabilities = annotation_counts / total_annotations

    De_num = 0.0
    for i in range(disagreement_matrix.shape[0]):
        for j in range(disagreement_matrix.shape[0]):
            De_num += probabilities[i] * probabilities[j] * disagreement_matrix[i, j]

    De = De_num
    alpha = 1.0 - (Do / De) if De != 0 else 0.0
    return alpha

def calculate_simple_agreement(df):
    """Calculate simple agreement for pairwise annotations."""
    n_items = df.shape[0]
    agreement_count = 0
    total_comparisons = 0

    for i in range(n_items):
        annotations = df.iloc[i, :]
        non_dna_annotations = [a for a in annotations if a != "DNA"]
        n = len(non_dna_annotations)
        if n <= 1:
            continue
        for m in range(n):
            for n_ in range(m + 1, n):
                if non_dna_annotations[m] == non_dna_annotations[n_]:
                    agreement_count += 1
                total_comparisons += 1

    simple_agreement = agreement_count / total_comparisons if total_comparisons != 0 else 0.0
    return simple_agreement

def calculate_binary_agreement(df):
    """Calculate binary agreement (presence or absence of any label)."""
    binary_df = df.applymap(lambda x: 1 if x is not None and x.strip() != "DNA" and x.strip() != "" else 0)

    n_items = binary_df.shape[0]
    agreement_count = 0
    total_comparisons = 0

    for i in range(n_items):
        row = binary_df.iloc[i, :]
        annotations = row[row != 0].values  # Ignore DNA or empty annotations
        n = len(annotations)
        if n <= 1:
            continue
        for m in range(n):
            for n_ in range(m + 1, n):
                if annotations[m] == annotations[n_]:
                    agreement_count += 1
                total_comparisons += 1

    binary_agreement = agreement_count / total_comparisons if total_comparisons != 0 else 0.0
    return binary_agreement

# Example usage:
csv_path = '~/Downloads/Merged_Annotations - Anno_3.csv'  # Update with the actual path
df = load_data(csv_path)
# df = pd.read_csv(csv_path, sep='|', quotechar='"', escapechar='\\', skip_blank_lines=False)

# Compute Jaccard distance matrix
df_indices, disagreement_matrix, annotation_to_index = calculate_jaccard_distance_matrix(df)
print(annotation_to_index)
# Calculate Krippendorff's alpha
alpha = calculate_krippendorffs_alpha(df_indices, disagreement_matrix)
print(f"Krippendorff's alpha: {alpha}")

# Calculate simple agreement
simple_agreement = calculate_simple_agreement(df)
print(f"Simple Agreement: {simple_agreement}")

# Calculate binary agreement
binary_agreement = calculate_binary_agreement(df)
print(f"Binary Agreement: {binary_agreement}")