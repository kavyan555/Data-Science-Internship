# =====================================
# IMPORT LIBRARIES
# =====================================
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import Trainer, TrainingArguments
 
# =====================================
# LOAD DATASET
# =====================================
df = pd.read_csv("ecommerce_reviews_1000.csv")
 
# =====================================
# CREATE LABEL FROM RATING
# =====================================
def convert_rating_to_label(rating):
    if rating >= 4:
        return 1   # Positive
    elif rating <= 2:
        return 0   # Negative
    else:
        return None  # Neutral
 
df['label'] = df['rating'].apply(convert_rating_to_label)
 
# Drop neutral values
df = df.dropna(subset=['label'])
 
# =====================================
# TRAIN-TEST SPLIT
# =====================================
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df['review_text'].tolist(),
    df['label'].tolist(),
    test_size=0.2,
    random_state=42
)
 
# =====================================
# TOKENIZATION
# =====================================
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
 
train_encodings = tokenizer(train_texts, truncation=True, padding=True)
val_encodings = tokenizer(val_texts, truncation=True, padding=True)
 
# =====================================
# DATASET CLASS (FIXED)
# =====================================
class ReviewDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
 
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)  # ✅ FIX
        return item
 
    def __len__(self):
        return len(self.labels)
 
train_dataset = ReviewDataset(train_encodings, train_labels)
val_dataset = ReviewDataset(val_encodings, val_labels)
 
# =====================================
# LOAD MODEL (FIXED)
# =====================================
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=2,
    problem_type="single_label_classification"   # ✅ FIX
)
 
# =====================================
# TRAINING ARGUMENTS (FIXED)
# =====================================
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    logging_dir='./logs',
    eval_strategy="epoch",     # ✅ FIX
    save_strategy="epoch"
)
 
# =====================================
# TRAINER
# =====================================
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)
 
# =====================================
# TRAIN MODEL
# =====================================
trainer.train()
 
# =====================================
# SAVE MODEL
# =====================================
model.save_pretrained("sentiment_model")
tokenizer.save_pretrained("sentiment_model")
 
print("✅ Model trained and saved successfully!")
 