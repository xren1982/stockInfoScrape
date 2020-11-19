import os
import pandas as pd
import json


def crawl():
    cacheClean()
    os.system("scrapy crawl prnewswire -o ./bin/prnewswire.json")
    dataFiles = getJsonFile()
    print('Data Scrapped in below files:')
    for f in dataFiles:
        print(f)

def getJsonFile():
    dir = os.getcwd()
    bin = os.path.join(dir, "bin")
    fileList = os.listdir(bin)
    dataFiles = [file for file in fileList if file.endswith(".json") and file.__contains__('input') == False]
    dataFileList = []
    for file in dataFiles:
        dataFileList.append(os.path.join(bin, file))
    return dataFileList

def searchfile(keyword, searchpath):
    items = os.listdir(searchpath)
    for item in items:
        path = os.path.join(searchpath, item)
        name = os.path.splitext(item)[0]
        suffix = os.path.splitext(item)[1]
        if(keyword in name):
            return path

    return ''

def cacheClean():
    c = 0
    dataFileList = getJsonFile()
    for file in dataFileList:
        os.remove(file)
        c+=1
    print('Removed ' + str(c) + ' Files!')

def SearchList(kwList,string):
    s = ''
    for x in kwList:
        xLen = len(x.split())
        if xLen > 1:
            if (x.lower() in string.lower()):
                s = s+', '+str(x)
        elif xLen == 1:
            if (x.lower() in string.lower().split()):
                s = s+', '+str(x)
    return s[2:]

if __name__ == "__main__":

    print('Web Crawl for news site Start!')
    crawl()
    print('Web Crawl for news site End!')
    
    print('Web Crawl for stock site Start!')
    tmpdownloadpath = searchfile('output_stockinfo',os.getcwd())
    if os.path.exists(tmpdownloadpath):
        os.remove(tmpdownloadpath)
    os.system("scrapy crawl nasdaq -o ./output_stockinfo.csv")
    print('Web Crawl for stock site End!')
    