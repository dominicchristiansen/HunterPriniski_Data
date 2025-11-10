import pandas as pd
df = pd.read_csv("interaction_vectors_ORIGINAL.csv")

df["new_count"] = 0
df["microstate"] = 0.0

# Group by participant ID
for pid, group in df.groupby("random ID"):
    counter = 1  
    microstate_values = []
    new_counts = []

    for i, row in group.iterrows():
        trial_number = (len(new_counts) + 1)  # local trial count for this participant
        
        if trial_number == 1:
            counter = 1
        elif row["DecisionType"] == "BN":
            counter += 1

        new_counts.append(counter)
        microstate_values.append(1 - counter / trial_number)

    df.loc[group.index, "new_count"] = new_counts
    df.loc[group.index, "microstate"] = microstate_values

df.to_csv("interaction_vectors_microstate(11-2).csv", index=False)
print("done")
