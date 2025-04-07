import requests
from bs4 import BeautifulSoup
import csv
import os

url = "https://www.angelone.in/support"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

topics = []
#get all topics 
for content in soup.select("div.content"):
    title_tag = content.find("h2")
    link_tag = content.find("a", class_="learn-more")
    
    if title_tag and link_tag:
        title = title_tag.get_text(strip=True)
        link = link_tag['href']
        topics.append({
            "title": title,
            "url": link
        })
#make new folder to store all csv files
os.makedirs("angelone_faqs", exist_ok=True)

for topic in topics:
    print(f"Scraping: {topic['title']}")
    res = requests.get(topic['url'])
    soup = BeautifulSoup(res.text, "html.parser")

   
    faqs = []
    for tab in soup.select("div.tab"):
        q = tab.select_one("label.tab-label")
        a = tab.select_one("div.tab-content")
        if q and a:
            question = q.get_text(strip=True)
            answer = a.get_text(strip=True)
            faqs.append([question, answer])

   
    if faqs:
        filename = f"angelone_faqs/{topic['title'].replace(' ', '_')}.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Question", "Answer"])
            writer.writerows(faqs)
        print(f"Saved {len(faqs)} FAQs to {filename}")
    else:
        print(f"No FAQs found for: {topic['title']}")
