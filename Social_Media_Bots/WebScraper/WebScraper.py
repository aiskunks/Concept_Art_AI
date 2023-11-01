import csv
import requests
from bs4 import BeautifulSoup
import os
import re

def scrape_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        page_content = response.text
        soup = BeautifulSoup(page_content, 'html.parser')
        body_content = soup.find('body').get_text()
        return body_content
    else:
        return None

def remove_special_characters(text):
    # Define a regex pattern that matches any character that is not a letter, number, or space
    pattern = r'[^a-zA-Z0-9\s]'
    clean_text = re.sub(pattern, ' ', text)
    return clean_text

def remove_large_spaces(text):
    # Define a regex pattern that matches multiple consecutive spaces and replaces them with a single space
    pattern = r'\s+'
    clean_text = re.sub(pattern, ' ', text)
    return clean_text

def format_text(text):
    # Split the text into paragraphs using double line breaks
    paragraphs = text.split('\n\n')

    # Remove extra spaces from each paragraph
    formatted_paragraphs = [remove_large_spaces(paragraph) for paragraph in paragraphs]

    # Rejoin the formatted paragraphs with double line breaks
    formatted_text = '\n\n'.join(formatted_paragraphs)

    return formatted_text

# Read the CSV file with names and links
csv_file = 'links.csv'
output_directory = 'scraped_content'

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

with open(csv_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        name = row['name']
        url = row['link']
        scraped_content = scrape_page(url)

        if scraped_content:
            # Remove special characters and save to a text file
            cleaned_content = remove_special_characters(scraped_content)
            # cleaned_content = remove_large_spaces(cleaned_content)
            formatted_content = format_text(cleaned_content)
            output_file = os.path.join(output_directory, f"{name}.txt")

            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(formatted_content)
                print(f"{name}.txt saved successfully!")
        else:
            print(f"Failed to scrape data from URL: {url}")

print("Scraping and saving to text files completed.")
