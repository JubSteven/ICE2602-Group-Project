import products
import threading
import queue
import time
import os
from queue import Empty
import re
import string
import sys
INDEX_DIR = "IndexFiles.index"
from cgi import FieldStorage
import sys, os, lucene, threading, time, re
from datetime import datetime
import pandas as pd
from java.io import File
from java.nio.file import Path
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, StringField, TextField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.pylucene.search.similarities import PythonSimilarity, PythonClassicSimilarity

import jieba

from urllib.parse import urlparse

def deal_nan(a):
    if pd.isna(a):
        return " "
    else:
        return a


# 0: title, 1: product_url, 2: pic_url, 3: price, 4: advertisement, 5: comments,
# 6: comments_num, 7: shop_url, 8: shop, 9: keyword, 10：title_ini, 11: advertisement_ini, 12: shop_ini
def get_data(product):
    a = []
    title = cut_word(deal_nan(product["title"]))
    a.append(title)
    a.append(deal_nan(product["product_url"]))
    a.append(deal_nan(product["pic_url"]))
    a.append(deal_nan(product["price"]))
    a.append(cut_word(deal_nan(product["advertisement"])))
    
    if not pd.isna(product["comments"]):
        c = product["comments"].split("+")[0]
        if c[-1] == "万":
            c = c[0: -1] + "0000"
        a.append(product["comments"].split("条")[0])
        a.append(c)
    else:
        a.append(" ")
        a.append(" ")
    a.append(deal_nan(product["shop_url"]))
    a.append(cut_word(deal_nan(product["shop"])))
    k = deal_nan(product["keyword"]).translate(str.maketrans({"\n":" ", "\t": " "}))
    a.append(k)
    
    a.append(deal_nan(product["title"]))
    a.append(deal_nan(product["advertisement"]))
    a.append(deal_nan(product["shop"]))
    
    
    return a
    
    
#分词器（jieba分词后转为可以被WhitespaceAnalyzer识别的字符串）      
def cut_word(word):
    word1 = ""  
    for i in jieba.cut_for_search(word):
        word1 += i
        word1 += ' '  
    return word1          

class Ticker(object):
    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)


#主体部分
#爬取网站，将所需的商品信息存入index中，以用来索引
class IndexFiles(object):
    def __init__(self, times_to_crawl, storeDir):
 
        self.times_to_crawl = times_to_crawl       
        store = SimpleFSDirectory(File(storeDir).toPath())
        analyzer = WhitespaceAnalyzer()
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        self.products = products.get_products()
        # set a new similarity computing method
        config.setSimilarity(PythonClassicSimilarity())

        writer = IndexWriter(store, config)
        self.get_url_jd(writer)
        ticker = Ticker()
        print('commit index')
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False      
            
        print('done')  


    def get_url_jd(self, writer):
        for i in range(self.times_to_crawl):
            product = get_data(self.products[i])
            
            #将结果存储
            doc = Document()
            
            doc.add(StringField("pic_url", product[2], Field.Store.YES))          
            doc.add(StringField('product_url', product[1], Field.Store.YES))                                 
            doc.add(StringField('comments', product[5], Field.Store.YES))
            doc.add(StringField('comments_num', product[6], Field.Store.YES))
            doc.add(StringField('price', product[3], Field.Store.YES))
            doc.add(StringField('shop_url', product[7], Field.Store.YES))
            doc.add(StringField('title_ini', product[10], Field.Store.YES))
            doc.add(StringField('advertisement_ini', product[11], Field.Store.YES))            
            doc.add(StringField('shop_ini', product[12], Field.Store.YES))
            
            doc.add(TextField('advertisement', product[4], Field.Store.NO))            
            doc.add(TextField('shop', product[8], Field.Store.NO))
            doc.add(TextField('keyword', product[9], Field.Store.YES))
            doc.add(TextField('title', product[0], Field.Store.NO))
            doc.add(TextField('search', product[0] + product[4] + product[8] + product[9], Field.Store.NO))
            
            writer.addDocument(doc)
            url = product[1]
            print (f"add {url}")


if __name__ == "__main__":
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    start = datetime.now()
    try:
        IndexFiles(10500, "index1")
        end = datetime.now()
        print(end - start)
    except Exception as e:
        print("Failed: ", e)
        raise e

