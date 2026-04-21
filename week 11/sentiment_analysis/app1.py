# =====================================
# IMPORT LIBRARIES
# =====================================
import streamlit as st
from transformers import pipeline

# =====================================
# LOAD PIPELINE
# =====================================
sentiment = pipeline("sentiment-analysis")

# =====================================
# PREDICTION FUNCTION
# =====================================
def predict_sentiment(text):
    result = sentiment(text)[0]

    label = result['label']
    score = result['score']

    if label == "POSITIVE":
        return f"Positive 😊 "
    else:
        return f"Negative 😞 "

# =====================================
# UI
# =====================================
st.title("🛍️ Sentiment Analysis")
text = st.text_area("Enter Review")

if st.button("Analyze"):
    if text:
        st.success(predict_sentiment(text))
    else:
        st.warning("Enter some text")