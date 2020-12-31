from collections import deque
import json
import get_url

URL = "http://rjshayari.com/"

MAIN_DATA = []

new_urls = deque([URL])
processed_urls = set()

while len(new_urls):
    url = new_urls.popleft()
    processed_urls.add(url)

    local, foreign, files, broken = get_url.get_local_urls(url)

    print("processing : ", url)

    if not broken:
        for i in local:
            if i not in new_urls and i not in processed_urls:
                new_urls.append(i)
        MAIN_DATA.append({
            "processed_url": url,
            "local_urls": list(local),
            "foreign_urls": list(foreign),
            "file_urls": list(files),
        })
    else:
        MAIN_DATA.append({
            "processed_url": url,
            "broken": broken
        })

with open("links.json", "w") as file:
    json.dump(MAIN_DATA, file, indent=4)
