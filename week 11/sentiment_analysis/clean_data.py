import pandas as pd

df = pd.read_csv("ecommerce_reviews_1000.csv")

def get_label(rating):
    if rating <= 2:
        return 0
    elif rating >= 4:
        return 1
    else:
        return None

df['label'] = df['rating'].apply(get_label)

df = df.dropna()

df = df[['review_text', 'label']]

df.to_csv("cleaned_reviews.csv", index=False)

print(df['label'].value_counts())