from bs4 import BeautifulSoup
import requests
from urllib.parse import urlsplit


def get_local_urls(url):
    # declare all variables as set
    local_urls = set()
    foreign_urls = set()
    files_urls = set()

    # to see if the link is broken or not
    try:
        response = requests.get(url, "html.parser")
    except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL,
           requests.exceptions.InvalidSchema):
        # if link is broken then return Broken tag True
        return local_urls, foreign_urls, files_urls, True

    # split url in parts
    parts = urlsplit(url)
    # create base url
    base = "{0.netloc}".format(parts)
    strip_base = base.replace("www.", "")
    # create base url
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    # create path
    path = url[:url.rfind("/") + 1] if "/" in parts.path else url + "/"

    # get full website
    soup = BeautifulSoup(response.text, "html.parser")

    # loop through all anchors
    for link in soup.find_all("a"):
        anchor = link.attrs["href"] if "href" in link.attrs else ""

        # if the anchor is file or not in this I only consider .pdf and .jpg .
        # In your logic you may have many more files you can add those as per logic
        if (anchor.endswith(".pdf") or anchor.endswith(".PDF") or anchor.endswith(".jpg")) and anchor.startswith("/"):
            files_urls.add(base_url + anchor)
        elif anchor.endswith(".pdf") or anchor.endswith(".PDF") or anchor.endswith(".jpg"):
            files_urls.add(anchor)
        elif anchor.startswith("/"):
            local_urls.add(base_url + anchor)
        elif strip_base in anchor:
            local_urls.add(anchor)
        elif not anchor.startswith("http"):
            local_urls.add(path + anchor)
        else:
            # get all foreign urls
            foreign_urls.add(anchor)

    # return all local foreign file urls and broken tag
    return local_urls, foreign_urls, files_urls, False


if __name__ == '__main__':
    URL = "https://ssc.nic.in/"
