import requests
import streamlit as st
from bs4 import BeautifulSoup
import csv
import io

def count_headings(url):
    if not url:
        st.write('URL is empty. Please provide a valid URL.')
        return None, None

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        headings_count = {}
        for heading_level in range(1, 7):
            headings = soup.find_all(f'h{heading_level}')
            headings_count[f'H{heading_level}'] = len(headings)

        return headings_count, soup
    else:
        st.write('Failed to fetch the URL. Please check the provided URL.')
        return None, None

def write_to_csv(headings_count, soup):
    rows_data = []
    for level, count in headings_count.items():
        if count > 0:
            headings = soup.find_all(level.lower())
            for index, heading in enumerate(headings, start=1):
                rows_data.append([heading.text.strip(), level, index])

    csv_data = io.StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(['Heading', 'Type', 'Index'])
    for row_data in rows_data:
        writer.writerow(row_data)

    st.download_button(
        label="Download headings_analysis.csv",
        data=csv_data.getvalue(),
        file_name='headings_analysis.csv',
        mime='text/csv',
    )

# Input URL for testing
url = st.text_input('Enter the URL to analyze: ')
button_clicked = st.button('Generate Results and CSV File')

if button_clicked:
    headings_count, soup = count_headings(url)
    
    if headings_count and soup:
        st.write('### Results:')
        
        rows_data = []  # Initialize rows_data here
        
        for level, count in headings_count.items():
            if count > 0:
                headings = soup.find_all(level.lower())
                for index, heading in enumerate(headings, start=1):
                    rows_data.append([heading.text.strip(), level, index])
        
        st.table(rows_data, headers=["Heading", "Type", "Index"])

        write_to_csv(headings_count, soup)
        st.write('CSV file generated successfully.')
