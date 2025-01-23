import pandas as pd
import sys

# Set the display options to show all columns and rows
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None) # This is the key line for showing full lines


# Load the TSV file using the given path
# file_path = '/home/ritik/Downloads/Merged_Annotations_nolinks.tsv'
file_path = '/home/ritik/Downloads/Merged_Annotations.tsv'
file_path_nolinks = '/home/ritik/Downloads/Merged_Annotations_nolinks.tsv'

dataframes = [pd.read_csv(file_path, sep='\t', keep_default_na=False), pd.read_csv(file_path_nolinks, sep='\t', keep_default_na=False)]

df = pd.concat(dataframes, ignore_index=True)
# df = pd.read_csv(file_path, sep='\t', keep_default_na=False)  # Prevent empty strings from being treated as NaN

# Annotation columns
annotation_columns = [
    'hh3649@nyu.edu', 'pr2480@nyu.edu', 'cat.mai@nyu.edu',
    'mm13032@nyu.edu', 'tdl7738@nyu.edu', 'ritik.r@nyu.edu', 'jj3545@nyu.edu'
]

# Preprocess each cell to convert annotations into sets
def preprocess_cell_annotations(cell):
    """
    Convert a cell containing annotations into a set of labels.

    Args:
    - cell (str): The cell content.

    Returns:
    - set: A set of labels, empty set for "", or None for DNA.
    """
    if cell.strip() == "DNA":
        return None  # Treat DNA as None (to ignore)
    elif cell.strip() == "":
        return set()  # Treat empty string as a valid empty set
    ret = []
    for label in cell.strip().split(';'):
        old = label
        label = label.split('(')[0].strip()
        if 'Deceptive' in label:
            label = label.split('-')[0].strip()
        label = label.split('(')[0].strip()
        # print('label_old:', old, 'label_new', label)
        if label != '':
            ret.append(label)
    return set(ret)

    # return set(cell.strip().split(';'))  # Split by ';' and convert to set

def build_annotation_to_index(df_preprocessed):
    """
    Build a mapping of unique annotation sets to indices.

    Args:
    - df_preprocessed (pd.DataFrame): Preprocessed DataFrame with sets of annotations.

    Returns:
    - dict: Mapping of unique annotation sets to unique indices.
    """
    unique_annotations = set()
    for col in df_preprocessed.columns:
        for cell in df_preprocessed[col]:
            if cell is not None:  # Exclude DNA
                # print(cell)
                unique_annotations.add(";".join(sorted(cell)) if cell else '')  # Handle empty set

    # Create a mapping from annotation set to index
    annotation_to_index = {annotation: idx for idx, annotation in enumerate(unique_annotations)}
    return annotation_to_index

# Preprocess the annotations
df_preprocessed = df[annotation_columns].applymap(preprocess_cell_annotations)
print(df_preprocessed.head())

# Build annotation-to-index mapping
annotation_to_index = build_annotation_to_index(df_preprocessed)
print(annotation_to_index)

# save_with_ground_truth(df_preprocessed, annotation_columns, './ground_truth.csv')

import numpy as np

def calculate_jaccard_distance_matrix(annotation_to_index):
    """
    Calculate the Jaccard distance matrix for unique annotation sets.

    Args:
    - annotation_to_index (dict): Mapping of unique annotation sets (as strings) to indices.

    Returns:
    - np.ndarray: Jaccard distance matrix.
    """
    # Reverse mapping to get annotation sets from indices
    index_to_annotation = {idx: ann for ann, idx in annotation_to_index.items()}
    n_annotations = len(annotation_to_index)

    # Initialize the distance matrix
    distance_matrix = np.zeros((n_annotations, n_annotations))

    # Calculate pairwise Jaccard distances
    for i in range(n_annotations):
        set_i = set(index_to_annotation[i].split(';'))  # Convert string back to set
        for j in range(i, n_annotations):
            set_j = set(index_to_annotation[j].split(';'))  # Convert string back to set

            if not set_i and not set_j:  # Both sets are empty
                distance = 0.0
            elif not set_i or not set_j:  # One set is empty, the other is not
                distance = 1.0
            else:
                intersection = len(set_i & set_j)
                union = len(set_i | set_j)
                distance = 1 - (intersection / union)

            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance  # Symmetric matrix

    return distance_matrix

