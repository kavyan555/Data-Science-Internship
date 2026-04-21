import pandas as pd

df = pd.read_csv("cleaned_reviews.csv")

# Convert to integer
df['label'] = df['label'].astype(int)

# Save again
df.to_csv("cleaned_reviews.csv", index=False)

print("✅ Labels fixed")
print(df['label'].dtype)