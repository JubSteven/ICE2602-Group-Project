#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, jieba

from java.io import File
from java.nio.file import Path
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from urllib.parse import urlparse

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""

def cut_word(word):
    word1 = ""  
    for i in jieba.cut_for_search(word):
        word1 += i
        word1 += ' '  
    return word1          


def parseCommand(command):

    allowed_opt = ['shop']
    command_dict = {}
    opt = 'search'
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                shop = cut_word(value)
                command_dict[opt] = command_dict.get(opt, '') + ' ' + shop
        else:
            m = cut_word(i)
            command_dict[opt] = command_dict.get(opt, '') + ' ' + m
    return command_dict

def run(searcher, analyzer):
    while True:
        print()
        print ("Hit enter with no input to quit.")
        command = input("Query:")
        # command = unicode(command, 'GBK')
        if command == '':
            return

        print()
        print ("Searching for:", command)
        
        command_dict = parseCommand(command)
        querys = BooleanQuery.Builder()
        for k,v in command_dict.items():
            query = QueryParser(k, analyzer).parse(v)
            querys.add(query, BooleanClause.Occur.MUST)
        scoreDocs = searcher.search(querys.build(), 50).scoreDocs
        print("%s total matching documents." % len(scoreDocs))

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
##            explanation = searcher.explain(query, scoreDoc.doc)
            print("------------------------")
            print('pic_url:', doc.get("pic_url"))
            print('product_url:', doc.get('product_url'))
            print('comments:', doc.get('comments'))
            print('comments_num:', doc.get('comments_num'))
            print('price:', doc.get('price'))
            print('shop_url:', doc.get('shop_url'))
            print('advertisement:', doc.get('advertisement_ini'))
            print('shop:', doc.get('shop_ini'))
            print('keyword:', doc.get('keyword'))
            print('title:', doc.get('title_ini'))
            
##            print explanation


if __name__ == '__main__':
    STORE_DIR = "index1"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer()
    run(searcher, analyzer)
    del searcher