def calculate_nominal_distance_matrix(annotation_to_index):
    """
    Calculate the Jaccard distance matrix for unique annotation sets.

    Args:
    - annotation_to_index (dict): Mapping of unique annotation sets (as strings) to indices.

    Returns:
    - np.ndarray: Jaccard distance matrix.
    """
    # Reverse mapping to get annotation sets from indices
    index_to_annotation = {idx: ann for ann, idx in annotation_to_index.items()}
    n_annotations = len(annotation_to_index)

    # Initialize the distance matrix
    distance_matrix = np.zeros((n_annotations, n_annotations))

    # Calculate pairwise Jaccard distances
    for i in range(n_annotations):
        set_i = set(index_to_annotation[i].split(';'))  # Convert string back to set
        for j in range(i, n_annotations):
            set_j = set(index_to_annotation[j].split(';'))  # Convert string back to set

            if not set_i and not set_j:  # Both sets are empty
                distance = 0.0
            elif not set_i or not set_j:  # One set is empty, the other is not
                distance = 1.0
            else:
                intersection = len(set_i & set_j)
                union = len(set_i | set_j)
                if intersection > 0:
                    distance = 0.0
                else:
                    distance = 1.0

            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance  # Symmetric matrix

    return distance_matrix

# Example usage:
jaccard_distance_matrix = calculate_jaccard_distance_matrix(annotation_to_index)
# jaccard_distance_matrix = calculate_nominal_distance_matrix(annotation_to_index)
print("Jaccard Distance Matrix:\n", jaccard_distance_matrix)

def calculate_observed_disagreement(df_preprocessed, annotation_to_index, jaccard_distance_matrix):
    """
    Calculate the observed disagreement (D_o) across all images.

    Args:
    - df_preprocessed (pd.DataFrame): Preprocessed DataFrame with sets of annotations.
    - annotation_to_index (dict): Mapping of unique annotation sets (as strings) to indices.
    - jaccard_distance_matrix (np.ndarray): Jaccard distance matrix.

    Returns:
    - float: Observed disagreement (D_o).
    """
    Do_num = 0.0  # Numerator for observed disagreement
    Do_den = 0.0  # Denominator (total number of comparisons)

    for _, row in df_preprocessed.iterrows():
        # Collect indices of valid annotation sets for the image
        valid_indices = [
            annotation_to_index[";".join(sorted(label))]
            for label in row if label is not None  # Ignore DNA
        ]

        n = len(valid_indices)
        if n <= 1:
            # Skip if fewer than 2 annotators provided annotations
            continue

        # Calculate pairwise disagreements for this image
        for i in range(n):
            for j in range(i + 1, n):
                idx_i = valid_indices[i]
                idx_j = valid_indices[j]
                Do_num += jaccard_distance_matrix[idx_i, idx_j]  # Sum disagreements

        Do_den += n * (n - 1) / 2  # Total number of pairwise comparisons

    # Calculate observed disagreement
    Do = Do_num / Do_den if Do_den > 0 else np.nan
    return Do

# Example usage:
Do = calculate_observed_disagreement(df_preprocessed, annotation_to_index, jaccard_distance_matrix)
print("Observed Disagreement (D_o):", Do)


def calculate_expected_disagreement(df_preprocessed, annotation_to_index, jaccard_distance_matrix):
    """
    Calculate the expected disagreement (D_e) across all images.

    Args:
    - df_preprocessed (pd.DataFrame): Preprocessed DataFrame with sets of annotations.
    - annotation_to_index (dict): Mapping of unique annotation sets to indices.
    - jaccard_distance_matrix (np.ndarray): Jaccard distance matrix.

    Returns:
    - float: Expected disagreement (D_e).
    """
    # Count the occurrences of each annotation set
    annotation_counts = np.zeros(len(annotation_to_index))
    for _, row in df_preprocessed.iterrows():
        for label in row:
            if label is not None:  # Exclude DNA
                key = ";".join(sorted(label))
                annotation_counts[annotation_to_index[key]] += 1

    # Calculate probabilities of each annotation set
    total_annotations = np.sum(annotation_counts)
    probabilities = annotation_counts / total_annotations

    # Calculate expected disagreement
    De = 0.0
    n_annotations = len(annotation_to_index)
    for i in range(n_annotations):
        for j in range(n_annotations):
            De += probabilities[i] * probabilities[j] * jaccard_distance_matrix[i, j]

    return De

