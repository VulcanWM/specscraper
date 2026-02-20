from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import json

# should get all the links from the subject content page
# eg. https://www.aqa.org.uk/subjects/physics/a-level/physics-7408/specification/subject-content

output = {}

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

print(topics)

# second subtopic isn't working because it uses h4 because of even more subtopics
# maybe count if the number of h3s is equal to tables
# if yes then only use have subtopics, if not then there are subsubtopics

for topic in topics:
    topic_url = topics[topic]
    topic_page = requests.get(topic_url)
    subtopics = []

    soup = BeautifulSoup(topic_page.content, "html.parser")
    results = soup.find_all("table")
    h3s = soup.find_all("h3", class_="mb-5 text-[color:var(--subject-color-primary)]")
    h4s = soup.find_all("h4", class_="mb-3 text-[color:var(--subject-color-primary)]")
    if len(h3s) == len(results):
        print("subtopics")
    elif len(h4s) == len(results):
        print("subsubtopics")
    for h3 in h3s:
        subtopics.append(h3.get_text())
        output[topic][h3.get_text()] = {}
    print(subtopics)
    print(json.dumps(output, indent=4))

    # subtopicIndex = 0
    # for result in results:
    #     tbody = result.find_all("tbody")[0]
    #     tds = result.find_all("td")
    #     count = 0
    #     for td in tds:
    #         if count == 0:
    #             output[topic][subtopics[subtopicIndex]]['content'] = td.get_text().replace(".", ". ")
    #         elif count == 1:
    #             output[topic][subtopics[subtopicIndex]]['opportunity'] = td.get_text().replace(".", ". ")
    #         count += 1
    #     subtopicIndex += 1


# then should get the name of each link (topic), then get the subtopic using the code below

# URL = "https://www.aqa.org.uk/subjects/physics/a-level/physics-7408/specification/subject-content/measurements-and-their-errors"
# page = requests.get(URL)
#
# output = {}
# subtopics = []
#
# soup = BeautifulSoup(page.content, "html.parser")
# results = soup.find_all("table")
# h3s = soup.find_all("h3", class_="mb-5 text-[color:var(--subject-color-primary)]")
# for h3 in h3s:
#     subtopics.append(h3.get_text())
#     output[h3.get_text()] = {}
#
# subtopicIndex = 0
# for result in results:
#     tbody = result.find_all("tbody")[0]
#     tds = result.find_all("td")
#     count = 0
#     for td in tds:
#         if count == 0:
#             output[subtopics[subtopicIndex]]['content'] = td.get_text().replace(".", ". ")
#         elif count == 1:
#             output[subtopics[subtopicIndex]]['opportunity'] = td.get_text().replace(".", ". ")
#         count += 1
#     subtopicIndex += 1
#
print(json.dumps(output, indent=4))