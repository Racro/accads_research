import scipy.stats as stats 
import numpy as np
from scipy.stats import fisher_exact

def find_z(x1, n1, x2, n2, scene):
    # Example data: Replace with your counts and totals 
    # x1, n1 = 54, 150  # Group 1 (e.g., Control): 40 successes out of 150 
    # x2, n2 = 66, 140  # Group 2 (e.g., Adblock): 60 successes out of 150 
    
    # Proportions 
    p1 = x1 / n1 
    p2 = x2 / n2 
    
    # Pooled proportion 
    p = (x1 + x2) / (n1 + n2) 
    
    # Standard error 
    se = np.sqrt(p * (1 - p) * (1/n1 + 1/n2)) 
    
    # Z-statistic 
    z_stat = (p1 - p2) / se 
    
    # One-tailed p-value (for p1 < p2) 
    p_value_one_tail = stats.norm.cdf(z_stat) 
    
    # Output 
    print("One-Tailed Z-Test", scene) 
    print(p1, p2)
    print(f"Z-Statistic: {z_stat}") 
    print(f"P-Value (One-Tailed): {p_value_one_tail}") 
    print("Significant?" if p_value_one_tail < 0.05 else "Not Significant")

def find_z_two_tailed(x1, n1, x2, n2, scene):
    # Compute proportions for each group
    p1 = x1 / n1 
    p2 = x2 / n2 
    
    # Calculate the pooled proportion
    p = (x1 + x2) / (n1 + n2) 
    
    # Standard error of the difference in proportions
    se = np.sqrt(p * (1 - p) * (1/n1 + 1/n2)) 
    
    # Z-statistic for the difference in proportions
    z_stat = (p1 - p2) / se 
    
    # Two-tailed p-value: double the one-tailed p-value based on the absolute value of z
    p_value_two_tail = 2 * stats.norm.sf(abs(z_stat))
    
    # Output the results
    print("Two-Tailed Z-Test", scene) 
    print("Proportion 1:", p1, "Proportion 2:", p2)
    print(f"Z-Statistic: {z_stat}") 
    print(f"P-Value (Two-Tailed): {p_value_two_tail}") 
    print("Significant?" if p_value_two_tail < 0.05 else "Not Significant")

# Example usage:
# find_z_two_tailed(54, 150, 66, 140, "Example Scene")


def fisher(control_occurrence, n1, adblock_occurrence, n2):
    # Example Data: Replace with your observed counts
    # control_occurrence = 10  # Number of times the label occurs in the control group
    control_non_occurrence = n1 - control_occurrence  # Complement in control group
    # adblock_occurrence = 12  # Number of times the label occurs in the adblock group
    adblock_non_occurrence = n2 - adblock_occurrence  # Complement in adblock group

    # Construct Contingency Table
    contingency_table = [[control_occurrence, control_non_occurrence],
                        [adblock_occurrence, adblock_non_occurrence]]

    # Perform Fisher's Exact Test
    # odds_ratio, p_value = fisher_exact(contingency_table, alternative='two-sided')
    odds_ratio, p_value = fisher_exact(contingency_table, alternative='greater')

    # Output Results
    print(f"Contingency Table: {contingency_table}")
    print(f"Odds Ratio: {odds_ratio}")
    print(f"P-Value: {p_value}")
    print("Significant?" if p_value < 0.05 else "Not Significant")


n1 = 150 # 150
n2 = 150 # 150
# ctrl = [0,0] # [34, 36]
# adb = [13,16] # [54, 50]
adb = [68, 66, 61, 57]
ctrl = [21, 54, 36, 50]
# adb = [66, 57]
# ctrl = [54, 50]
# scenario = ['over_18', 'germany']

# ctrl = [34, 54, 36, 50]
# adb = [52, 66, 61, 57]
scenario = ['under_18', 'over_18', 'US', 'germany']
for i in range(len(ctrl)):
    find_z(ctrl[i], n1, adb[i], n2, scenario[i])
    # fisher(ctrl[i], n1, adb[i], n2)
    print('-'*50)

find_z(ctrl[0], n1, ctrl[1], n2, 'adblock_18')