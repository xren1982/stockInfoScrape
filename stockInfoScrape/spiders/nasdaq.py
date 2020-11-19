import scrapy
from ..items import StockInfoItem
import pandas as pd
from configparser import ConfigParser
import os
import json
import datetime

def getJsonFile():
    dir = os.getcwd()
    dir.replace('spiders/','')
    bin = os.path.join(dir, "bin")
    fileList = os.listdir(bin)
    dataFiles = [file for file in fileList if file.endswith(".json") and file.__contains__('input') == False]
    dataFileList = []
    for file in dataFiles:
        dataFileList.append(os.path.join(bin, file))
    return dataFileList

class NasdaqSpider(scrapy.Spider):
    name = 'nasdaq'
    start_urls = ['https://api.nasdaq.com/api/quote/BHC/historical?assetclass=stocks&fromdate=2015-11-19&limit=18&offset=18&todate=2020-11-19']
    
   

    def parse(self, response):
        currentday = str(datetime.date.today().year)+'-'+str(datetime.date.today().month).rjust(2, '0')+'-'+str(datetime.date.today().day).rjust(2, '0')
        stockDetailURLTemplate = 'https://api.nasdaq.com/api/quote/stockname/historical?assetclass=stocks&fromdate=2019-05-19&limit=5&todate='+currentday
        dataFiles = getJsonFile()
        for jsonFilePath in dataFiles:
            df = pd.DataFrame(json.load(open(jsonFilePath)))
            for i in df.index:
                stockname = df['stockname'].at[i]
                stockDetailURL = stockDetailURLTemplate.replace('stockname',stockname)
                request = response.follow(stockDetailURL, callback = self.getContent)
                yield request
        
        stockDetailURL = 'https://api.nasdaq.com/api/quote/shop/historical?assetclass=stocks&fromdate=2019-05-19&limit=5&todate='+currentday
        request = response.follow(stockDetailURL, callback = self.getContent)
        yield request 
        
    def getContent(self, response):
        try:
            jsonBody = json.loads(response.body.decode('gbk').encode('utf-8'))
            htmlcode = jsonBody['data']['tradesTable']['rows']
            df = pd.DataFrame(htmlcode)
            df['stockname'] = jsonBody['data']['symbol']
            print(df)
            for i in df.index:
                spiderItem = StockInfoItem()
                spiderItem['stockname'] = str(df['stockname'].at[i])
                spiderItem['date'] = str(df['date'].at[i])
                spiderItem['close'] = str(df['close'].at[i])
                spiderItem['volume'] = str(df['volume'].at[i])
                spiderItem['open'] = str(df['open'].at[i])
                spiderItem['high'] = str(df['high'].at[i])
                spiderItem['low'] = str(df['low'].at[i])
                yield spiderItem
        except Exception as e:
            print('invalid stock codes')
        
                
        
        
        
        