# Example usage:
De = calculate_expected_disagreement(df_preprocessed, annotation_to_index, jaccard_distance_matrix)
print("Expected Disagreement (D_e):", De)

def calculate_krippendorffs_alpha(Do, De):
    """
    Calculate Krippendorff's alpha.

    Args:
    - Do (float): Observed disagreement.
    - De (float): Expected disagreement.

    Returns:
    - float: Krippendorff's alpha.
    """
    if De == 0:
        raise ValueError("Expected disagreement (D_e) is zero, Krippendorff's alpha cannot be calculated.")
    
    alpha = 1 - (Do / De)
    return alpha

# Example usage:
alpha = calculate_krippendorffs_alpha(Do, De)
print("Krippendorff's Alpha (α):", alpha)


############################
# Label Wise alpha
############################
def calculate_observed_disagreement_binary(binary_matrix):
    """
    Calculate observed disagreement (D_o) for a binary presence matrix.

    Args:
    - binary_matrix (pd.DataFrame): Binary presence matrix for a single label.

    Returns:
    - float: Observed disagreement (D_o).
    """
    Do_num = 0.0
    Do_den = 0.0

    for _, row in binary_matrix.iterrows():
        # Drop NaN values for valid annotations
        annotations = row.dropna().values
        n = len(annotations)
        if n <= 1:
            continue

        # Calculate pairwise disagreements
        for i in range(n):
            for j in range(i + 1, n):
                Do_num += abs(annotations[i] - annotations[j])  # Binary disagreement

        Do_den += n * (n - 1) / 2  # Total pairwise comparisons

    return Do_num / Do_den if Do_den > 0 else 0

def calculate_expected_disagreement_binary(binary_matrix):
    """
    Calculate expected disagreement (D_e) for a binary presence matrix.

    Args:
    - binary_matrix (pd.DataFrame): Binary presence matrix for a single label.

    Returns:
    - float: Expected disagreement (D_e).
    """
    # Count 1s (presence) and total annotations (ignoring NaN)
    presence_counts = binary_matrix.sum().sum()  # Sum across entire DataFrame
    total_annotations = binary_matrix.count().sum()  # Total number of non-NaN values

    if total_annotations == 0:
        return 0.0

    # Probabilities of presence (1) and absence (0)
    p1 = presence_counts / total_annotations  # Probability of 1
    p0 = 1 - p1  # Probability of 0

    # Expected disagreement for binary classification
    De = 2 * p1 * p0
    return float(De)  # Ensure the return value is a scalar float



def calculate_krippendorffs_alpha_binary(binary_matrix):
    """
    Calculate Krippendorff's Alpha (α) for a binary presence matrix.

    Args:
    - binary_matrix (pd.DataFrame): Binary presence matrix for a single label.

    Returns:
    - float: Krippendorff's Alpha (α).
    """
    Do = calculate_observed_disagreement_binary(binary_matrix)
    De = calculate_expected_disagreement_binary(binary_matrix)

    if De == 0.0:  # Safeguard against division by zero
        return np.nan
    return 1 - (Do / De)


# Extract all unique labels
all_labels = set(label for cell in df_preprocessed.values.flatten() if cell for label in cell)

# Initialize a dictionary to store Krippendorff's Alpha for each label
label_agreements = {}

for label in all_labels:
    # Create binary presence matrix for this label
    binary_matrix = pd.DataFrame(index=df_preprocessed.index, columns=annotation_columns)
    for col in annotation_columns:
        binary_matrix[col] = df_preprocessed[col].apply(
            lambda x: 1 if x is not None and label in x else (0 if x is not None else np.nan)
        )

    # Calculate Krippendorff's Alpha
    alpha = calculate_krippendorffs_alpha_binary(binary_matrix)
    label_agreements[label] = alpha

# Print label-specific agreements
for label, alpha in label_agreements.items():
    print(f"Label: {label}, Krippendorff's Alpha: {alpha}")


