import streamlit as st
import pandas as pd
import base64

# Sample headings data - you can modify this based on your requirements
sample_headings_data = {
    'Heading': ['Heading 1', 'Heading 2', 'Heading 3'],
    'Type': ['Type A', 'Type B', 'Type C'],
    'Index': [1, 2, 3]
}

# Function to write heading data to a CSV file
def write_to_csv(data):
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64
