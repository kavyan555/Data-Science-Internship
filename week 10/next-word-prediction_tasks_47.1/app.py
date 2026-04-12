import streamlit as st
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load models
rnn_model = load_model("rnn_model.h5")
lstm_model = load_model("lstm_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

max_len = 10  # adjust if needed

def predict(model, text):
    token_list = tokenizer.texts_to_sequences([text])[0]
    token_list = pad_sequences([token_list], maxlen=max_len-1, padding='pre')

    predicted = np.argmax(model.predict(token_list), axis=1)

    for word, index in tokenizer.word_index.items():
        if index == predicted:
            return word

st.title("Next Word Prediction (RNN vs LSTM)")

model_choice = st.selectbox("Choose Model", ["RNN", "LSTM"])
input_text = st.text_input("Enter text")

if st.button("Predict"):
    if input_text:
        if model_choice == "RNN":
            result = predict(rnn_model, input_text)
        else:
            result = predict(lstm_model, input_text)

        st.success(f"Next word: {result}")