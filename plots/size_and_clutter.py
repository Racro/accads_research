# import matplotlib.pyplot as plt
# import numpy as np

# category = 'size'
# category = ''

# # Data
# x_labels = ['A', 'B', 'C', 'D']
# group1 = [10, 15, 20, 25]
# group2 = [12, 18, 22, 28]

# # Define bar width and x positions
# x = np.arange(len(x_labels))  # Positions for x labels
# bar_width = 0.15

# # Adjust figure size to decrease gaps
# plt.figure(figsize=(4, 4))  # Adjust width and height

# # Plot bars
# plt.bar(x - bar_width / 2, group1, width=bar_width, label='Group 1', color='#0072B2')
# plt.bar(x + bar_width / 2, group2, width=bar_width, label='Group 2', color='#E69F00')

# # Customization
# plt.xticks(x, x_labels)  # Add x-labels at positions
# plt.ylabel('Values')
# plt.title('Bar Plot with Adjacent Bars')
# plt.legend()

# # Display
# plt.tight_layout()
# plt.show()



import matplotlib.pyplot as plt
import numpy as np
import json

def plot_graph(group1, group2):
    # Only for resources graph
    categories = ['UnAuth_US', 'UnAuth_Germany', 'Over_18', 'Under_18']
    group1_mean = []
    group1_99 = []
    group2_mean = []
    group2_99 = []

    for i in range(len(categories)):
        a1 = np.array(group1[i])#/1000
        a2 = np.array(group2[i])#/1000

        group1_mean.append(np.mean(a1))
        group2_mean.append(np.mean(a2))
        group1_99.append(np.percentile(a1, 95))
        group2_99.append(np.percentile(a2, 95))

    # Calculate differences (99th percentile - mean)
    group1_diff = np.array(group1_99) - np.array(group1_mean)
    group2_diff = np.array(group2_99) - np.array(group2_mean)

    # Define bar width and positions
    bar_width = 0.2
    x = np.arange(len(categories))

    # Plotting
    fig, ax = plt.subplots(figsize=(5.3, 4))

    # Group 1 bars
    bars1_mean = ax.bar(x - bar_width/2, group1_mean, bar_width, label='Group 1 Mean')
    bars1_diff = ax.bar(x - bar_width/2, group1_diff, bar_width, bottom=group1_mean, label='Group 1 99% Diff')

    # Group 2 bars
    bars2_mean = ax.bar(x + bar_width/2, group2_mean, bar_width, label='Group 2 Mean')
    bars2_diff = ax.bar(x + bar_width/2, group2_diff, bar_width, bottom=group2_mean, label='Group 2 99% Diff')

    # # Overlay line graphs
    # ax.plot(x - bar_width/2, group1_line_data, marker='o', linestyle='-', color='blue', label='Group 1 Line')
    # ax.plot(x + bar_width/2, group2_line_data, marker='o', linestyle='-', color='red', label='Group 2 Line')

    # Define custom legend
    custom_legend_labels = [
        "Control: Mean",
        "Control: P95 Diff",
        "Acceptable Ads: Mean",
        "Acceptable Ads: P95 Diff"
    ]
    custom_handles = [
        bars1_mean,
        bars1_diff,
        bars2_mean,
        bars2_diff
    ]

    # Calculate the maximum value in the data
    max_value = max(max(group1_99), max(group2_99))

    # Add padding to the top of the y-axis
    # padding = 25
    padding = 200
    ax.set_ylim(0, max_value + padding)

    # Add labels, title, and legend
    # ax.set_ylabel('Values (in KB)')
    ax.set_ylabel('Values')
    # ax.set_title('Ad Sizes in Different Scenarios')
    ax.set_title('Total Ad Resources in Different Scenarios')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    # Add custom legend
    ax.legend(custom_handles, custom_legend_labels, loc='upper center', ncols=2)

    # Show the plot
    plt.tight_layout()
    plt.show()
    