############################
# Alpha with ground truth
# Step 1: Create the ground truth label based on the condition
# Binary value is 1 if there are >= 2 ones in the row, else 0

# Function to calculate Krippendorff's Alpha
def calculate_krippendorffs_alpha_with_ground_truth(binary_matrix, annotation_columns, ground_truth_column):
    """
    Calculate Krippendorff's Alpha for annotators compared to the ground truth.

    Args:
    - binary_matrix (pd.DataFrame): Binary matrix of annotator labels and ground truth.
    - annotation_columns (list): List of annotator column names.
    - ground_truth_column (str): Name of the ground truth column.

    Returns:
    - float: Krippendorff's Alpha (α).
    """
    ground_truth = binary_matrix[ground_truth_column]
    Do_num = 0.0
    Do_den = 0.0

    # Observed disagreement
    for annotator in annotation_columns:
        annotator_values = binary_matrix[annotator]
        valid_indices = annotator_values.notna() & ground_truth.notna()
        annotator_values = annotator_values[valid_indices].values
        gt_values = ground_truth[valid_indices].values

        Do_num += np.abs(annotator_values - gt_values).sum()
        Do_den += len(gt_values)

    Do = Do_num / Do_den if Do_den > 0 else 0

    # Expected disagreement
    total_ones = binary_matrix[annotation_columns].sum().sum() + ground_truth.sum()
    total_values = binary_matrix[annotation_columns].count().sum() + ground_truth.count()
    p1 = total_ones / total_values
    p0 = 1 - p1
    De = 2 * p1 * p0

    # Calculate Alpha
    return 1 - (Do / De) if De > 0 else np.nan

# Main loop to calculate label-specific agreement
label_agreements = {}

for label in all_labels:
    # Create binary presence matrix for this label
    binary_matrix = pd.DataFrame(index=df_preprocessed.index, columns=annotation_columns)
    for col in annotation_columns:
        binary_matrix[col] = df_preprocessed[col].apply(
            lambda x: 1 if x is not None and label in x else (0 if x is not None else np.nan)
        )

    # Create ground truth column
    binary_matrix['ground_truth'] = binary_matrix.apply(
        lambda row: 1 if row.sum() >= 2 else 0, axis=1
    )

    # Calculate Krippendorff's Alpha for this label
    alpha = calculate_krippendorffs_alpha_with_ground_truth(
        binary_matrix, annotation_columns, 'ground_truth'
    )
    label_agreements[label] = alpha

# Print label-specific agreements
print("Krippendorff's Alpha for each label with ground truth:")
for label, alpha in label_agreements.items():
    print(f"Label: {label}, Krippendorff's Alpha: {alpha}")

############################
# Annotator agreements
############################
def filter_images_with_annotator(df_preprocessed, annotator):
    """
    Filter images where a specific annotator is present.

    Args:
    - df_preprocessed (pd.DataFrame): Preprocessed DataFrame with sets of annotations.
    - annotator (str): The specific annotator column to filter by.

    Returns:
    - pd.DataFrame: Filtered DataFrame where the annotator is present.
    """
    return df_preprocessed[df_preprocessed[annotator].notnull()]

def calculate_ground_truth(df_preprocessed, annotation_columns):
    """
    Calculate the ground truth for each image based on labels occurring at least twice.

    Args:
    - df_preprocessed (pd.DataFrame): Preprocessed DataFrame with sets of annotations.
    - annotation_columns (list): Columns containing annotator annotations.

    Returns:
    - pd.Series: A series where each entry is the ground truth set of labels for an image.
    """
    ground_truths = []

    for _, row in df_preprocessed.iterrows():
        label_counts = {}
        benign_count = 0

        # Count occurrences of each label across annotators
        for annotation in row[annotation_columns]:
            if annotation is not None:  # Exclude DNA
                if isinstance(annotation, (str)) and annotation == "":
                    benign_count += 1  # Count benign (empty) annotations
                else:
                    for label in annotation:
                        label_counts[label] = label_counts.get(label, 0) + 1

        # Determine ground truth based on counts
        if benign_count >= 2 and not any(count >= 2 for count in label_counts.values()):
            ground_truth = set()  # Keep empty set as ground truth
        else:
            ground_truth = {label for label, count in label_counts.items() if count >= 2}

        ground_truths.append(ground_truth)

    return pd.Series(ground_truths, index=df_preprocessed.index, name="Ground Truth")

