import datetime
import time
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
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out
        return soup.get_text(strip=False).split()
    except Exception as err:
        print(err)
        return []


def append_line_to_file(filename, line):
    with open(filename, 'a') as file:
        file.write(line + "\n")


def read_lines_from_file(filename):
    with open(filename) as file:
        return file.readlines()


already_processed_urls = []
for url in read_lines_from_file("data/successful_urls.txt"):
    already_processed_urls.append(url.strip())
for url in read_lines_from_file("data/failed_urls.txt"):
    already_processed_urls.append(url.strip())

start = time.time()

for i, url in enumerate(read_lines_from_file("./dmoz_urls_de.txt")):
    url = url.strip()
    time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    if url not in already_processed_urls:
        print(time_stamp + " Downloading " + str(i) + ": " + url)
        html = download_html_from_url(url)
        visible_text = visible_text_from_html(html)
        if len(visible_text) > 0:
            append_line_to_file("data/successful_urls.txt", url)
            append_line_to_file("data/successful_text_extractions.txt", " ".join(visible_text))
        else:
            append_line_to_file("data/failed_urls.txt", url)
    else:
        print(time_stamp + " Skipping " + str(i) + ": " + url)

end = time.time()
print(end - start)
