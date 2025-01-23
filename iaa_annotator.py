import pandas as pd

# Load the TSV files
file_path = "/mnt/data/Merged_Annotations.tsv"
file_path_nolinks = "/mnt/data/Merged_Annotations_nolinks.tsv"

# Load dataframes
df1 = pd.read_csv(file_path, sep='\t', keep_default_na=False)
df2 = pd.read_csv(file_path_nolinks, sep='\t', keep_default_na=False)

# Combine the dataframes
df = pd.concat([df1, df2], ignore_index=True)

# Display the first few rows of the combined dataframe
import ace_tools as tools; tools.display_dataframe_to_user(name="Combined Annotations Data", dataframe=df)

# Define annotator columns for preprocessing
annotator_columns = [
    "hh3649@nyu.edu", "pr2480@nyu.edu", "cat.mai@nyu.edu",
    "mm13032@nyu.edu", "tdl7738@nyu.edu", "ritik.r@nyu.edu", "jj3545@nyu.edu"
]

def preprocess_annotations(cell):
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

# Apply preprocessing to the annotator columns
df[annotator_columns] = df[annotator_columns].applymap(preprocess_annotations)

# Display a sample of preprocessed annotations to verify
tools.display_dataframe_to_user(name="Preprocessed Annotations Data", dataframe=df[annotator_columns].head())


