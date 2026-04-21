# =====================================
# IMPORT LIBRARIES
# =====================================
import streamlit as st
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

# =====================================
# LOAD MODEL
# =====================================
model = DistilBertForSequenceClassification.from_pretrained("sentiment_model")
tokenizer = DistilBertTokenizer.from_pretrained("sentiment_model")

model.eval()

# =====================================
# PREDICTION FUNCTION
# =====================================
def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=1)
    pred = torch.argmax(probs).item()
    confidence = probs[0][pred].item()

    if pred == 1:
        return f"Positive 😊 ({confidence:.2f})"
    else:
        return f"Negative 😞 ({confidence:.2f})"

# =====================================
# UI
# =====================================
st.title("🛍️ Sentiment Analysis (DistilBERT - Trained Model)")
text = st.text_area("Enter Review")

if st.button("Analyze"):
    if text:
        st.success(predict_sentiment(text))
    else:
        st.warning("Enter some text")