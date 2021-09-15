import validators
from bs4 import BeautifulSoup
from urllib.request import urlopen


def iterative_deepening_search(url, depth):
    # Documentation for BeautifulSoup found here:
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    html = urlopen(user_url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # Reference for removing JavaScript code:
    # https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
    for script in soup(["script", "style"]):
        script.extract()

    # print(soup.prettify())

    url_list = list()
    for link in soup.find_all('a'):
        url_list.append((link.get('href')))

    return url_list


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

url_list = iterative_deepening_search(user_url, depth)
unigram_extractor(url_list)
