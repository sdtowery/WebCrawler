import validators
from bs4 import BeautifulSoup
from urllib.request import urlopen

from validators.url import url


def ids():
    pass


def webcrawl(url):
    # Documentation for BeautifulSoup found here:
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    if not validators.url(url):
        return

    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    print(soup.original_encoding)

    # Reference for removing JavaScript code:
    # https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
    for script in soup(["script", "style"]):
        script.extract()

    content = soup.prettify()
    write_file(content, url)

    url_list = []
    for link in soup.find_all('a'):
        url_list.append((link.get('href')))

    return url_list


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

url_list = webcrawl(user_url)
print(url_list)
# unigram_extractor(url_list)
