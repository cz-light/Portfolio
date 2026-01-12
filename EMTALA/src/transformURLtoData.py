"""
This script extracts paragraphs from enforcement action pages on the HHS OIG website
and uses OpenAI to parse and extract relevant metadata from each paragraph. The extracted data
is saved in a JSON file for further processing.
"""

import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os
import json

ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

case_paragraphs = []
parsed_urls = set()
case_data = []

url = "https://oig.hhs.gov/fraud/enforcement/?type=emtalapatient-dumping&page="

def find_metadata(paragraph, id):
    """
    uses openai to extract the metadata from an input paragraph and return the paragraph and metadata in a unique JSON object
    """
    prompt = f"""Parse the following paragraph and extract the monetary penalty, date, hospital name, hospital name abbreviation, and state. 
                Output your text extraction in a JSON format with the provided unique ID, example: {{"id": <unique_id>, "paragraph": <paragraph>, "metadata": {{"penalty": [<money>], "date": [<date>], "hospital_name": [<hospital name>], "hospital_abbreviation": [<abbreviation>], "state": [<state>]}}}}\n 
                If one of the metadata elements does not exist in the paragraph, simply write "None" in the list. 
                For example, if the monetary penalty does not exist, then output: {{"id": <unique_id>, "paragraph": <paragraph>, "metadata": {{"penalty": [None], "date": [<date>], "hospital_name": [<hospital name>], "hospital_abbreviation": [<abbreviation>], "state": [<state>]}}}} 
                If there are multiple possibilities in the paragraph for a single element, then make the element a nested list with all possibilities. 
                For example, if there are two monetary penalties mentioned, output: {{"id": <unique_id>, "paragraph": <paragraph>, "metadata": {{"penalty": [<money1>, <money2>], "date": [<date>], "hospital_name": [<hospital name>], "hospital_abbreviation": [<abbreviation>], "state": [<state>]}}}}\n 
                Do not output anything other than the JSON of extracted data. 
                Here is the unique id: {id}\n
                Here is the paragraph:\n {paragraph}"""
    
    response = ai_client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.choices[0].message.content
    try:
        text_as_json = json.loads(text)
    except:
        #error message for debugging and I can go back and manually extract the error data
        print(f"Error parsing JSON for paragraph ID {id}. Returning None values.")
        text_as_json = {"id": id, "paragraph": paragraph, "metadata": {"penalty": [None], "date": [None], "hospital_name": [None], "hospital_abbreviation": [None], "state": [None]}}
    return text_as_json

def extractTextFromURL(url):
    #first for loop finds all URLs displayed on each page, each page is represented by the iterater "i"
        #next steps: need to add logic to find how many pages there are dynamically and to go into the archives
    for i in range(6):
        response = requests.get(f"{url}{i+1}")
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text()
        links = soup.find_all("a", href=True)
        page_urls = []

        #for loop checks each link to see if it is a link to an enforcement action page, which contains the paragraphs we want to extract
        for link in links:
            if link['href'].startswith("/fraud/enforcement/"):
                
                full_url = f"https://oig.hhs.gov{link['href']}"
                #avoid duplicates
                if full_url in parsed_urls:
                    continue
                else:
                    page_urls.append(full_url)
                    parsed_urls.add(full_url)

        #for loop goes into each enforcement action link and extracts all the paragraphs
        for j in range(len(page_urls)):
            #print(f"----PROCESSING URL {j+1}/{len(page_urls)}----") ##uncomment for debugging
            response = requests.get(page_urls[j])
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            paragraphs = soup.find_all("p")

            #for loop goes through each paragraph and filters out unwanted text, then appends the cleaned paragraphs to all_paragraphs
            for paragraph in paragraphs:
                text = paragraph.get_text().strip()
                if not text or text.startswith("HHS") or text.startswith("An official")  or text.startswith("Read more") or text.startswith("Visit") or text.startswith("This table") or text.startswith("Recipients") or text.startswith("Providers") or text.startswith("OIG") or text.startswith("The MFCUs") or text.startswith("Actions related") or text.startswith("Details about") or text.startswith("Criminal, civil") or text.startswith("Secure .gov") or text.startswith("Official websites") or text.startswith("Here’s how") or text in case_paragraphs:
                    continue
                case_paragraphs.append(text)

    return case_paragraphs

def main():
    print("**Starting paragraph extraction from URLs**")
    extracted_paragraphs = extractTextFromURL(url)

    print("**Starting metadata extraction from paragraphs**")
    for i in range(len(extracted_paragraphs)):
        jsonObject = find_metadata(extracted_paragraphs[i], 10000+1+i)
        case_data.append(jsonObject)

    print("**Saving data to JSON file**")
    with open("data/emtala_case_data.json", "w") as f:
        json.dump(case_data, f, indent=4)
    print("**Data extraction complete. JSON file created.**")

