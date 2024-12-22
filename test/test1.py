import streamlit as st

# Define the sections and their contents
def section_a():
    st.header("A Portion")
    st.write("This is the content for section A.")

def section_b():
    st.header("B Portion")
    st.write("This is the content for section B.")

def section_c():
    st.header("C Portion")
    st.write("This is the content for section C.")

# Create a container for the buttons at the top of the page
st.markdown("""
    <style>
    .stButton>button {
        width: 100px;
        margin: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Place the buttons at the top using the columns layout
col1, col2, col3 = st.columns(3)
with col1:
    button_a = st.button("Test A")
with col2:
    button_b = st.button("Test B")
with col3:
    button_c = st.button("Test C")

# Create the sections that will be displayed when a button is clicked
if button_a:
    section_a()
elif button_b:
    section_b()
elif button_c:
    section_c()

# Default behavior when no button is clicked
else:
    st.write("Please select a section to view.")
