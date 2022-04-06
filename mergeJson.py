#!/usr/bin/python3
"""
遍历 dictionary 文件夹，对比合并，输出最终的JSON文件

命令行参数：
h ：生成对应的html文件
r ：生成重复记录文件repeat.txt
"""
import json
import os
import sys

if "h" in sys.argv[1:]:
    HTML = True
else:
    HTML = False

if "r" in sys.argv[1:]:
    REPEAT = True
else:
    REPEAT = False

dictionary = {}
repeat = []


def diff(filename):
    with open(os.path.join("dictionary", filename), 'r', encoding="utf-8") as f:
        load_dict = json.load(f)
        for key, value in load_dict.items():
            if key not in dictionary:
                dictionary[key] = value
            else:
                repeat.append(key)


for maindir, subdir, file_name_list in os.walk(os.path.join(os.getcwd(), "dictionary")):
    for filename in file_name_list:
        diff(filename)

if len(dictionary) > 0:
    file = open(os.path.join(os.getcwd(), "ultimate.json"), "w+", encoding="utf-8")
    file.write(json.dumps(dictionary, ensure_ascii=False, indent=4, sort_keys=True))
    file.close()
    if HTML:
        htmlList = []
        with open(os.path.join(os.getcwd(), "ultimate.json"), 'r', encoding="utf-8") as f:
            ultimate_dict = json.load(f)
            for key, value in ultimate_dict.items():
                # 过滤 None
                if value == None:
                    continue
                htmlList.append("<DT><A HREF=\"" + key + "\" >" + value + "</A>")
        file = open(os.path.join(os.getcwd(), "ultimate.html"), "w+", encoding="utf-8")
        file.write("\n".join(htmlList))
        file.close()

if REPEAT and len(repeat) > 0:
    file = open(os.path.join(os.getcwd(), "repeat.txt"), "w+", encoding="utf-8")
    file.write("\n".join(repeat))
    file.close()
