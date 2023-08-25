import requests
from bs4 import BeautifulSoup
import csv

def get_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return ""

def extract_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extracting task_ID
    question_title_div = soup.find('div', class_='question-title clearfix')
    if question_title_div:
        task_ID = question_title_div.h3.text.split('.')[1].strip()
    else:
        task_ID = ""
    
    # Extracting question content
    question_content_div = soup.find('div', class_='question-content default-content')
    if question_content_div:
        question_content = question_content_div.get_text(strip=True)
    else:
        question_content = ""
    
    # Extracting acceptance rate
    contest_info_div = soup.find('div', class_='contest-question-info pull-right')
    if contest_info_div:
        total_accepted = int(contest_info_div.find('strong', text='Total Accepted:').find_next_sibling().text.strip())
        total_submissions = int(contest_info_div.find('strong', text='Total Submissions:').find_next_sibling().text.strip())
        acceptance_rate = total_accepted / total_submissions
    else:
        acceptance_rate = 0
    
    return task_ID, question_content, acceptance_rate

def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Task_ID', 'Question_Content', 'Acceptance_Rate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerow({
            'Task_ID': data[0],
            'Question_Content': data[1],
            'Acceptance_Rate': data[2]
        })

# Sample usage:
url = "https://leetcode.com/contest/weekly-contest-314/problems/find-the-original-array-of-prefix-xor/"
html_content = get_html_content(url)
if html_content:
    data = extract_data(html_content)
    write_to_csv(data, 'output.csv')
