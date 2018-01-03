import datetime
import threading
import time
import urllib.error
import urllib.request

from bs4 import BeautifulSoup


class DownloaderThread(threading.Thread):
    def __init__(self, threadID, name, url_list):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.url_list = url_list

    def run(self):
        print("Starting " + self.name)
        download_and_store(self.url_list, self.name)


def download_and_store(list_of_urls, thread_name):
    for i, url in enumerate(list_of_urls):
        url = url.strip()
        time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        if url not in already_processed_urls:
            print(thread_name + " " + time_stamp + " Downloading " + str(i) + ": " + url)
            html = download_html_from_url(url)
            visible_text = visible_text_from_html(html)
            threadLock.acquire()
            if len(visible_text) > 0:
                append_line_to_file(path_to_successful_urls, url)
                append_line_to_file(path_to_extracted_texts, " ".join(visible_text))
            else:
                append_line_to_file(path_to_failed_urls, url)
            threadLock.release()
        else:
            print(thread_name + " " + time_stamp + " Skipping " + str(i) + ": " + url)


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


def chunk(url_list, number_of_chunks):
    length_of_list = len(url_list)
    assert 0 < number_of_chunks <= length_of_list
    chunk_size = (length_of_list // number_of_chunks) + 1
    return [url_list[p:p + chunk_size] for p in range(0, length_of_list, chunk_size)]


start = time.time()

path_to_urls = "./data/urls/pos/xing_urls.txt"
path_to_successful_urls = "./data/urls/pos/successful_urls.txt"
path_to_failed_urls = "./data/urls/pos/failed_urls.txt"
path_to_extracted_texts = "./data/positive/visible_text/successful_text_extractions.txt"


print("STARTED")

threadLock = threading.Lock()
already_processed_urls = []
for url in read_lines_from_file(path_to_successful_urls):
    already_processed_urls.append(url.strip())
for url in read_lines_from_file(path_to_failed_urls):
    already_processed_urls.append(url.strip())
new_urls = []
for url in read_lines_from_file(path_to_urls):
    if url.strip() not in already_processed_urls:
        new_urls.append(url.strip())

number_of_threads = 8
chunks = chunk(new_urls, number_of_threads)

threads = []
for i in range(number_of_threads):
    thread = DownloaderThread(i, "thread-" + str(i), chunks[i])
    thread.start()
    threads.append(thread)

for t in threads:
    t.join()

end = time.time()
print("DONE")
print("Time: " + str(end - start))
