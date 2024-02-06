import requests
import streamlit as st
from bs4 import BeautifulSoup

def count_headings(url):
    if not url:
        st.error('URL is empty. Please provide a valid URL.')
        return None

    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url  # Adding a default schema if missing

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            headings_count = {}
            for heading_level in range(1, 7):
                headings = soup.find_all(f'h{heading_level}')
                headings_count[f'H{heading_level}'] = len(headings)

            return headings_count
        else:
            st.error('Failed to fetch the URL. Please check the provided URL.')
            return None
    except requests.exceptions.RequestException as e:
        st.error(f'An error occurred: {e}')
        return None

# Input URL for testing
url = st.text_input('Enter the URL to analyze: ')
headings_count = count_headings(url)

if headings_count:
    st.write(headings_count)
