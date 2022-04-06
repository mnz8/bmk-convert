'''
将保留书签与新的书签对比，合并生成新的

命令行参数：
参数一：保留文件
参数二：新的文件


问题1：标签内含有html未转义字符, 影响解析, 导致报错
       形如：<A HREF="" >HTML <a> 标签的 download 属性</A>
       增加 xml.sax.saxutils escape 转义

增加排序

'''
import os
import sys
import operator
import datetime
from bs4 import BeautifulSoup
from xml.sax.saxutils import escape

params = sys.argv[1:]


def create_dict(param):
    dictionary = {}
    with open(os.path.join(os.getcwd(), param), "r", encoding="utf-8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, "lxml")
        param_list = soup.find_all("a")
        for item in param_list:
            # AttributeError: 'NoneType' object has no attribute 'replace'
            if (item.string == None):
                print(item["href"])
                continue
            # 打印到报错位置 KeyError: 'href'
            # print(item)
            dictionary[item["href"]] = escape(item.string)
    # 按key升序
    sort_key_dict = dict(sorted(dictionary.items(), key=operator.itemgetter(0)))
    return sort_key_dict


def create_html(dictionary):
    htmlList = []
    for key, value in dictionary.items():
        # 过滤 None
        if value == None:
            continue
        htmlList.append("<DT><A HREF=\"" + key + "\" >" + value + "</A>")
    time_suffix = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    file = open(os.path.join(os.getcwd(), "ultimate_" + time_suffix + ".html"), "w+", encoding="utf-8")
    file.write("\n".join(htmlList))
    file.close()


def main():
    if (len(params) < 2) or ".html" not in params[0] or ".html" not in params[1]:
        print("incorrect parameter")
        return
    ultimate = params[0]
    filename = params[1]
    ultimate_dict = create_dict(ultimate)
    filename_dict = create_dict(filename)
    # ultimate_dict 覆盖 filename_dict
    merge_dict = {**filename_dict, **ultimate_dict}
    create_html(merge_dict)


main()