def clutter():
    group2_line_data = [3.31, 3.53, 3.28, 3.57]
    group1_line_data = [4.71, 4.81, 4.59, 4.73]

    categories = ['UnAuth_US', 'UnAuth_Germany', 'Over_18', 'Under_18']

    # Define x positions for categories
    x = np.arange(len(categories))

    # Create the plot
    plt.figure(figsize=(5, 4))

    # Plot Group 1 line
    plt.plot(x, group1_line_data, marker='o', linestyle='-', color='blue', label='Control')

    # Plot Group 2 line
    plt.plot(x, group2_line_data, marker='o', linestyle='-', color='red', label='Accads')

    # Customize the plot
    plt.xticks(ticks=x, labels=categories, fontsize=10)
    plt.yticks(np.arange(0, max(max(group1_line_data), max(group2_line_data)) + 5, 1))  # Y-axis from 0 with step of 1
    plt.ylim(2, max(max(group1_line_data), max(group2_line_data)) + 1)  # Ensure the axis starts at 0
    plt.ylabel('Values', fontsize=10)
    plt.title('Avg Ads Per Page', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(alpha=0.5)

    # Show the plot
    plt.tight_layout()
    plt.show()


lst = ['control_US', 'control_germany', 'control_over_18', 'control_under_18', 'accads_US', 'accads_germany', 'accads_over_18', 'accads_under_18']

group1 = []
group2 = []

for i in lst:
    if 'control' in i:
        print(i)
        # group1.append(json.load(open(f'../ad_sizes/plot_sizes_{i}.json', 'r')))
        group1.append(json.load(open(f'../ad_sizes/plot_resources_{i}.json', 'r')))
    else:
        print(i)
        # group2.append(json.load(open(f'../ad_sizes/plot_sizes_{i}.json', 'r')))
        group2.append(json.load(open(f'../ad_sizes/plot_resources_{i}.json', 'r')))

# plot_graph(group1, group2)
# clutter()

import matplotlib.pyplot as plt
import numpy as np
import json

def boxplot_grouped_with_means(json_files, categories):
    # Initialize lists for grouped data
    control_data = []  # Control group data
    accads_data = []  # Accads group data

    # Process each file and categorize data
    for idx, file_path in enumerate(json_files):
        with open(f'../avg_ads/avg_ads_{file_path}', 'r') as file:
            data = json.load(file)

        if idx < 4:  # First 4 files are Control group
            control_data.append(data)
        else:  # Last 4 files are Accads group
            accads_data.append(data)

    # Print statistics for each category
    for i, category in enumerate(categories):
        # Control group statistics
        control_mean = np.mean(control_data[i])
        control_median = np.median(control_data[i])
        control_q1, control_q3 = np.percentile(control_data[i], [25, 75])
        print(f"Control - {category}: Mean = {control_mean:.2f}, Median = {control_median:.2f}, IQR = [{control_q1:.2f}, {control_q3:.2f}]")

        # Accads group statistics
        accads_mean = np.mean(accads_data[i])
        accads_median = np.median(accads_data[i])
        accads_q1, accads_q3 = np.percentile(accads_data[i], [25, 75])
        print(f"Accads - {category}: Mean = {accads_mean:.2f}, Median = {accads_median:.2f}, IQR = [{accads_q1:.2f}, {accads_q3:.2f}]")

    # Create the boxplot
    plt.figure(figsize=(6, 4))  # Reduced width and height for a compact figure

    # Clustered positions for boxplots
    num_categories = len(categories)
    cluster_width = 0.15  # Narrower boxplots for compact size
    spacing = 0.05  # Smaller spacing between Control and Accads within each cluster
    control_positions = np.arange(num_categories) - (cluster_width + spacing) / 2
    accads_positions = np.arange(num_categories) + (cluster_width + spacing) / 2

    # Plot Control group boxplots
    box_control = plt.boxplot(control_data, positions=control_positions, widths=cluster_width, patch_artist=True,
                              boxprops=dict(facecolor='lightblue'),
                              medianprops=dict(color='darkblue', linewidth=2))

    # Plot Accads group boxplots
    box_accads = plt.boxplot(accads_data, positions=accads_positions, widths=cluster_width, patch_artist=True,
                             boxprops=dict(facecolor='lightcoral'),
                             medianprops=dict(color='darkred', linewidth=2))

    # Add mean markers and lines for Control group
    for i, mean in enumerate([np.mean(data) for data in control_data]):
        # plt.scatter(control_positions[i], mean, color='black', zorder=3, label='Mean' if i == 0 else None)
        plt.plot([control_positions[i] - cluster_width / 2, control_positions[i] + cluster_width / 2],
                 [mean, mean], linestyle='dotted', color='black')

    # Add mean markers and lines for Accads group
    for i, mean in enumerate([np.mean(data) for data in accads_data]):
        # plt.scatter(accads_positions[i], mean, color='black', zorder=3)
        plt.plot([accads_positions[i] - cluster_width / 2, accads_positions[i] + cluster_width / 2],
                 [mean, mean], linestyle='dotted', color='black')

    # Customize the plot
    plt.xticks(ticks=np.arange(num_categories), labels=categories, fontsize=14, ha='center')
    plt.ylabel('Values', fontsize=14)
    plt.title('Avg Ads Per Page', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # Adjust x-axis limits to squeeze the plot horizontally
    plt.xlim(-0.5, num_categories - 0.5)
    plt.ylim(0, 12)

    # Add a legend
    plt.legend(handles=[
        plt.Line2D([0], [0], color='lightblue', lw=5, label='Control'),
        plt.Line2D([0], [0], color='lightcoral', lw=5, label='Accads'),
        plt.Line2D([0], [0], color='black', linestyle='dotted', linewidth=2, label='Mean'),
        plt.Line2D([0], [0], color='black', linestyle='-', linewidth=2, label='Median')
    ], loc='upper right', ncol=2, fontsize=11, frameon=False)

    # Adjust layout for compactness
    plt.tight_layout(pad=0.5)

    # Show the plot
    plt.show()

# List of JSON file paths
json_files = [
    'control_US.json', 'control_germany.json', 'control_over_18.json', 'control_under_18.json',
    'accads_US.json', 'accads_germany.json', 'accads_over_18.json', 'accads_under_18.json'
]

# Categories for the x-axis
categories = ['US', 'Germany', 'Over_18', 'Under_18']

# Call the function
boxplot_grouped_with_means(json_files, categories)

