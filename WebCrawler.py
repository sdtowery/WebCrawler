
from urllib.request import urlopen
import bs4

html = urlopen('https://auburn.edu').read()
soup = bs4.BeautifulSoup(html, features="html.parser")
for script in soup(["script", "style"]):
    script.extract()

print(soup.prettify())
