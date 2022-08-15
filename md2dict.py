import mistletoe
from bs4 import BeautifulSoup
from xml.sax.saxutils import escape

dictionary = {}

with open('link.md', 'r', encoding='utf-8') as fs:
    rendered = mistletoe.markdown(fs)
    soup = BeautifulSoup(rendered, "html.parser")
    a_list = soup.find_all("a")
    for item in a_list:
        if (item.string == None):
            print(item["href"])
            continue
        dictionary[item["href"]] = escape(item.string)

print(len(dictionary))