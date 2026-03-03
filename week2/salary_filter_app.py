import streamlit as st
import pandas as pd

st.title("Employee Salary Filter App")

#  ROLE SELECTION 
st.sidebar.title("User Role")
role = st.sidebar.selectbox(
    "Select Your Role",
    ["HR", "Manager", "Employee"]
)

# Display content based on role
if role == "HR":
    st.sidebar.success("Welcome HR ")
elif role == "Manager":
    st.sidebar.info("Manager Dashboard ")
elif role == "Employee":
    st.sidebar.warning("Employee View ")

st.write(f"### Logged in as: {role}")

#  FILE UPLOAD 
file = st.file_uploader("Upload Employee CSV File", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    st.subheader("Original Data")
    st.dataframe(df)

    #  SALARY FILTER 
    if "Salary" in df.columns:
        filtered_df = df[df["Salary"] > 50000]

        st.subheader("Employees with Salary > 50,000")
        st.dataframe(filtered_df)

        st.success(f"{len(filtered_df)} employees found with salary > 50,000")
    else:
        st.error("Salary column not found in CSV file.")