def calculate_alpha_for_annotator(filtered_df, annotation_to_index):
    """
    Calculate Krippendorff's alpha for a specific annotator.

    Args:
    - filtered_df (pd.DataFrame): Filtered DataFrame with annotator and ground truth columns.
    - annotation_to_index (dict): Mapping of unique annotation sets to indices.

    Returns:
    - float: Krippendorff's alpha for the annotator.
    """
    # Map annotations to indices
    def process_annotation(annotation):
        if isinstance(annotation, (set, list)):
            return ";".join(sorted(annotation))
        elif isinstance(annotation, str) and annotation != "":
            return annotation
        elif annotation is None or annotation == "":
            return ""
        else:
            raise ValueError(f"Unexpected annotation type: {type(annotation)}")
    
    filtered_df = filtered_df.applymap(process_annotation)
    df_indices = filtered_df.applymap(lambda x: annotation_to_index.get(x, -1))

    # Filter out invalid indices (-1)
    valid_indices = df_indices[(df_indices >= 0).all(axis=1)]

    if valid_indices.empty:
        return 0.0  # No valid data

    # Calculate Krippendorff's alpha
    Do = calculate_observed_disagreement(valid_indices, annotation_to_index, jaccard_distance_matrix)
    De = calculate_expected_disagreement(valid_indices, annotation_to_index, jaccard_distance_matrix)
    return calculate_krippendorffs_alpha(Do, De)


def calculate_per_annotator_alpha(df_preprocessed, annotation_columns, annotation_to_index):
    """
    Calculate Krippendorff's alpha for each annotator based on the ground truth.

    Args:
    - df_preprocessed (pd.DataFrame): Preprocessed DataFrame with sets of annotations.
    - annotation_columns (list): Columns containing annotator annotations.
    - annotation_to_index (dict): Mapping of unique annotation sets to indices.

    Returns:
    - dict: Krippendorff's alpha scores for each annotator.
    """
    ground_truth_series = calculate_ground_truth(df_preprocessed, annotation_columns)

    annotator_alphas = {}

    for annotator in annotation_columns:
        # Filter images where the annotator is present
        filtered_df = filter_images_with_annotator(df_preprocessed, annotator)

        if filtered_df.empty:
            annotator_alphas[annotator] = 0.0  # No data for this annotator
            continue

        # Create a DataFrame with annotator and ground truth
        filtered_df = filtered_df[[annotator]].copy()
        filtered_df["Ground Truth"] = ground_truth_series.loc[filtered_df.index]

        # Calculate Krippendorff's alpha for this annotator
        alpha = calculate_alpha_for_annotator(filtered_df, annotation_to_index)
        annotator_alphas[annotator] = alpha

    return annotator_alphas

# Example Usage
# # Define annotation columns
# annotation_columns = [
#     "hh3649@nyu.edu", "pr2480@nyu.edu", "cat.mai@nyu.edu", "mm13032@nyu.edu", "tdl7738@nyu.edu", "ritik.r@nyu.edu", "jj3545@nyu.edu"
# ]
# # print(annotation_to_index)
# # Compute Krippendorff's alpha per annotator
# per_annotator_alpha = calculate_per_annotator_alpha(df_preprocessed, annotation_columns, annotation_to_index)

# # Display results
# for annotator, alpha in per_annotator_alpha.items():
#     print(f"Annotator: {annotator}, Krippendorff's Alpha: {alpha:.4f}")



