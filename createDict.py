#!/usr/bin/python3
from unicodedata import name
from bs4 import BeautifulSoup
import json
import os
import sys

if "c" in sys.argv[1:]:
    COUNT = True
else:
    COUNT = False


# 判断文件夹
def existsPath(path):
    if not os.path.exists(path):
        os.mkdir(path)


def singleProcess(filename):
    # 命名后缀
    suffix = filename.replace("bookmarks", "").replace(".html", "")
    with open(os.path.join("bookmarks", filename), "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, "lxml")
        aList = soup.find_all("a")
        dictionary = {}
        count = {}

        for item in aList:
            if item["href"] not in dictionary:
                dictionary[item["href"]] = item.string
                continue
            if item["href"] not in count:
                count[item["href"]] = 2
            else:
                count[item["href"]] += 1

    if len(dictionary) > 0:
        # 存储
        existsPath("dictionary")
        file = open(os.path.join(os.getcwd(), "dictionary/dictionary" + suffix + ".json"), "w+", encoding="utf-8")
        file.write(json.dumps(dictionary, ensure_ascii=False, indent=4, sort_keys=True))
        file.close()

    if COUNT and len(count) > 0:
        # 重复计数
        existsPath("count")
        file = open(os.path.join(os.getcwd(), "count/count" + suffix + ".json"), "w+", encoding="utf-8")
        file.write(json.dumps(count, ensure_ascii=False, indent=4, sort_keys=True))
        file.close()


# 遍历 bookmarks 文件夹
for maindir, subdir, file_name_list in os.walk(os.path.join(os.getcwd(), "bookmarks")):
    for filename in file_name_list:
        singleProcess(filename)
