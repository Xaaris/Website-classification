from gensim import utils


def write_urls_to_disc(filename, urls):
    with open(filename, 'w') as urls_file:
        for url in urls:
            urls_file.write(url + "\n")


def read_lines_from_file(filename):
    with utils.smart_open(filename) as file:
        return file.readlines()


lines_with_urls = set()
path = "/Users/hannes/Downloads/content.rdf.u8"
for line in read_lines_from_file(path):
    line_as_string = str(line)
    if "<link r:resource=" in line_as_string and ".de/" in line_as_string and ".pdf" not in line_as_string:
        line_as_string = line_as_string.replace("b'    <link r:resource=\"", "").replace("\"></link>\\n'", "")
        lines_with_urls.add(line_as_string)

write_urls_to_disc("dmoz_urls_de.txt", lines_with_urls)
