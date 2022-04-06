'''
最终版

将保留书签与指定文件夹内所有书签对比合并，生成最新文件
如果存在重复，则以保留书签的值保存；如果是指定文件夹内部重复，则以文件夹内书签顺序为准

命令行参数：
参数一：保留书签
参数二：指定文件夹

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


# 生成新的html
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
    if (len(params) < 2) or ".html" not in params[0] or ".html" in params[1]:
        print("参数1书签名，参数2文件夹名")
        return
    ultimate = params[0]
    foldername = params[1]
    if not os.path.exists(foldername):
        print('文件夹错误')
        return
    ultimate_dict = create_dict(ultimate)

    for maindir, subdir, file_name_list in os.walk(os.path.join(os.getcwd(), foldername)):
        for filename in file_name_list:
            filename_dict = create_dict(filename, foldername)
            # 重复的情况：ultimate_dict 覆盖 filename_dict
            ultimate_dict = {**filename_dict, **ultimate_dict}

    # 按key升序
    sort_key_dict = dict(sorted(ultimate_dict.items(), key=operator.itemgetter(0)))
    create_html(sort_key_dict)


main()