import streamlit as st
import pickle
import pandas as pd

# ==============================
# Load Data
# ==============================
books_dict = pickle.load(open('books.pkl', 'rb'))
similarity = pickle.load(open('similarity_books.pkl', 'rb'))

books = pd.DataFrame(books_dict)

# ==============================
# Recommendation Function
# ==============================
def recommend(book):
    if book not in books['title'].values:
        return [], []

    book_index = books[books['title'] == book].index[0]
    distances = similarity[book_index]

    books_list = sorted(
        enumerate(distances),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    names = []
    posters = []

    for i in books_list:
        names.append(books.iloc[i[0]]['title'])
        posters.append(books.iloc[i[0]]['thumbnail'])

    return names, posters


# ==============================
# UI
# ==============================
st.set_page_config(page_title="Book Recommender", layout="wide")

st.title("📚 Book Recommendation System")

selected_book = st.selectbox(
    "Choose a book",
    books['title'].values
)

# ==============================
# Button Action
# ==============================
if st.button("Recommend"):
    names, posters = recommend(selected_book)

    if names:
        cols = st.columns(5)

        for i in range(len(names)):
            with cols[i]:
                st.image(posters[i])
                st.caption(names[i])
    else:
        st.warning("Book not found!")