#############################
# Binary and Non-Problematic agreement
#############################
def calculate_binary_agreements_with_average(df_preprocessed, annotation_columns, annotation_to_index, jaccard_distance_matrix):
    """
    Calculate binary nominal agreement (average) and Krippendorff's alpha for binary classification.

    Args:
    - df_preprocessed (pd.DataFrame): Preprocessed DataFrame with sets of annotations.
    - annotation_columns (list): Columns containing annotator annotations.
    - annotation_to_index (dict): Mapping of unique annotation sets to indices.
    - jaccard_distance_matrix (np.ndarray): Jaccard distance matrix.

    Returns:
    - tuple: (float avg_nominal_agreement, float alpha value for binary classification).
    """
    nominal_agreements = []

    Do_num = 0.0
    Do_den = 0.0
    annotation_counts = np.zeros(2)  # Binary annotations: 0 (non-problematic) and 1 (problematic)

    for _, row in df_preprocessed.iterrows():
        binary_annotations = [
            1 if label is not None and len(label) > 0 else 0
            for label in row[annotation_columns]
            if label is not None  # Exclude DNA
        ]
        n = len(binary_annotations)
        if n <= 1:
            # Skip if fewer than 2 valid annotators
            continue

        # Nominal agreement calculation
        agree_count = sum(
            1 for i in range(n) for j in range(i + 1, n)
            if binary_annotations[i] == binary_annotations[j]
        )
        total_pairs = n * (n - 1) / 2
        nominal_agreement = agree_count / total_pairs if total_pairs > 0 else np.nan
        nominal_agreements.append(nominal_agreement)

        # Observed disagreement (D_o)
        for i in range(n):
            for j in range(i + 1, n):
                Do_num += abs(binary_annotations[i] - binary_annotations[j])

        Do_den += n * (n - 1) / 2

        # Count annotation occurrences for D_e
        for b in binary_annotations:
            annotation_counts[b] += 1

    # Average nominal agreement
    avg_nominal_agreement = np.nanmean(nominal_agreements)

    # Observed disagreement (D_o)
    Do = Do_num / Do_den if Do_den > 0 else np.nan

    # Expected disagreement (D_e)
    total_annotations = np.sum(annotation_counts)
    probabilities = annotation_counts / total_annotations

    De = 0.0
    for i in range(len(probabilities)):
        for j in range(len(probabilities)):
            De += probabilities[i] * probabilities[j] * abs(i - j)

    # Krippendorff's alpha
    alpha = 1 - (Do / De) if De > 0 else np.nan

    return avg_nominal_agreement, alpha


def calculate_problematic_agreements_with_average(df_preprocessed, annotation_columns, annotation_to_index, jaccard_distance_matrix):
    """
    Calculate problematic categories nominal agreement (average) and Krippendorff's alpha.

    Args:
    - df_preprocessed (pd.DataFrame): Preprocessed DataFrame with sets of annotations.
    - annotation_columns (list): Columns containing annotator annotations.
    - annotation_to_index (dict): Mapping of unique annotation sets to indices.
    - jaccard_distance_matrix (np.ndarray): Jaccard distance matrix.

    Returns:
    - tuple: (float avg_nominal_agreement, float alpha value for problematic categories).
    """
    nominal_agreements = []

    Do_num = 0.0
    Do_den = 0.0

    for _, row in df_preprocessed.iterrows():
        # Collect indices of problematic annotations (exclude empty sets and DNA)
        problematic_indices = [
            annotation_to_index[";".join(sorted(label))]
            for label in row[annotation_columns]
            if label is not None and len(label) > 0
        ]

        n = len(problematic_indices)
        if n <= 1:
            # Skip if fewer than 2 valid annotators
            continue

        # Nominal agreement calculation
        pairwise_agreements = []
        for i in range(n):
            for j in range(i + 1, n):
                idx_i = problematic_indices[i]
                idx_j = problematic_indices[j]
                agreement = 1 - jaccard_distance_matrix[idx_i, idx_j]  # Convert distance to agreement
                pairwise_agreements.append(agreement)
                Do_num += jaccard_distance_matrix[idx_i, idx_j]

        Do_den += n * (n - 1) / 2
        avg_agreement = np.mean(pairwise_agreements) if pairwise_agreements else np.nan
        nominal_agreements.append(avg_agreement)

    # Average nominal agreement
    avg_nominal_agreement = np.nanmean(nominal_agreements)

    # Observed disagreement (D_o)
    Do = Do_num / Do_den if Do_den > 0 else np.nan

    # Expected disagreement (D_e)
    annotation_counts = np.zeros(len(annotation_to_index))
    for _, row in df_preprocessed.iterrows():
        for label in row[annotation_columns]:
            if label is not None and len(label) > 0:
                key = ";".join(sorted(label))
                annotation_counts[annotation_to_index[key]] += 1

    total_annotations = np.sum(annotation_counts)
    probabilities = annotation_counts / total_annotations

    De = 0.0
    for i in range(len(probabilities)):
        for j in range(len(probabilities)):
            De += probabilities[i] * probabilities[j] * jaccard_distance_matrix[i, j]

    # Krippendorff's alpha
    alpha = 1 - (Do / De) if De > 0 else np.nan

    return avg_nominal_agreement, alpha

