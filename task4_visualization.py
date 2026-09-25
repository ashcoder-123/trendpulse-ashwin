import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the analysed data from Task 3
df = pd.read_csv("data/trends_analysed.csv")

# Create the output folder if it does not already exist
os.makedirs("outputs", exist_ok=True)

print(f"Loaded data: {df.shape}")

# Select the 10 stories with the highest scores
top_stories = df.nlargest(10, "score").copy()

# Shorten titles longer than 50 characters for the chart
top_stories["short_title"] = top_stories["title"].apply(
    lambda title: title[:50] + "..." if len(title) > 50 else title
)

# Create a horizontal bar chart
plt.figure(figsize=(10, 6))
plt.barh(top_stories["short_title"], top_stories["score"])

plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")

# Put the highest-scoring story at the top
plt.gca().invert_yaxis()

# Save the chart before displaying it
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")

plt.show()

# Count the number of stories in each category
category_counts = df["category"].value_counts()

# Create a bar chart for the category counts
plt.figure(figsize=(8, 5))
plt.bar(
    category_counts.index,
    category_counts.values,
    color=["red", "blue", "green", "orange", "purple"]
)

plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

# Save the chart before displaying it
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")

plt.show()

# Separate stories based on whether they are popular
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

# Create a scatter plot of score against number of comments
plt.figure(figsize=(8, 6))

plt.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular"
)

plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.legend()

# Save the chart before displaying it
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")

plt.show()

# Create a single dashboard containing all three charts
fig, axes = plt.subplots(1, 3, figsize=(20, 7))

# Chart 1: Top 10 stories by score
axes[0].barh(top_stories["short_title"], top_stories["score"])
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Story Title")
axes[0].invert_yaxis()

# Chart 2: Stories per category
axes[1].bar(
    category_counts.index,
    category_counts.values,
    color=["red", "blue", "green", "orange", "purple"]
)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")

# Chart 3: Score vs comments
axes[2].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)
axes[2].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular"
)
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].legend()

# Add an overall title to the dashboard
fig.suptitle("TrendPulse Dashboard", fontsize=18)

# Adjust the spacing between the charts
plt.tight_layout()

# Save the complete dashboard
plt.savefig("outputs/dashboard.png")

plt.show()