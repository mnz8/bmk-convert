#!/usr/bin/python3
from bs4 import BeautifulSoup
import os

if not os.path.exists("flat"):
    os.mkdir("flat")


def singleProcess(filename):
    suffix = filename.replace("bookmarks", "")
    with open(os.path.join("bookmarks", filename), "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, "lxml")
        aList = soup.find_all("a")
        newList = []

        for item in aList:
            newList.append("<DT><A HREF=\""+item["href"]+"\" >"+item.string+"</A>")

        file = open(os.path.join(os.getcwd(), "flat/flat" + suffix), "w+", encoding="utf-8")
        file.write("\n".join(newList))
        file.close()


for maindir, subdir, file_name_list in os.walk(os.path.join(os.getcwd(), "bookmarks")):
    for filename in file_name_list:
        singleProcess(filename)
