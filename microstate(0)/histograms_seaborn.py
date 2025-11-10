import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


df = pd.read_csv("microstate(0)/interaction_vectors_microstate(0).csv")
selected_trials = [5, 10, 20, 30, 40]
df_filtered = df[df['TrialNumber'].isin(selected_trials)]

def microstate0_plots(df, run=False):
    if not run:
        print("run=False → Skipping plot generation.")
        return

    # Microstate(0) = 1 - ( |BN| / Trial )
    output_folder = "Microstate(0) Plots"
    os.makedirs(output_folder, exist_ok=True)

    experiment_cols = ['Content', 'Size', 'Structure', 'Run']
    bin_edges = [i / 10 for i in range(11)]

    for exp_vals, subset in df_filtered.groupby(experiment_cols):
        content, size, structure, run_num = exp_vals
        typecolor = "blue" if content == "Face" else "red"

        g = sns.FacetGrid(subset, col='TrialNumber', col_wrap=5, height=2.5, aspect=1.2)
        g.map_dataframe(
            sns.histplot,
            x='microstate',
            bins=bin_edges,
            stat='density',
            color=typecolor,
            edgecolor='black'
        )

        g.set_axis_labels("Microstate", "Density")
        g.set_titles("Trial {col_name}")

        # Adjust y-axis depending on content type
        height = 10 if content == "Face" else 6
        g.set(xlim=(0, 1), ylim=(0, height))

        exp_name = f"Content: {content} | Size: {size} | Structure: {structure} | Run: {run_num}"
        g.fig.suptitle(exp_name, fontsize=14, y=1.15)
        g.fig.subplots_adjust(top=0.75)

        safe_name = f"{content}_Size{size}_{structure}_Run{run_num}.png".replace(" ", "_")
        plt.savefig(os.path.join(output_folder, safe_name), bbox_inches='tight')
        plt.show()
        plt.close()

def microstate0_trend_plots(df, run=False):

    if not run:
        print("run=False → Skipping mean microstate dotplot generation.")
        return

    output_folder = "Microstate(0) Dotplots"
    os.makedirs(output_folder, exist_ok=True)

    # Keep only selected trials
    selected_trials = [5, 10, 15, 20, 25, 30, 35, 40]
    df_filtered = df[df['TrialNumber'].isin(selected_trials)]

    # Step 1: Group by Content, Structure, Size, TrialNumber across all individuals
    df_grouped = df_filtered.groupby(['Content', 'Structure', 'Size', 'TrialNumber'], as_index=False).agg(
        mean_microstate=('microstate', 'mean'),
        sd_microstate=('microstate', 'std')
    )

    # Define color mapping
    face_colors = {20: "#41a8df", 50: "#1258ad"}
    hashtag_colors = {20: "#ec4e3c", 50: "#b6130d", 100: "#67000d"}

    # Define the 4 experiment combinations
    plot_conditions = [
        ('Face', 'Homogeneous'),
        ('Face', 'Spatial'),
        ('Hashtag', 'Homogeneous'),
        ('Hashtag', 'Spatial'),
    ]

    for content, structure in plot_conditions:
        plt.figure(figsize=(6, 4))
        color_map = face_colors if content == 'Face' else hashtag_colors

        for size, color in color_map.items():
            subset = df_grouped[
                (df_grouped['Content'] == content) &
                (df_grouped['Structure'] == structure) &
                (df_grouped['Size'] == size)
            ]
            #ignore face, size = 100 
            if subset.empty:
                continue

            # Line connecting dots
            plt.plot(
                subset['TrialNumber'],
                subset['mean_microstate'],
                color=color,
                linewidth=1.0,
                alpha=0.8
            )

            # Scatter points
            plt.scatter(
                subset['TrialNumber'],
                subset['mean_microstate'],
                color=color,
                s=50,
                label=f"Group {size}"
            )

            # Error bars = SD of all individuals
            plt.errorbar(
                subset['TrialNumber'],
                subset['mean_microstate'],
                yerr=subset['sd_microstate'],
                fmt='none',
                ecolor=color,
                elinewidth=1,
                capsize=3,
                alpha=0.9
            )

        plt.title(f"Average Microstate: {content} - {structure}")
        plt.xlabel("Trial Number")
        plt.ylabel("Mean Microstate ± SD")
        plt.ylim(0, 1)
        plt.xticks(selected_trials)
        plt.legend(title="Group Size", frameon=False)
        plt.tight_layout()

        safe_name = f"{structure}_{content}_dotplot.png".replace(" ", "_")
        plt.savefig(os.path.join(output_folder, safe_name), bbox_inches='tight', dpi=300)
        plt.show()
        plt.close()

def microstate0_combined_histogram(df, run=False):
    if not run:
        print("run=False → Skipping histogram generation.")
        return

    output_folder = "Microstate(0)_Histograms"
    os.makedirs(output_folder, exist_ok=True)

    # Only include these trials
    selected_trials = [5, 10, 20, 30, 40]
    df_filtered = df[df['TrialNumber'].isin(selected_trials)]

    # Define the 4 experiment conditions
    plot_conditions = [
        ('Face', 'Homogeneous'),
        ('Face', 'Spatial'),
        ('Hashtag', 'Homogeneous'),
        ('Hashtag', 'Spatial'),
    ]

    # Bin edges for histograms
    bin_edges = [i / 10 for i in range(11)]

    for content, structure in plot_conditions:
        # Subset all participants for this condition
        subset = df_filtered[
            (df_filtered['Content'] == content) &
            (df_filtered['Structure'] == structure)
        ]

        if subset.empty:
            continue

        # Color
        typecolor = "blue" if content == "Face" else "red"

        # Create a FacetGrid faceted by TrialNumber
        g = sns.FacetGrid(subset, col='TrialNumber', col_wrap=5, height=2.5, aspect=1.2)

        # Plot histogram: each individual counts equally
        g.map_dataframe(
            sns.histplot,
            x='microstate',
            bins=bin_edges,
            stat='density',  # density ensures area = 1 per trial
            color=typecolor,
            edgecolor='black'
        )

        # Axis labels
        g.set_axis_labels("Microstate", "Density")
        g.set_titles("Trial {col_name}")

        # Adjust y-axis for content type
        height = 10 if content == "Face" else 6
        g.set(xlim=(0,1), ylim=(0,height))

        # Title
        g.fig.suptitle(f"Microstate Density Across all Runs: {content} - {structure}", fontsize=14, y=1.05)
        g.fig.subplots_adjust(top=0.85)

        safe_name = f"{structure}_{content}_histogram.png".replace(" ", "_")
        plt.savefig(os.path.join(output_folder, safe_name), bbox_inches='tight', dpi=300)
        plt.show()
        plt.close()

microstate0_plots(df, run=False) 
microstate0_trend_plots(df, run=True)
microstate0_combined_histogram(df, run=True)