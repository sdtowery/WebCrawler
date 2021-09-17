import re
from urllib.error import URLError
import validators
from bs4 import BeautifulSoup
from urllib.request import HTTPError
from urllib.request import urlopen
from validators.url import url


def dls(url, depth):
    global visited
    if depth >= 0:
        content = ""
        print(f"current url: {url}")
        if depth > 0:
            # When depth > 0, grab content and links
            # If data = None, skip to next child
            data = webcrawl(url)
            if data == None: return
            content, links = data
            for link in links:
                if not link in visited:
                    visited.append(link)
                    dls(link, depth - 1)
        else:
            # When depth = 0, grab content
            # If data = None, skip to next child
            data = webcrawl(url)
            if data == None: return
            content = data[0]
        write_file(content, url)


def ids(url, max_depth):
    global visited
    for i in range(max_depth + 1):
        visited = []
        visited.append(url)
        print("-------------------------")
        print("Depth: ", i)
        dls(url, i)
        print("-------------------------")

def webcrawl(url):
    # Documentation for BeautifulSoup found here:
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    if not validators.url(url):
        return

    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")
    except HTTPError as err:
        print(f"HTTP Error {err.code}: {err.reason} - \'{url}\' ... skipping ...")
        return None
    except URLError as err:
        print(f"URL Error: {err.reason} - \'{url}\' ... skipping ...")
        return None

    # Reference for removing JavaScript code:
    # https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
    for script in soup(["script", "style"]):
        script.extract()

    content = soup.prettify()
    write_file(content, url)

    url_list = []
    for link in soup.findAll('a', attrs={'href': re.compile("^https?://")}):
        url = link.get('href')
        if url == None: continue
        # Strip '/' from the end of the url to avoid duplicates
        url_list.append(url.rstrip('/'))

    return content, url_list


def write_file(content, url):
    pass


def unigram_extractor(links):
    print(*links, sep="\n")


# Main
# User inputs URL and depth
while True:
    user_url = input("Enter a valid URL: ")
    if not validators.url(user_url):
        print("URL not valid")
    else:
        break

depth = int((input("Enter a maximum depth: ")))

visited = []
ids(user_url, depth)
# unigram_extractor(url_list)