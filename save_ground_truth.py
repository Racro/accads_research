import pandas as pd
import sys

# Set the display options to show all columns and rows
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None) # This is the key line for showing full lines


# Load the TSV file using the given path
# file_path = '/home/ritik/Downloads/Merged_Annotations_nolinks.tsv'
file_path = '/home/ritik/Downloads/Merged_Annotations - Anno_3.tsv'
file_path_nolinks = '/home/ritik/Downloads/Merged_Annotations_nolinks - Anno_3.tsv'

dataframes = [pd.read_csv(file_path, sep='\t', keep_default_na=False), pd.read_csv(file_path_nolinks, sep='\t', keep_default_na=False)]
# dataframes = [pd.read_csv(file_path, sep='\t', keep_default_na=False), pd.read_csv(file_path_nolinks, sep='\t', keep_default_na=False)]

df = pd.concat(dataframes, ignore_index=True)
# df = pd.read_csv(file_path, sep='\t', keep_default_na=False)  # Prevent empty strings from being treated as NaN
# print(df)

replacements = {'1_Germany': 'control_germany',
  '1_over18': 'control_over_18',
  '1_under_18': 'control_under_18',
  '1_US': 'control_US',
  '2_Germany': 'adblock_germany',
  '2_over18': 'adblock_over_18',
  '2_under_18': 'adblock_under_18',
  '2_US': 'adblock_US'}
# {
#     "{1_Germany}": "control_germany",
#     "{1_over18}": "control_over_18",
#     "{1_under_18}": "control_under_18",
#     "{1_US}": "control_US",
#     "{2_Germany}": "adblock_germany",
#     "{2_over18}": "adblock_over_18",
#     "{2_under_18}": "adblock_under_18",
#     "{2_US}": "adblock_US"
# }

# Ensure 'JSON Filename' is processed for replacements
if "JSON Filename" in df.columns:
    df["JSON Filename"] = df["JSON Filename"].replace(replacements, regex=True)
else:
    raise KeyError("The 'JSON Filename' column is missing from the DataFrame.")

# Annotation columns
annotation_columns = [
    'Filename', 'JSON Filename', 'hh3649@nyu.edu', 'pr2480@nyu.edu', 'cat.mai@nyu.edu',
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

def calculate_ground_truth(df_preprocessed, annotation_columns):
    """
    Calculate the ground truth for each image based on updated logic.

    Args:
    - df_preprocessed (pd.DataFrame): Preprocessed DataFrame with sets of annotations.
    - annotation_columns (list): Columns containing annotator annotations.

    Returns:
    - pd.Series: A series where each entry is the ground truth set of labels for an image.
    """
    ground_truths = []

    for _, row in df_preprocessed.iterrows():
        label_counts = {}
        benign_count = 0  # Count of empty set annotations

        # Count occurrences of each label across annotators
        for annotation in row[annotation_columns]:
            if annotation is not None:  # Exclude DNA
                if len(annotation) == 0:  # Empty set
                    benign_count += 1
                else:  # Non-empty set
                    for label in annotation:
                        label_counts[label] = label_counts.get(label, 0) + 1

        # Logic for determining the ground truth
        if benign_count >= 2 and not any(count >= 2 for count in label_counts.values()):
            # Majority of benign annotations and no label meets the threshold
            ground_truth = set()
        else:
            # Include only labels that appear at least twice
            ground_truth = {label for label, count in label_counts.items() if count >= 2}

        ground_truths.append(ground_truth)

    return pd.Series(ground_truths, index=df_preprocessed.index, name="Ground Truth")


def save_with_ground_truth(df_preprocessed, annotation_columns, output_file_path):
    """
    Calculate updated ground truth and save it along with specific columns to a CSV.

    Args:
    - df_preprocessed (pd.DataFrame): Preprocessed DataFrame with sets of annotations.
    - annotation_columns (list): Columns containing annotator annotations.
    - output_file_path (str): Path to save the output CSV.
    """
    # Calculate updated ground truth
    ground_truth_series = calculate_ground_truth(df_preprocessed, annotation_columns)

    # Create a new DataFrame with required columns
    output_df = df_preprocessed[["Filename", "JSON Filename"]].copy()
    output_df["Ground Truth"] = ground_truth_series

    # Convert ground truth sets to strings for saving in CSV
    output_df["Ground Truth"] = output_df["Ground Truth"].apply(lambda x: ";".join(x) if x else "")

    # Save to CSV
    output_df.to_csv(output_file_path, index=False)
    print(f"Updated DataFrame with ground truth saved to {output_file_path}")

# print(df.head(), df.columns)

# Preprocess the annotations
df_preprocessed = df[annotation_columns].applymap(preprocess_cell_annotations)
# print(df_preprocessed["JSON Filename"])

save_with_ground_truth(df_preprocessed, annotation_columns, 'merged_ground_truth.csv')

