#!/usr/bin/python3
"""
将 bookmarks 文件夹内书签展平，放在 flat 文件夹

增加 xml.sax.saxutils escape 转义
"""
import os
from bs4 import BeautifulSoup
from xml.sax.saxutils import escape

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
            if item.string == None:
                continue
            newList.append("<DT><A HREF=\"" + item["href"] + "\" >" + escape(item.string) + "</A>")

        file = open(os.path.join(os.getcwd(), "flat/flat" + suffix), "w+", encoding="utf-8")
        file.write("\n".join(newList))
        file.close()


for maindir, subdir, file_name_list in os.walk(os.path.join(os.getcwd(), "bookmarks")):
    for filename in file_name_list:
        singleProcess(filename)
