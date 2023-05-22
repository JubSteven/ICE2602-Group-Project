from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.queryparser.classic import QueryParser
import lucene
import jieba

# 分词辅助函数
def cut_word(word):
    word1 = ""  
    for i in jieba.cut_for_search(word):
        word1 += i
        word1 += ' '  
    return word1   

# 解析搜索的商品
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

# 搜索函数
def get_search_result(searcher, analyzer, command):
    title_lst = []
    product_url_lst = []
    pic_url_lst = []
    price_lst = []
    advertisement_lst = []
    comments_lst = []
    shop_url_lst = []
    shop_lst = []
    keyword_lst = []
    command_lst = []
    while True:
        if command == '':
            return
        
        command_dict = parseCommand(command)
        vm_env = lucene.getVMEnv()
        vm_env.attachCurrentThread()
        querys = BooleanQuery.Builder()
        for k,v in command_dict.items():
            query = QueryParser(k, analyzer).parse(v)
            querys.add(query, BooleanClause.Occur.MUST)
        scoreDocs = searcher.search(querys.build(), 750).scoreDocs
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            title_lst.append(doc.get('title_ini'))
            product_url_lst.append(doc.get('product_url'))
            pic_url_lst.append(doc.get("pic_url"))
            
            price_lst.append("".join(list(filter(lambda x: str.isdigit(x) or x==".", list(doc.get('price'))))))
                
            advertisement_lst.append(doc.get('advertisement_ini'))
            if doc.get("comments") != " ":
                if "评价" in doc.get("comments"): 
                    comments_lst.append(doc.get('comments')[:-2])
                else:
                    comments_lst.append(doc.get('comments'))
            else:
                comments_lst.append(0)

            shop_url_lst.append(doc.get('shop_url'))
            shop_lst.append(doc.get('shop_ini'))
            if "公益" in doc.get("keyword"):
                keyword_lst.append("成交额部分用于公益")
            else:
                keyword_lst.append(doc.get("keyword"))
            command_lst.append("command")
            
        break
    
    return title_lst, product_url_lst, pic_url_lst, price_lst, advertisement_lst, comments_lst, shop_url_lst, shop_lst, keyword_lst, command_lst

def keyword_processing(keyword_lst):
    target = []
    for i in range(len(keyword_lst)):
        raw = ''.join(keyword_lst[i]).replace(" ", "")
        target.append(raw)
        
    return target

def product_price_processing(products):
    for i in range(len(products)):
            try:
                products[i][3] = float(products[i][3])
            except ValueError:
                products[i][3] = -1
        
    products.sort(key=lambda x: float(x[3]), reverse=True)  # 按照元组的第三个数排
    for i in range(len(products)):
        if products[i][3] == -1:
            products[i][3] = "暂无价格"
            
    return products


def comments_num_sort(products):
    for i in range(len(products)):
        flag = False
        if "万" in str(products[i][5]):
            flag = True
        products[i][5] = int(float("".join(list(filter(lambda x: str.isdigit(x) or x==".", list(str(products[i][5])))))))
        products[i][5] *= 10000 if flag else 1            
        
    products.sort(key=lambda x: int(x[5]), reverse=True)
    return products

def comments_num_string(products):
    for i in range(len(products)):
        if int(products[i][5]) >= 10000:
            products[i][5] = "{}万+".format(products[i][5] // 10000)
        else:
            products[i][5] = "{}+".format(products[i][5])
                        
    return products

def sort_(result, method, reverse_opt):
    # 这里要求result的顺序不变，由索引来提取相应的信息
    products = []
    for i in range(len(result[0])):
        product = []
        for j in range(10):
            product.append(result[j][i])
        products.append(product)
    
    if method == "price":
        products = product_price_processing(products)
                
    elif method == "quality":
        products = comments_num_sort(products)
        products = comments_num_string(products)

    
    results = [[] for _ in range(10)]
    for each in products:
        for i in range(10):
            results[i].append(each[i])
            
    if reverse_opt == 1:
        results = reverse_(results)
    
    return results

def reverse_(results):
    for i in range(len(results)):
        a = results[i]
        a.reverse()
        results[i] = a
        
    return results