import streamlit as st
from transformers import pipeline, CLIPProcessor, CLIPModel
from PIL import Image
import torch
import librosa
import io
import numpy as np

# ---------------- LOAD MODELS ----------------
@st.cache_resource
def load_pipelines():
    return {
        "sentiment": pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        ),
        "generator": pipeline(
            "text-generation",
            model="gpt2"
        ),
        "image_classifier": pipeline(
            "image-classification",
            model="google/vit-base-patch16-224"
        ),
        "asr": pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-small"
        ),
    }

@st.cache_resource
def load_clip():
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return model, processor

pipelines = load_pipelines()
clip_model, clip_processor = load_clip()

# ---------------- UI ----------------
st.title("AI Playground with Transformers")

task = st.sidebar.selectbox(
    "Choose a task:",
    ["Sentiment Analysis", "Text Generation", "Image Classification", "Automatic Speech Recognition"]
)

# ---------------- SENTIMENT ----------------
if task == "Sentiment Analysis":
    text = st.text_area("Enter text:", "I love using transformers for AI projects")

    if st.button("Analyze"):
        result = pipelines["sentiment"](text)[0]
        st.write(f"Sentiment: {result['label']}")
        st.write(f"Score: {result['score']:.4f}")

# ---------------- TEXT GENERATION ----------------
elif task == "Text Generation":
    prompt = st.text_area("Enter prompt:", "Once upon a time")

    if st.button("Generate"):
        result = pipelines["generator"](
            prompt,
            max_length=50,
            num_return_sequences=1
        )[0]
        st.write(result["generated_text"])

# ---------------- IMAGE CLASSIFICATION ----------------
elif task == "Image Classification":
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Classify"):
            result = pipelines["image_classifier"](image)
            st.write(f"Prediction: {result[0]['label']}")
            st.write(f"Confidence: {result[0]['score']:.4f}")

# ---------------- ASR ----------------
elif task == "Automatic Speech Recognition":
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

    if uploaded_file is not None:
        st.audio(uploaded_file)

        if uploaded_file.size > 10 * 1024 * 1024:
            st.warning("File too large (max 10MB)")
        else:
            if st.button("Recognize"):
                with st.spinner("Transcribing..."):
                    try:
                        # Convert file → numpy array
                        audio_bytes = uploaded_file.read()
                        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)

                        # Convert stereo → mono
                        if len(audio.shape) > 1:
                            audio = np.mean(audio, axis=1)

                        # Run ASR
                        result = pipelines["asr"](audio)

                        st.success("Transcription:")
                        st.write(result["text"])

                    except Exception as e:
                        st.error(f"Error: {e}")