# Binary Classification Agreement
binary_avg_nominal, binary_alpha = calculate_binary_agreements_with_average(
    df_preprocessed, annotation_columns, annotation_to_index, jaccard_distance_matrix
)
print(f"Average Binary Nominal Agreement: {binary_avg_nominal}")
print(f"Binary Classification Krippendorff's Alpha: {binary_alpha}")

# Problematic Categories Agreement
problematic_avg_nominal, problematic_alpha = calculate_problematic_agreements_with_average(
    df_preprocessed, annotation_columns, annotation_to_index, jaccard_distance_matrix
)
print(f"Average Problematic Nominal Agreement: {problematic_avg_nominal}")
print(f"Problematic Categories Krippendorff's Alpha: {problematic_alpha}")


######################
# Label-wise Agreements
######################

# def create_binary_presence_matrix(df_preprocessed, annotation_columns, all_labels):
#     """
#     Create a binary presence matrix for each label across all images, ignoring DNA.

#     Args:
#     - df_preprocessed (pd.DataFrame): Preprocessed DataFrame with sets of annotations.
#     - annotation_columns (list): Columns containing annotator annotations.
#     - all_labels (set): Set of all unique labels.

#     Returns:
#     - dict: A dictionary where each key is a label, and the value is a binary presence matrix (pd.DataFrame).
#     """
#     binary_matrices = {}

#     for label in all_labels:
#         # Create a binary matrix for the current label
#         binary_matrix = pd.DataFrame(index=df_preprocessed.index, columns=annotation_columns)

#         for col in annotation_columns:
#             # Apply presence check for each annotator
#             binary_matrix[col] = df_preprocessed[col].apply(
#                 lambda x: 1 if x is not None and label in x else (0 if x is not None else np.nan)
#             )

#         binary_matrices[label] = binary_matrix

#     return binary_matrices

# # Example usage:
# all_labels = set(label for cell in df_preprocessed.values.flatten() if cell for label in cell)
# binary_presence_matrices = create_binary_presence_matrix(df_preprocessed, annotation_columns, all_labels)
# # print(all_labels)
# # print(binary_presence_matrices)

# def calculate_label_agreement(binary_matrix):
#     """
#     Calculate Krippendorff's alpha for a binary presence matrix, ignoring NaN.

#     Args:
#     - binary_matrix (pd.DataFrame): Binary presence matrix for a single label.

#     Returns:
#     - float: Krippendorff's alpha for the label.
#     """
#     # Observed disagreement
#     Do_num = 0.0
#     Do_den = 0.0

#     for _, row in binary_matrix.iterrows():
#         # Drop NaN values for this image
#         annotations = row.dropna().values
#         n = len(annotations)
#         if n <= 1:
#             continue

#         for i in range(n):
#             for j in range(i + 1, n):
#                 Do_num += abs(annotations[i] - annotations[j])  # Binary disagreement

#         Do_den += n * (n - 1) / 2

#     Do = Do_num / Do_den if Do_den > 0 else np.nan

#     # Expected disagreement
#     annotation_counts = binary_matrix.sum(axis=0).values
#     total_annotations = np.sum(annotation_counts)
#     probabilities = annotation_counts / total_annotations

#     De_num = 0.0
#     for i in range(len(probabilities)):
#         for j in range(len(probabilities)):
#             De_num += probabilities[i] * probabilities[j] * abs(i - j)

#     De = De_num

#     # Krippendorff's alpha
#     alpha = 1 - (Do / De) if De > 0 else np.nan
#     return alpha

# # Example usage:
# # label_agreements = {label: calculate_label_agreement(binary_matrix)
# #                     for label, binary_matrix in binary_presence_matrices.items()}
# # print("Label-wise Agreements:", label_agreements)



# #####################
# # DEBUG FUNCTIONS
# #####################

