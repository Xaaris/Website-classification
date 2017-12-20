import urllib.error
import urllib.request

from bs4 import BeautifulSoup


def download_html_from_url(url):
    try:
        with urllib.request.urlopen(url, timeout=30) as url:
            return url.read()
    except Exception as err:
        print(err)
        return None


def visible_text_from_html(html):
    if html is None:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    return soup.get_text(strip=False).split()
