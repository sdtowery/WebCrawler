import requests

r = requests.get("https://auburn.edu")
print(r.text)