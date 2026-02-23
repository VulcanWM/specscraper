from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import json

output = {}

print("getting output")

URL = "https://www.aqa.org.uk/subjects/physics/a-level/physics-7408/specification/subject-content"

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
topics = {}

links = soup.find_all("a", class_="font-semibold text-red underline hover:text-red-60")
for link in links:
    topic_name = link.get_text()
    relative_link = link.get("href")
    full_link = urljoin(URL, relative_link)
    topics[topic_name] = full_link
    output[topic_name] = {}

for topic in topics:
    topic_url = topics[topic]
    topic_page = requests.get(topic_url)

    soup = BeautifulSoup(topic_page.content, "html.parser")
    results = soup.find_all("table")
    h3s = soup.find_all("h3", class_="mb-5 text-[color:var(--subject-color-primary)]")
    h4s = soup.find_all("h4", class_="mb-3 text-[color:var(--subject-color-primary)]")
    if len(h3s) == len(results):
        subtopics = []
        for h3 in h3s:
            subtopics.append(h3.get_text())
            output[topic][h3.get_text()] = {}
        subtopicIndex = 0
        for result in results:
            tbody = result.find_all("tbody")[0]
            tds = result.find_all("td")
            count = 0
            for td in tds:
                if count == 0:
                    output[topic][subtopics[subtopicIndex]]['content'] = td.decode_contents()
                elif count == 1:
                    output[topic][subtopics[subtopicIndex]]['opportunity'] = td.decode_contents()
                count += 1
            subtopicIndex += 1
    elif len(h4s) == len(results):
        subsubtopics = {}
        for h3 in h3s:
            output[topic][h3.get_text()] = {}
        for h4 in h4s:
            subsubtopic = h4.get_text()
            for subtopic in output[topic]:
                if subtopic.split()[0] in subsubtopic.split()[0]:
                    output[topic][subtopic][subsubtopic] = {}
                    subsubtopics[subsubtopic] = subtopic

        subsubtopicIndex = 0
        for result in results:
            tbody = result.find_all("tbody")[0]
            tds = result.find_all("td")
            count = 0
            subsubtopic = list(subsubtopics.keys())[subsubtopicIndex]
            subtopic = list(subsubtopics.values())[subsubtopicIndex]
            for td in tds:
                if count == 0:
                    output[topic][subtopic][subsubtopic]['content'] = td.decode_contents()
                elif count == 1:
                    output[topic][subtopic][subsubtopic]['opportunity'] = td.decode_contents()
                count += 1
            subsubtopicIndex += 1

print(json.dumps(output, indent=4))

with open("aqa_physics.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)