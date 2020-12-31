from collections import deque
import json
import get_url

# main website url
URL = "http://rjshayari.com/"

# variable which holds all the data
MAIN_DATA = []

# new urls which have to be fetch
new_urls = deque([URL])
# list of urls which are fetched
processed_urls = set()

# loop through all the new urls
while len(new_urls):
    # take one url from from "new_urls" set
    url = new_urls.popleft()
    # add to "processed_urls"
    processed_urls.add(url)

    # run get_url function and get local, foreign , files url and get broken tag to know if the link is broken
    local, foreign, files, broken = get_url.get_local_urls(url)

    # print processing url
    print("processing : ", url)

    # if the link is not broken
    if not broken:
        for i in local:
            # if the local urls are already not fetched , then add to "new_urls"
            if i not in new_urls and i not in processed_urls:
                new_urls.append(i)
        # append MAIN_DATA variable
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

    # after all run make a json file
    with open("links.json", "w") as file:
        json.dump(MAIN_DATA, file, indent=4)
