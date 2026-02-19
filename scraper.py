from bs4 import BeautifulSoup
import requests
import json

# should get all the links from the subject content page
# eg. https://www.aqa.org.uk/subjects/physics/a-level/physics-7408/specification/subject-content

# then should get the name of each link (topic), then get the subtopic using the code below

URL = "https://www.aqa.org.uk/subjects/physics/a-level/physics-7408/specification/subject-content/measurements-and-their-errors"
page = requests.get(URL)

output = {}
subtopics = []

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("table")
h3s = soup.find_all("h3", class_="mb-5 text-[color:var(--subject-color-primary)]")
for h3 in h3s:
    subtopics.append(h3.get_text())
    output[h3.get_text()] = {}

subtopicIndex = 0
for result in results:
    tbody = result.find_all("tbody")[0]
    tds = result.find_all("td")
    count = 0
    for td in tds:
        if count == 0:
            output[subtopics[subtopicIndex]]['content'] = td.get_text().replace(".", ". ")
        elif count == 1:
            output[subtopics[subtopicIndex]]['opportunity'] = td.get_text().replace(".", ". ")
        count += 1
    subtopicIndex += 1

print(json.dumps(output, indent=4))