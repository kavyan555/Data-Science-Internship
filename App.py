import streamlit as st
import pandas as pd

#  TITLE 
st.title("Integrated Streamlit Application")

# SIDEBAR MENU 
st.sidebar.title("Courses Menu")
course = st.sidebar.selectbox(
    "Select Course",
    ["Data Science", "Full Stack Java", "Full Stack Python", "Dot Net"]
)

st.sidebar.success(f"You selected {course}")

#  PROFILE SECTION 
st.header("My Profile")
st.write("Name: Kavyashree N")
st.write("Role: Data Science Intern")
st.write("Skills: Python, SQL, Machine Learning")

# - USER INPUT SECTION 
st.header("User Input Section")

name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=0, max_value=100)

if st.button("Submit"):
    st.success("Button Clicked Successfully!")
    st.write(f"Hello {name}, you are {age} years old.")

# CHECKBOX SHOW/HIDE 

if st.checkbox("Show Secret Message"):
    st.write("Welcome to Streamlit ")

#  SELECTBOX 
st.header("Programming Language Selection")

language = st.selectbox(
    "Choose Programming Language",
    ["Python", "Java", "C++", "JavaScript"]
)

st.write(f"You selected: {language}")

# COUNTER 
st.header("Simple Counter")

if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("Increase Counter"):
    st.session_state.count += 1

st.write("Counter Value:", st.session_state.count)

#  DATAFRAME DISPLAY 
st.header("Display Sample DataFrame")

data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Salary": [50000, 60000, 70000]
}

df = pd.DataFrame(data)
st.dataframe(df)

#  CSV FILE UPLOAD 
st.header("Upload CSV File")

file = st.file_uploader("Upload a CSV file", type=["csv"])

if file is not None:
    uploaded_df = pd.read_csv(file)
    st.write("Uploaded Data:")
    st.dataframe(uploaded_df)

# IMAGE DISPLAY 
st.header("Display Image")

st.image(
    "https://images.unsplash.com/photo-1519389950473-47ba0277781c",
    caption="Sample Image",
    use_container_width=True
)
