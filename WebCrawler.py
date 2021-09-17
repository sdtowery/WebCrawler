import re
from urllib.error import URLError
import validators
import os
import json
from typing import Counter
from bs4 import BeautifulSoup
from urllib.request import HTTPError
from urllib.request import urlopen


def dls(url, depth):
    global visited
    if depth >= 0:
        content = ""
        print(f"current url: {url}")
        if depth > 0:
            # When depth > 0, grab content and links
            # If data = None, skip to next child
            data = webcrawl(url)
            if data == None:
                return
            content, links = data
            for link in links:
                if not link in visited:
                    visited.append(link)
                    dls(link, depth - 1)
        else:
            # When depth = 0, grab content
            # If data = None, skip to next child
            data = webcrawl(url)
            if data == None:
                return
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
        print(
            f"HTTP Error {err.code}: {err.reason} - \'{url}\' ... skipping ...")
        return None
    except URLError as err:
        print(f"URL Error: {err.reason} - \'{url}\' ... skipping ...")
        return None

    # Reference for removing JavaScript code:
    # https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
    for script in soup(["script", "style"]):
        script.extract()

    content = soup.prettify()

    url_list = []
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        url = link.get('href')
        if url == None:
            continue
        # Strip '/' from the end of the url to avoid duplicates
        url_list.append(url.rstrip('/'))

    return content, url_list


def write_file(content, url):
    global html_file_directory
    global file_list
    # https://stackoverflow.com/questions/27647155/most-efficient-way-to-strip-forbidden-characters-in-file-name-from-unicode-strin
    url = re.sub(r'[\\/*?:"<>|.]', "", url)
    file_name = url + ".txt"

    try:
        # Create directory for html files if it doesn't exist
        if not os.path.exists(html_file_directory):
            os.makedirs(html_file_directory)
        f = open(html_file_directory + file_name, "x")
        f.write(content)
        f.close()
        file_list.append(file_name)
    except FileExistsError as err:
        print(f"File exists: {file_name}")
    except OSError:
        print('Error: Creating directory. ' + html_file_directory)
    except Exception as err:
        print(f"Error: {err}")


def unigram_extractor(files):
    # https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
    global unigram_file_directory
    
    for file_name in files:
        f = open(html_file_directory + file_name, 'r')
        contents = f.read()
        lines = (line.strip() for line in contents.splitlines())
        chunks = (phrase.strip()
                  for line in lines for phrase in line.split(" "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        row = list(text)
        unigram = json.dumps(Counter(row))
        try:
            # Create directory for unigram files if it doesn't exist
            if not os.path.exists(unigram_file_directory):
                os.makedirs(unigram_file_directory)
            unigram_file = open(unigram_file_directory + file_name, 'x')
            unigram_file.write(unigram)
            unigram_file.close()
        except FileExistsError as err:
            print(f"File exists: {file_name}")
        except OSError:
            print('Error: Creating directory. ' + unigram_file_directory)
        except Exception as err:
            print(f"Error: {err}")

def total_unigram_extractor():
    global unigram_file_directory
    total_filename = "total_unigram" + ".txt"

    total_unigram = {}
    for file in os.listdir(unigram_file_directory):
        with open(os.path.join(unigram_file_directory, file), 'r') as f:
            unigram = json.loads(f.read())
            for item in unigram:
                if not item in total_unigram:
                    total_unigram[item] = unigram[item]
                else:
                    total_unigram[item] += unigram[item]
    try:
        f = open(unigram_file_directory + total_filename, "x")
        f.write(json.dumps(total_unigram))
        f.close()
    except Exception as err:
        print(f"Error: {err}")
# Main
# User inputs URL and depth
html_file_directory = "./html_files/"
unigram_file_directory = "./unigram_files/"
while True:
    user_url = input("Enter a valid URL: ")
    if not validators.url(user_url):
        print("URL not valid")
    else:
        break

depth = int((input("Enter a maximum depth: ")))

file_list = []
visited = []
ids(user_url, depth)
unigram_extractor(file_list)
total_unigram_extractor()