import streamlit as st
from sentence_transformers import SentenceTransformer
import pinecone
import numpy as np
import tempfile
from pathlib import Path
import os
 
# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Semantic Search Engine",
    page_icon="🔍",
    layout="wide"
)
 
# -----------------------------
# LIGHT THEME CSS
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #f8fafc;
    color: #0f172a;
}
 
.stTextInput > div > div > input {
    background-color: #ffffff;
    color: #0f172a;
    border-radius: 10px;
    border: 1px solid #cbd5e1;
}
 
.stFileUploader {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
}
 
.result-box {
    background-color: #ffffff;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 15px;
    border: 1px solid #e2e8f0;
}
 
.score {
    color: #2563eb;
    font-size: 18px;
    font-weight: bold;
}
 
.title-style {
    text-align: center;
    color: #2563eb;
    font-size: 42px;
    font-weight: bold;
}
 
.subtitle {
    text-align: center;
    color: #475569;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)
 
# -----------------------------
# LOAD MODEL
# -----------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")
 
# -----------------------------
# PINECONE SETUP
# -----------------------------
from pinecone import Pinecone, ServerlessSpec
 
def init_pinecone():
    pc = Pinecone(api_key="pcsk_5HzujT_PUp7Kypqq7UPwCjENw8wD6cB6hma1iEist3ipuPbyWdVW1aixAkjZvxbNdbHwqF")
 
    index_name = "semantic-search-index"
 
    # Create index if not exists
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"   # change if needed
            )
        )
 
    return pc.Index(index_name)
 
# -----------------------------
# LOAD DOCUMENTS
# -----------------------------
def load_documents_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]
 
    documents = []
 
    for i in range(0, len(lines), 2):
        question = lines[i]
        answer = lines[i + 1] if i + 1 < len(lines) else ""
        documents.append(f"Q: {question}\nA: {answer}")
 
    return documents
 
# -----------------------------
# UPSERT TO PINECONE
# -----------------------------
def upload_to_pinecone(documents, model, index):
    embeddings = model.encode(documents)
 
    vectors = []
    for i, emb in enumerate(embeddings):
        vectors.append(
            (
                str(i),
                emb.tolist(),
                {"text": documents[i]}
            )
        )
 
    index.upsert(vectors)
 
# -----------------------------
# SEARCH
# -----------------------------
def search(query, model, index, top_k=3):
    query_embedding = model.encode([query])[0]
 
    results = index.query(
        vector=query_embedding.tolist(),
        top_k=top_k,
        include_metadata=True
    )
 
    output = []
    for match in results["matches"]:
        output.append(
            {
                "document": match["metadata"]["text"],
                "score": match["score"]
            }
        )
 
    return output
 
# -----------------------------
# MAIN APP
# -----------------------------
def main():
 
    st.markdown(
        '<div class="title-style">🔍 Semantic Search Engine</div>',
        unsafe_allow_html=True
    )
 
    st.markdown(
        '<div class="subtitle">Sentence Transformers + Pinecone + Streamlit</div>',
        unsafe_allow_html=True
    )
 
    st.sidebar.title("⚙️ Settings")
    top_k = st.sidebar.slider("Results", 1, 10, 3)
 
    uploaded_file = st.file_uploader(
        "📄 Upload a TXT file with Q&A pairs",
        type=["txt"]
    )
 
    if uploaded_file is not None:
 
        # Save temp file
        temp_dir = tempfile.gettempdir()
        filepath = Path(temp_dir) / uploaded_file.name
 
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
 
        # Load model
        with st.spinner("Loading model..."):
            model = load_model()
 
        # Load docs
        documents = load_documents_from_file(filepath)
        st.success(f"✅ Loaded {len(documents)} documents")
 
        # Init Pinecone
        with st.spinner("Connecting to Pinecone..."):
            index = init_pinecone()
 
        # Upload
        with st.spinner("Uploading embeddings..."):
            upload_to_pinecone(documents, model, index)
 
        st.success("✅ Data indexed successfully!")
 
        # Query
        query = st.text_input("💬 Enter your query")
 
        if query:
            with st.spinner("Searching..."):
                results = search(query, model, index, top_k)
 
            st.markdown("## 🔎 Results")
 
            for res in results:
                st.markdown(
                    f"""
                    <div class="result-box">
                        <div class="score">
                            Similarity Score: {res['score']:.4f}
                        </div>
                        <br>
                        <div style="white-space: pre-wrap;">
                            {res['document']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
 
    else:
        st.info("📌 Upload a file to begin")
 
# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    main()