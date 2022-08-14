'''
chrome bookmarks convert markdown

命令行参数：
参数一: html 文件 或者 html 文件夹

xml.sax.saxutils escape 转义
sorted 排序

python cbm2md.py test/bookmarks.html
'''
import os
import sys
import operator
import datetime
from bs4 import BeautifulSoup
from xml.sax.saxutils import escape

params = sys.argv[1:]


# 生成对应字典
def create_dict(param, foldername=''):
    dictionary = {}
    if (foldername):
        file = os.path.join(os.getcwd(), foldername, param)
    else:
        file = os.path.join(os.getcwd(), param)
    with open(file, "r", encoding="utf-8") as f:
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
    return dictionary


# 生成 markdown
def create_markdown(dictionary):
    htmlList = []
    for key, value in dictionary.items():
        # 过滤 None
        if value == None:
            continue
        htmlList.append("[" + value + "](" + key + ")")
    time_suffix = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    file = open(os.path.join(os.getcwd(), "markdown_" + time_suffix + ".md"), "w+", encoding="utf-8")
    file.write("\n".join(htmlList))
    file.close()


def main():
    if (len(params) == 0):
        print("需要参数：书签文件或者书签的文件夹")
        return
    if (len(params) > 1):
        print("只需要一个参数")
        return

    receive = params[0]
    fullpath = os.path.join(os.getcwd(), receive)

    # 文件
    if os.path.isfile(fullpath):
        if ".html" in receive:
            create_markdown(create_dict(receive))
            return
        else:
            print("not an html")
            return

    # 文件夹
    if os.path.isdir(fullpath):
        total_dict = {}
        for maindir, subdir, file_name_list in os.walk(fullpath):
            for filename in file_name_list:
                if ".html" in filename:
                    filename_dict = create_dict(filename, receive)
                    # 重复的情况：后面覆盖之前的
                    total_dict = {**total_dict, **filename_dict}
        # 按key升序
        sort_key_dict = dict(sorted(total_dict.items(), key=operator.itemgetter(0)))
        create_markdown(sort_key_dict)
        return

    # error
    print("something error")


main()