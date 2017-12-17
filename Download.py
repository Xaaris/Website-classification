import urllib.request
import urllib.error
from bs4 import BeautifulSoup


def download_html_from_url(url):
        try:
            with urllib.request.urlopen(url) as url:
                return url.read()
        except urllib.error.HTTPError as err:
            print(err)


def visible_text_from_html(html):
    if html is None:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    return soup.get_text(strip=False).split()
