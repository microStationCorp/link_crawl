from bs4 import BeautifulSoup
import requests
from urllib.parse import urlsplit


def get_local_urls(url):
    local_urls = set()
    foreign_urls = set()
    files_urls = set()

    try:
        response = requests.get(url, "html.parser")
    except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL,
           requests.exceptions.InvalidSchema):
        return local_urls, foreign_urls, files_urls, True

    parts = urlsplit(url)
    base = "{0.netloc}".format(parts)
    strip_base = base.replace("www.", "")
    base_url = "{0.scheme}://{0.netloc}".format(parts)

    path = url[:url.rfind("/") + 1] if "/" in parts.path else url + "/"

    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a"):
        anchor = link.attrs["href"] if "href" in link.attrs else ""

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
            foreign_urls.add(anchor)

    return local_urls, foreign_urls, files_urls, False


if __name__ == '__main__':
    URL = "https://ssc.nic.in/"
