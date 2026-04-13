# =====================================
# IMPORT LIBRARIES
# =====================================
import streamlit as st
import torch
from transformers import BertTokenizer, BertForSequenceClassification
 
# =====================================
# LOAD MODEL
# =====================================
model = BertForSequenceClassification.from_pretrained("sentiment_model")
tokenizer = BertTokenizer.from_pretrained("sentiment_model")
 
model.eval()
 
# =====================================
# PREDICTION FUNCTION
# =====================================
def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
   
    with torch.no_grad():
        outputs = model(**inputs)
   
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
   
    if predicted_class == 1:
        return "Positive 😊"
    else:
        return "Negative 😞"
 
# =====================================
# STREAMLIT UI
# =====================================
st.title("🛍️ Sentiment Analysis using BERT")
 
st.write("Analyze product reviews using Transformers")
 
user_input = st.text_area("Enter Review")
 
if st.button("Analyze"):
    if user_input.strip() != "":
        result = predict_sentiment(user_input)
        st.success(f"Sentiment: {result}")
    else:
        st.warning("Please enter some text")
 