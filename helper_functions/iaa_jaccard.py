import pandas as pd
import numpy as np

# Step 1: Read and preprocess the data
# df = pd.read_csv('common_csv_prompt4_4o.csv', quotechar='"', skip_blank_lines=False)
df = pd.read_csv('~/Downloads/Transformed_CSV_Data.csv', quotechar='"', skip_blank_lines=False)

def preprocess_annotations(cell):
    if pd.isna(cell) or str(cell).strip() == '':
        return set()
    else:
        labels = [l.strip() for l in str(cell).split(',')]
        return set(labels)

df_sets = df.applymap(preprocess_annotations)

# Step 2: Map annotations to indices
all_annotations = []
for col in df_sets.columns:
    all_annotations.extend(df_sets[col].tolist())

annotation_to_index = {frozenset(ann): idx for idx, ann in enumerate(set(frozenset(ann) for ann in all_annotations))}
index_to_annotation = {idx: ann for ann, idx in annotation_to_index.items()}
print(annotation_to_index)

df_indices = df_sets.applymap(lambda ann: annotation_to_index[frozenset(ann)])

# Step 3: Compute the disagreement matrix
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

# Step 4: Compute observed disagreement Do
Do_num = 0.0
Do_den = 0.0

n_items = df_indices.shape[0]

for i in range(n_items):
    annotations = df_indices.iloc[i, :].dropna().values
    n = len(annotations)
    if n <= 1:
        continue
    for m in range(n):
        for n_ in range(m + 1, n):
            ann_m = int(annotations[m])
            ann_n = int(annotations[n_])
            Do_num += disagreement_matrix[ann_m, ann_n]
    Do_den += n * (n - 1) / 2

Do = Do_num / Do_den if Do_den != 0 else 0.0

# Step 5: Compute expected disagreement De
annotation_counts = np.zeros(n_annotations)
for ann_list in df_indices.values.flatten():
    if not np.isnan(ann_list):
        annotation_counts[int(ann_list)] += 1

total_annotations = np.sum(annotation_counts)
probabilities = annotation_counts / total_annotations

De_num = 0.0
for i in range(n_annotations):
    for j in range(n_annotations):
        De_num += probabilities[i] * probabilities[j] * disagreement_matrix[i, j]

De = De_num

# Step 6: Calculate Krippendorff's alpha
alpha = 1.0 - (Do / De) if De != 0 else 0.0
print(f"Krippendorff's alpha (manual calculation): {alpha}")


annotators = df_indices.columns.tolist()
num_annotators = len(annotators)

for i in range(num_annotators):
    for j in range(i + 1, num_annotators):
        # Extract annotations for the two annotators
        pair_annotations = df_indices[[annotators[i], annotators[j]]]
        
        # Repeat Steps 4 to 6 for the pair
        Do_num_pair = 0.0
        Do_den_pair = 0.0

        for idx in range(n_items):
            annotations = pair_annotations.iloc[idx, :].dropna().values
            n = len(annotations)
            if n <= 1:
                continue
            ann_m = int(annotations[0])
            ann_n = int(annotations[1])
            Do_num_pair += disagreement_matrix[ann_m, ann_n]
            Do_den_pair += 1  # One pair per item

        Do_pair = Do_num_pair / Do_den_pair if Do_den_pair != 0 else 0.0

        # Compute De for the pair
        counts_pair = np.zeros(n_annotations)
        for ann_list in pair_annotations.values.flatten():
            if not np.isnan(ann_list):
                counts_pair[int(ann_list)] += 1

        total_counts_pair = np.sum(counts_pair)
        probs_pair = counts_pair / total_counts_pair

        De_num_pair = 0.0
        for m in range(n_annotations):
            for n_ in range(n_annotations):
                De_num_pair += probs_pair[m] * probs_pair[n_] * disagreement_matrix[m, n_]

        De_pair = De_num_pair

        alpha_pair = 1.0 - (Do_pair / De_pair) if De_pair != 0 else 0.0
        print(f"Krippendorff's alpha between {annotators[i]} and {annotators[j]}: {alpha_pair}")
