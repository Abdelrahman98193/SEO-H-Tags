import requests
import streamlit as st
from bs4 import BeautifulSoup
import csv

def count_headings(url):
    if not url:
        print('URL is empty. Please provide a valid URL.')
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
        print('Failed to fetch the URL. Please check the provided URL.')
        return None, None

def write_to_csv(headings_count, soup):
    with open('headings_analysis.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Heading', 'Type', 'Count'])

        for level, count in headings_count.items():
            if count > 0:
                headings = soup.find_all(level.lower())
                for index, heading in enumerate(headings, start=1):
                    writer.writerow([heading.text.strip(), level, index])

        writer.writerow(['Total Count of Each Heading Type'])
        for level, total_count in headings_count.items():
            writer.writerow([level, total_count])

# Input URL for testing
url = st.text_input('Enter the URL to analyze: ')
headings_count, soup = count_headings(url)

if headings_count and soup:
    write_to_csv(headings_count, soup)
    print('CSV file generated successfully.')
