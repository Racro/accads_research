import plotly.graph_objects as go
import matplotlib.colors as mcolors

# Define node labels and corresponding colors
labels = [
    "control_under_18", "control_over_18", "control_US", "control_germany",
    "Non_problematic", "Dark_Patterns_and_Manipulative_Design",
    "Political_and_Socially_Sensitive_Topics", "Deceptive_Claims_and_Exaggerated_Benefits",
    "Regulations", "Inappropriate_or_Offensive_Content", "User_Experience_Disruption",
    "adblock_under_18", "adblock_over_18", "adblock_US", "adblock_germany"
]

colors = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",  # Leftmost nodes
    "#bcbd22", "#17becf", "#aec7e8", "#ffbb78",  # Middle nodes
    "#98df8a", "#ff9896", "#c5b0d5",             # Middle nodes
    "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"   # Rightmost nodes
]

# Define source, target, and values for links
source_indices = [
    0, 0, 0, 0,  # control_under_18 to various categories
    1, 1, 1, 1,  # control_over_18 to various categories
    2, 2, 2, 2,  # control_US to various categories
    3, 3, 3, 3,  # control_germany to various categories
    4, 4, 4, 4, 4, 4, 4,  # categories to adblock_under_18
    5, 5, 5, 5, 5, 5, 5,  # categories to adblock_over_18
    6, 6, 6, 6, 6, 6, 6,  # categories to adblock_US
    7, 7, 7, 7, 7, 7, 7   # categories to adblock_germany
]

target_indices = [
    4, 5, 6, 7,  # control_under_18 to various categories
    4, 5, 6, 7,  # control_over_18 to various categories
    4, 5, 6, 7,  # control_US to various categories
    4, 5, 6, 7,  # control_germany to various categories
    11, 12, 13, 14,  # categories to adblock_under_18
    11, 12, 13, 14,  # categories to adblock_over_18
    11, 12, 13, 14,  # categories to adblock_US
    11, 12, 13, 14   # categories to adblock_germany
]

values = [
    116, 13, 0, 16,  # control_under_18 flows
    96, 25, 2, 24,   # control_over_18 flows
    114, 13, 0, 13,  # control_US flows
    100, 28, 0, 13,  # control_germany flows
    82, 17, 11, 32, 16, 3, 5,  # to adblock_under_18
    84, 26, 9, 22, 0, 4, 7,    # to adblock_over_18
    89, 22, 5, 16, 16, 4, 4,   # to adblock_US
    93, 29, 7, 23, 8, 1, 0     # to adblock_germany
]

# Map node labels to their colors
label_to_color = dict(zip(labels, colors))

# Determine link colors based on source and target nodes
link_colors = []
for src, tgt in zip(source_indices, target_indices):
    if src in [0, 1, 2, 3]:  # Leftmost nodes
        rgba_color = mcolors.to_rgba(label_to_color[labels[src]], alpha=0.45)
    elif tgt in [11, 12, 13, 14]:  # Rightmost nodes
        rgba_color = mcolors.to_rgba(label_to_color[labels[tgt]], alpha=0.45)
    else:  # Middle nodes
        rgba_color = mcolors.to_rgba("#B0B0B0", alpha=0.45)  # Gray with 45% opacity
    link_colors.append(f'rgba{rgba_color}')

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color=colors,
        hoverinfo='all'
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=values,
        color=link_colors,
        hoverinfo='all'
    )
)])

# Update layout for better visualization
fig.update_layout(
    title_text="Customized Sankey Diagram with Specific Styling",
    font=dict(size=12, color='black'),
    hovermode='x',
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Display the figure
fig.show()

# Save the figure as a static image
# fig.write_image("sankey_diagram.png")

# control_under_18 [116] Non-Problematic
# control_under_18 [13] Dark Patterns and Manipulative Design
# control_under_18 [0] Political and Socially Sensitive Topics
# control_under_18 [16] Deceptive Claims and Exaggerated Benefits
# control_under_18 [13] Regulations
# control_under_18 [1] Inappropriate or Offensive Content
# control_under_18 [5] User Experience Disruption
# control_over_18 [96] Non-Problematic
# control_over_18 [25] Dark Patterns and Manipulative Design
# control_over_18 [2] Political and Socially Sensitive Topics
# control_over_18 [24] Deceptive Claims and Exaggerated Benefits
# control_over_18 [0] Regulations
# control_over_18 [5] Inappropriate or Offensive Content
# control_over_18 [14] User Experience Disruption
# control_US [114] Non-Problematic
# control_US [13] Dark Patterns and Manipulative Design
# control_US [0] Political and Socially Sensitive Topics
# control_US [13] Deceptive Claims and Exaggerated Benefits
# control_US [7] Regulations
# control_US [2] Inappropriate or Offensive Content
# control_US [8] User Experience Disruption
# control_germany [100] Non-Problematic
# control_germany [28] Dark Patterns and Manipulative Design
# control_germany [0] Political and Socially Sensitive Topics
# control_germany [13] Deceptive Claims and Exaggerated Benefits
# control_germany [6] Regulations
# control_germany [3] Inappropriate or Offensive Content
# control_germany [3] User Experience Disruption

# Non-Problematic [82] adblock_under_18
# Dark Patterns and Manipulative Design [17] adblock_under_18
# Political and Socially Sensitive Topics [11] adblock_under_18
# Deceptive Claims and Exaggerated Benefits [32] adblock_under_18
# Regulations [16] adblock_under_18
# Inappropriate or Offensive Content [3] adblock_under_18
# User Experience Disruption [5] adblock_under_18
# Non-Problematic [84] adblock_over_18
# Dark Patterns and Manipulative Design [26] adblock_over_18
# Political and Socially Sensitive Topics [9] adblock_over_18
# Deceptive Claims and Exaggerated Benefits [22] adblock_over_18
# Regulations [0] adblock_over_18
# Inappropriate or Offensive Content [4] adblock_over_18
# User Experience Disruption [7] adblock_over_18
# Non-Problematic [89] adblock_US
# Dark Patterns and Manipulative Design [22] adblock_US
# Political and Socially Sensitive Topics [5] adblock_US
# Deceptive Claims and Exaggerated Benefits [16] adblock_US
# Regulations [16] adblock_US
# Inappropriate or Offensive Content [4] adblock_US
# User Experience Disruption [4] adblock_US
# Non-Problematic [93] adblock_germany
# Dark Patterns and Manipulative Design [29] adblock_germany
# Political and Socially Sensitive Topics [7] adblock_germany
# Deceptive Claims and Exaggerated Benefits [23] adblock_germany
# Regulations [8] adblock_germany
# Inappropriate or Offensive Content [1] adblock_germany
# User Experience Disruption [0] adblock_germany

# :control_under_18 #1f77b4
# :control_over_18 #ff7f0e
# :control_US #2ca02c
# :control_germany #d62728
# :adblock_under_18 #9467bd
# :adblock_over_18 #8c564b
# :adblock_US #e377c2
# :adblock_germany #7f7f7f
# :Non-Problematic #bcbd22
# :Dark Patterns and Manipulative Design #bcbd22
# :Political and Socially Sensitive Topics #bcbd22
# :Deceptive Claims and Exaggerated Benefits #bcbd22
# :Regulations #bcbd22
# :Inappropriate or Offensive Content #bcbd22
# :User Experience Disruption #bcbd22
