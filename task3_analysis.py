import pandas as pd
import numpy as np

# Load the cleaned data from Task 2
df = pd.read_csv("data/trends_clean.csv")

print(f"Loaded data: {df.shape}")

# Display the first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Calculate and display the average score and comments
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print(f"\nAverage score   : {average_score:.2f}")
print(f"Average comments: {average_comments:.2f}")

# Convert the score column into a NumPy array for statistical calculations
scores = df["score"].to_numpy()

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")

# Count the number of stories in each category
category_counts = df["category"].value_counts()

most_common_category = category_counts.idxmax()
most_common_category_count = category_counts.max()

print(
    f"\nMost stories in: "
    f"{most_common_category} ({most_common_category_count} stories)"
)

# Find the story with the highest number of comments
most_commented_index = df["num_comments"].idxmax()
most_commented_story = df.loc[most_commented_index]

print(
    f'\nMost commented story: '
    f'"{most_commented_story["title"]}" '
    f'— {most_commented_story["num_comments"]} comments'
)

# Calculate how much discussion each story gets per upvote
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Mark stories whose score is above the overall average
df["is_popular"] = df["score"] > average_score

# Save the DataFrame with the new columns for Task 4
output_file = "data/trends_analysed.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")