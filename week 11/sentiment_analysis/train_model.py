# =====================================
# IMPORT LIBRARIES
# =====================================
from datasets import load_dataset
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments

# =====================================
# LOAD DATASET
# =====================================
dataset = load_dataset('csv', data_files={'train': 'cleaned_reviews.csv'})

# =====================================
# LOAD TOKENIZER
# =====================================
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

# =====================================
# TOKENIZATION
# =====================================
def tokenize(example):
    return tokenizer(
        example['review_text'],
        truncation=True,
        padding='max_length',
        max_length=128
    )

dataset = dataset.map(tokenize, batched=True)

# =====================================
# FIX LABEL COLUMN
# =====================================
dataset = dataset.rename_column("label", "labels")

# IMPORTANT: ensure labels are int
def convert_labels(example):
    return {"labels": int(example["labels"])}

dataset = dataset.map(convert_labels)

# =====================================
# FORMAT FOR PYTORCH
# =====================================
dataset.set_format(
    type='torch',
    columns=['input_ids', 'attention_mask', 'labels']
)

# =====================================
# LOAD MODEL
# =====================================
model = DistilBertForSequenceClassification.from_pretrained(
    'distilbert-base-uncased',
    num_labels=2
)

# =====================================
# TRAINING CONFIG (FAST + STABLE)
# =====================================
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    logging_steps=10,
    save_strategy="epoch"
)

# =====================================
# TRAINER
# =====================================
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train']
)

# =====================================
# TRAIN
# =====================================
trainer.train()

# =====================================
# SAVE MODEL
# =====================================
trainer.save_model("sentiment_model")
tokenizer.save_pretrained("sentiment_model")

print("✅ DistilBERT Training Completed!")