# def calculate_observed_disagreement_debug(df_preprocessed, annotation_to_index, jaccard_distance_matrix):
#     """
#     Calculate the observed disagreement (D_o) with debug outputs.

#     Args:
#     - df_preprocessed (pd.DataFrame): Preprocessed DataFrame with sets of annotations.
#     - annotation_to_index (dict): Mapping of unique annotation sets to indices.
#     - jaccard_distance_matrix (np.ndarray): Jaccard distance matrix.

#     Returns:
#     - float: Observed disagreement (D_o).
#     """
#     Do_num = 0.0  # Numerator for observed disagreement
#     Do_den = 0.0  # Denominator (total number of comparisons)

#     for image_id, row in df_preprocessed.iterrows():
#         # Collect indices of valid annotation sets for the image
#         valid_indices = [
#             annotation_to_index[";".join(sorted(label))]
#             for label in row if label is not None  # Ignore DNA
#         ]

#         n = len(valid_indices)
#         if n <= 1:
#             # Skip if fewer than 2 annotators provided annotations
#             continue

#         # Debug: Print valid indices for the image
#         print(f"Image {image_id}: Valid Indices = {valid_indices}")

#         # Calculate pairwise disagreements for this image
#         for i in range(n):
#             for j in range(i + 1, n):
#                 idx_i = valid_indices[i]
#                 idx_j = valid_indices[j]
#                 disagreement = jaccard_distance_matrix[idx_i, idx_j]
#                 Do_num += disagreement

#                 # Debug: Print pairwise disagreement
#                 print(f"  Pair ({idx_i}, {idx_j}): Disagreement = {disagreement}")

#         Do_den += n * (n - 1) / 2  # Total number of pairwise comparisons

#     # Debug: Print numerator and denominator for D_o
#     print(f"Do_num = {Do_num}, Do_den = {Do_den}")

#     Do = Do_num / Do_den if Do_den > 0 else np.nan
#     return Do


# def calculate_expected_disagreement_debug(df_preprocessed, annotation_to_index, jaccard_distance_matrix):
#     """
#     Calculate the expected disagreement (D_e) with debug outputs.

#     Args:
#     - df_preprocessed (pd.DataFrame): Preprocessed DataFrame with sets of annotations.
#     - annotation_to_index (dict): Mapping of unique annotation sets to indices.
#     - jaccard_distance_matrix (np.ndarray): Jaccard distance matrix.

#     Returns:
#     - float: Expected disagreement (D_e).
#     """
#     # Count the occurrences of each annotation set
#     annotation_counts = np.zeros(len(annotation_to_index))
#     for image_id, row in df_preprocessed.iterrows():
#         for label in row:
#             if label is not None:  # Exclude DNA
#                 key = ";".join(sorted(label))
#                 annotation_counts[annotation_to_index[key]] += 1

#     # Debug: Print annotation counts
#     print("Annotation Counts:", annotation_counts)

#     # Calculate probabilities of each annotation set
#     total_annotations = np.sum(annotation_counts)
#     probabilities = annotation_counts / total_annotations

#     # Debug: Print probabilities
#     print("Probabilities:", probabilities)

#     # Calculate expected disagreement
#     De = 0.0
#     n_annotations = len(annotation_to_index)
#     for i in range(n_annotations):
#         for j in range(n_annotations):
#             De += probabilities[i] * probabilities[j] * jaccard_distance_matrix[i, j]

#             # Debug: Print pairwise expected disagreement contribution
#             print(f"  Pair ({i}, {j}): Contribution = {probabilities[i] * probabilities[j] * jaccard_distance_matrix[i, j]}")

#     # Debug: Print final De
#     print(f"Expected Disagreement (D_e) = {De}")

#     return De


# Do = calculate_observed_disagreement_debug(df_preprocessed, annotation_to_index, jaccard_distance_matrix)
# print(f"Observed Disagreement (D_o): {Do}")

# De = calculate_expected_disagreement_debug(df_preprocessed, annotation_to_index, jaccard_distance_matrix)
# print(f"Expected Disagreement (D_e): {De}")

# alpha = calculate_krippendorffs_alpha(Do, De)
# print(f"Krippendorff's Alpha (α): {alpha}")

########################