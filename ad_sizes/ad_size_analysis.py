import json
import pandas as pd
import numpy as np
from scipy import stats
import sys 

def analyze_data(file_path, key):
    """
    Analyzes the input JSON file to calculate:
    - Mean, median, mode, 95th percentile, 99th percentile, and last 5 max values with filenames of numerical values (resource sizes) excluding zeros
    - Mean, median, mode, 95th percentile, 99th percentile, and last 5 max values with filenames of total resources per website,
      excluding websites with zero non-zero resources
    """
    # Load the JSON data from the given file path
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Extract numerical values and count total resources for each website
    numericals = []
    numerical_sources = []
    resource_counts = {}

    for website, resources in data.items():
        # Extract the second value (numerical) from each list, excluding zeros
        non_zero_values = [resource[1] for resource in resources if resource[1] != 0]
        numericals.extend(non_zero_values)
        
        # Track the source (filename) for each numerical value
        numerical_sources.extend([(resource[1], website) for resource in resources if resource[1] != 0])
        
        # Count non-zero resources for the current website
        non_zero_count = len(non_zero_values)
        
        # Only include websites with non-zero resources
        if non_zero_count > 0:
            resource_counts[website] = non_zero_count

    json.dump(numericals, open(f'plot_sizes_{key}.json', 'w'))
    json.dump(list(resource_counts.values()), open(f'plot_resources_{key}.json', 'w'))

    # Convert numerical values and total resources to NumPy arrays for efficient calculations
    numericals = np.array(numericals)
    total_resources = np.array(list(resource_counts.values()))
    # print(total_resources)
    # sys.exit(0)

    # Sort numerical values and total resources along with their sources
    sorted_numerical_sources = sorted(numerical_sources, key=lambda x: x[0], reverse=True)
    sorted_total_resources = sorted(resource_counts.items(), key=lambda x: x[1], reverse=True)

    # Calculate statistics for numerical values (sizes) excluding zeros
    if len(numericals) > 0:
        mean_size = np.mean(numericals)
        median_size = np.median(numericals)
        mode_size = stats.mode(numericals, keepdims=True)[0][0]
        p95_size = np.percentile(numericals, 95)
        p99_size = np.percentile(numericals, 99)
        top_5_max_sizes = sorted_numerical_sources[:5]  # Top 5 max values with filenames
    else:
        mean_size = median_size = mode_size = p95_size = p99_size = top_5_max_sizes = None

    # Calculate statistics for total resources excluding websites with zero non-zero resources
    if len(total_resources) > 0:
        mean_resources = np.mean(total_resources)
        median_resources = np.median(total_resources)
        mode_resources = stats.mode(total_resources, keepdims=True)[0][0]
        p95_resources = np.percentile(total_resources, 95)
        p99_resources = np.percentile(total_resources, 99)
        top_5_max_resources = sorted_total_resources[:5]  # Top 5 max values with filenames
    else:
        mean_resources = median_resources = mode_resources = p95_resources = p99_resources = top_5_max_resources = None

    # Display results for numerical values (sizes)
    print("Statistics for Non-Zero Resource Sizes:")
    print(f"Mean: {mean_size}, Median: {median_size}, Mode: {mode_size}")
    print(f"95th Percentile: {p95_size}, 99th Percentile: {p99_size}, Last 5 Max Values (with filenames): {top_5_max_sizes}")
    
    # Display results for total resources per website
    print("\nStatistics for Non-Zero Total Resources per Website:")
    print(f"Mean: {mean_resources}, Median: {median_resources}, Mode: {mode_resources}")
    print(f"95th Percentile: {p95_resources}, 99th Percentile: {p99_resources}, Last 5 Max Values (with filenames): {top_5_max_resources}")

    # Create a DataFrame for websites with non-zero resources
    resource_counts_df = pd.DataFrame(list(resource_counts.items()), columns=["Website", "Non-Zero Total Resources"])
    return resource_counts_df

lst = ['control_US', 'control_germany', 'control_over_18', 'control_under_18', 'accads_US', 'accads_germany', 'accads_over_18', 'accads_under_18']

for i in lst:
    # Example usage with the given file
    file_path = f'ad_sizes_{i}.json'
    result_df = analyze_data(file_path, i)
    print("\nNon-Zero Resource Counts by Website:\n", result_df)

