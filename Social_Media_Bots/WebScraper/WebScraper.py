import csv
import requests
from bs4 import BeautifulSoup
import os
import re
from zipfile import ZipFile

def scrape_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        page_content = response.text
        soup = BeautifulSoup(page_content, 'html.parser')
        body_content = soup.find(id="main")
        if not body_content:
            body_content = soup.find("body")
        # Return the scraped content between the navbar and footer.
        return body_content.get_text() if body_content else None
    else:
        return None

def remove_special_characters(text):
    # Define a regex pattern that matches any character that is not a letter, number, or space
    pattern = r'[^a-zA-Z0-9\s]'
    clean_text = re.sub(pattern, ' ', text)
    return clean_text

def remove_large_spaces(text):
    # Define a regex pattern that matches multiple consecutive spaces and replaces them with a single space
    # clean_text = re.sub(r'\n+', '\n', text)
    cleaned_text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
    return cleaned_text

def zip_texts(texts_directory, name):
  # Create a zip file with the specified name and add all the text files from the directory
  with ZipFile(f"{name}.zip", 'w') as zip_file:
    for root, _, files in os.walk(texts_directory):
      for file in files:
        full_path = os.path.join(root, file)
        zip_file.write(full_path, os.path.relpath(full_path, os.path.join(texts_directory, '')))

# Read the CSV file with names and links
csv_file = 'E:\Concept_Art_AI\Social_Media_Bots\WebScraper\csv_files\links.csv'
output_directory = 'scraped_content\ogs'

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

visitedLinks = set()

with open(csv_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        name = row['name']
        url = row['link']
        if url not in visitedLinks:
            visitedLinks.add(url)

            scraped_content = scrape_page(url)

            if scraped_content:
                # Remove special characters and save to a text file
                cleaned_content = remove_special_characters(scraped_content)
                cleaned_content = remove_large_spaces(cleaned_content)
                output_file = os.path.join(output_directory, f"{name}.txt")

                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(cleaned_content)
                    print(f"{name}.txt saved successfully!")
            else:
                print(f"Failed to scrape data from URL: {url}")
        else:
            continue

zip_texts(output_directory, "OGS")
print("Scraping and saving to text files completed. Zipped files successfully!")


def merge_files(folder_path, output_file):
  """
  Merges the content of all files in a folder into a single text file.

  Args:
    folder_path: The path to the folder containing the files to merge.
    output_file: The path to the output file where the merged content will be written.
  """
  with open(output_file, "w") as outfile:
    for filename in os.listdir(folder_path):
      filepath = os.path.join(folder_path, filename)
      if os.path.isfile(filepath):
        with open(filepath, "r") as infile:
          content = infile.read()
          outfile.write(content)
          outfile.write("\n") # Add a newline between files


folder_path = "scraped_content\ogs"
output_file = "scraped_content\ogs\ogs.txt"
merge_files(folder_path, output_file)
print(f"Successfully merged files into {output_file}")
