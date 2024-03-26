import streamlit as st

# Define the path to your image
path = 'C:/Users/Work/OneDrive - University of Bath/ART-AI MRes Modules/CM50304 AI Challenge/AI-Challenge/user_interface/'

# Set the page title and icon
st.set_page_config(
    page_title="Welcome to FeelFlow!",
    page_icon=path + 'FeelFlow.png'
)

# Display the image
st.image(path + "FeelFlow.png")

st.write("# Welcome to FeelFlow, Miles! 👋")

st.write(
    "FeelFlow is an AI-powered emotion tracking and journaling app that you can use to support your mental health."
)

st.write('## Ready to get journaling?')

if st.button("Record my Journal Entry"):
    st.switch_page("pages/1_📓_Lets_Get_Journaling.py")

st.write('## View your old journal content below:')