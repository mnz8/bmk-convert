'''
将参数文件 json转为html

打印 value 为None 的链接
'''
import json
import os
import sys

filename = sys.argv[1:][0]

if ("json" in filename):
    prefix = filename.replace(".json", "")
    htmlList = []
    with open(os.path.join(os.getcwd(), filename), 'r', encoding="utf-8") as f:
        json_dict = json.load(f)
        for key, value in json_dict.items():
            # 过滤 None
            if value == None:
                print(key)
                continue
            htmlList.append("<DT><A HREF=\"" + key + "\" >" + value + "</A>")
    file = open(os.path.join(os.getcwd(), prefix + ".html"), "w+", encoding="utf-8")
    file.write("\n".join(htmlList))
    file.close()