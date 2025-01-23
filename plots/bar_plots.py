import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load and preprocess data
# file_path = '~/Downloads/category_label_frequencies.csv'  # Update this to your file path
file_path = '~/work/pes/accads_research/label_frequencies.csv'  # Update this to your file path
data = pd.read_csv(file_path)
data = data.rename(columns={'Unnamed: 0': 'Condition'})
# data['Condition'] = data['Condition'].str.strip("{}").str.replace("'", "")
data['Condition'] = data['Condition'].str.strip("{}").str.replace("'", "")

legend_replacements = {
    'control_germany': 'Control_Germany',
    'control_US': 'Control_US',
    'control_under_18': 'Control_under_18',
    'control_over_18': 'Control_over_18',
    'adblock_germany': 'Accads_Germany',
    'adblock_US': 'Accads_US',
    'adblock_under_18': 'Accads_under_18',
    'adblock_over_18': 'Accads_over_18'
}

# Function to replace keywords in legend labels
def replace_legend_labels(label, replacements):
    return replacements.get(label, label)

# Split the data into control and adblock conditions
control_data = data[data['Condition'].str.contains('control')].set_index('Condition')
adblock_data = data[data['Condition'].str.contains('adblock')].set_index('Condition')
print(control_data, adblock_data)
# Ensure numeric columns
columns_to_plot = data.columns[1:]
control_data = control_data[columns_to_plot].apply(pd.to_numeric)
adblock_data = adblock_data[columns_to_plot].apply(pd.to_numeric)

# Drop "Non-Problematic" and "Total Entries" columns
columns_to_keep = [col for col in control_data.columns if col not in ['Non problematic', 'Total Entries']]
control_data = control_data[columns_to_keep]
adblock_data = adblock_data[columns_to_keep]

# Abbreviation mapping for x-axis labels
abbreviations = {
    'Dark Patterns and Manipulative Design': 'DPMD',
    'Political and Socially Sensitive Topics': 'PST',
    'Deceptive Claims and Exaggerated Benefits': 'DCB',
    'Regulations': 'REG',
    'Inappropriate or Offensive Content': 'IOC',
    'User Experience Disruption': 'UED',
}

# Apply abbreviations dynamically
def abbreviate_columns(columns, abbreviation_map):
    return [abbreviation_map.get(col, next((abbr for full, abbr in abbreviation_map.items() if full in col), col)) for col in columns]

control_data.columns = abbreviate_columns(control_data.columns, abbreviations)
adblock_data.columns = abbreviate_columns(adblock_data.columns, abbreviations)

# Generate color-blind-friendly palette
color_palette = sns.color_palette("colorblind", 8)

# Define plotting function
def plot_control_and_adblock(control_data, adblock_data, title_control, title_adblock):
    x = np.arange(len(control_data.columns)) * 1.5  # Add spacing between groups
    bar_width = 0.25

    fig, axs = plt.subplots(1, 2, figsize=(18, 8), sharey=True)  # Shared y-axis

    # Control
    for i, (row_label, color) in enumerate(zip(control_data.index, color_palette[:4])):
        axs[0].bar(
            x + i * bar_width,
            control_data.loc[row_label],
            width=bar_width,
            label=replace_legend_labels(row_label, legend_replacements),
            # label=row_label,
            color=color,
        )
    axs[0].set_xticks(x + bar_width * (len(control_data.index) - 1) / 2)
    axs[0].set_xticklabels(control_data.columns, rotation=45, ha="right",  fontsize=20)
    axs[0].set_title(title_control, fontsize=20)
    axs[0].legend(loc='upper right', fontsize=20, frameon=False)
    axs[0].set_ylabel('# Problematic Ads', fontsize=20)
    axs[0].grid(axis='y', linestyle='--', linewidth=0.7)  # Add dotted gridlines for y-axis

    # Adblock
    for i, (row_label, color) in enumerate(zip(adblock_data.index, color_palette[4:])):
        axs[1].bar(
            x + i * bar_width,
            adblock_data.loc[row_label],
            width=bar_width,
            label=replace_legend_labels(row_label, legend_replacements),
            # label=row_label,
            color=color,
        )
    axs[1].set_xticks(x + bar_width * (len(adblock_data.index) - 1) / 2)
    axs[1].set_xticklabels(adblock_data.columns, rotation=45, ha="right", fontsize=20)
    axs[1].set_title(title_adblock, fontsize=20)
    axs[1].legend(loc='upper right', fontsize=20, frameon=False)
    axs[1].grid(axis='y', linestyle='--', linewidth=0.7)  # Add dotted gridlines for y-axis
    
    plt.tight_layout()
    plt.show()

# Define the desired order of conditions
desired_order = [
    'control_US',
    'control_germany',
    'control_under_18',
    'control_over_18',
    'adblock_US',
    'adblock_germany',
    'adblock_under_18',
    'adblock_over_18'
]

# Reorder the indices for control and adblock data
control_data = control_data.reindex([cond for cond in desired_order if 'control' in cond])
adblock_data = adblock_data.reindex([cond for cond in desired_order if 'adblock' in cond])

# Plot control and adblock subplots with reordered data
plot_control_and_adblock(
    control_data,
    adblock_data,
    "Comparison of Control group scenarios",
    "Comparison of Accads group scenarios"
)