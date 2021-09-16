import validators
from bs4 import BeautifulSoup
from urllib.request import urlopen

from validators.url import url


def ids(url, max_depth):
    visited = []
    url_list = []
    url_list.append(url)
    # Run until url_list is empty
    while url_list:
        if not url in visited:
            visited.append(url)
            # Get children urls
            temp_list = webcrawl(url)
            # Pop current url from stack
            url_list.pop()
            # Add temp_list to url_list if not None
            if temp_list != None:
                url_list += temp_list
            # Set url to top of stack
            url = url_list[-1]
        else:
            # Pop current url from stack and set url to top of stack 
            url_list.pop()
            url = url_list[-1]
            

def webcrawl(url):
    # Documentation for BeautifulSoup found here:
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    if not validators.url(url):
        return

    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # Reference for removing JavaScript code:
    # https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
    for script in soup(["script", "style"]):
        script.extract()

    content = soup.prettify()
    write_file(content, url)

    url_list = []
    for link in soup.find_all('a'):
        url = link.get('href')
        if url == None: continue
        # Strip '/' from the end of the url to avoid duplicates
        url_list.append(url.rstrip('/'))

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

url_list = ids(user_url, depth)
# unigram_extractor(url_list)