
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Constants
EXCEL_FILE = "raagam_entries.xlsx"
DOT_ABOVE = '\u0307'
DOT_BELOW = '\u0323'
SUBSCRIPT_MAP = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

# Format musical notes
def format_notes(note_line):
    tokens = note_line.strip().split()
    formatted = []
    for token in tokens:
        token = token.upper()
        dot_below = token.startswith('.')
        dot_above = token.endswith('.')
        token = token.strip('.')
        letter = ''.join(filter(str.isalpha, token))
        number = ''.join(filter(str.isdigit, token))
        formatted_token = letter
        if dot_below:
            formatted_token += DOT_BELOW
        if dot_above:
            formatted_token += DOT_ABOVE
        if number:
            formatted_token += number.translate(SUBSCRIPT_MAP)
        formatted.append(formatted_token)
    return ' '.join(formatted)

# App layout
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(to bottom, #ffffff, #e6f0ff);
        padding: 2rem;
        border-radius: 10px;
    }
    label {
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: #003366;'>ॐ SwaraNighantuvu ॐ</h1>", unsafe_allow_html=True)

with st.container():
    raagam = st.text_input("Raagam")
    arohana = st.text_input("Arohana")
    avarohana = st.text_input("Avarohana")
    composer = st.text_input("Composer")
    student = st.text_input("Student Name")
    details = st.text_area("Raagam Details", height=100)

    if st.button("Convert and Save"):
        formatted_arohana = format_notes(arohana)
        formatted_avarohana = format_notes(avarohana)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        output = f"Raagam: {raagam}\nArohana: {formatted_arohana}\nAvarohana: {formatted_avarohana}\nComposer: {composer}\nRaagam Details: {details}\nStudent Name: {student}"
        st.text_area("Formatted Output", value=output, height=150)

        new_entry = pd.DataFrame([[raagam, formatted_arohana, formatted_avarohana, composer, details, student, timestamp]],
                                 columns=["Raagam", "Arohana", "Avarohana", "Composer", "Raagam Details", "Student Name", "Timestamp"])

        if os.path.exists(EXCEL_FILE):
            existing = pd.read_excel(EXCEL_FILE, engine='openpyxl')
            updated = pd.concat([existing, new_entry], ignore_index=True)
        else:
            updated = new_entry

        updated.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
        st.success("Entry saved to Excel file.")

    if st.button("View All Entries"):
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
            st.dataframe(df)
        else:
            st.info("No entries found.")
