import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from snownlp import SnowNLP
from snownlp import sentiment
import jieba.posseg as psg

def stop_words_lst():
    stopwords = [line.strip() for line in open("/workspaces/code/stopwords.txt", encoding='UTF-8').readlines()]
    stopwords.append("耳机")
    stopwords.append("京东")
    return stopwords

df = pd.read_csv("raw_comments3.csv")
df_lst = df.values.tolist()
new_dict = {"target_URL": [], "score": [], "keywords": [], "comment_avg": []}

new_dict['target_URL'].append(df_lst[0][12].split("#")[0])
new_dict['score'].append(df_lst[0][16])
new_dict['keywords'].append(df_lst[0][17])
ID = ''.join(list(filter(str.isdigit, str(df_lst[0][12]))))

count = 0
comment_score = 0
text = ""
for i in range(len(df_lst)):
    if str(df_lst[i][12]).split("#")[0] in new_dict['target_URL']:
        s = SnowNLP(str(df_lst[i][5]))
        t = s.sentiments
        comment_score += t
        count += 1
        text += str(df_lst[i][5])
        
    else:
        # 先结束上一轮
        new_dict['comment_avg'].append(comment_score / count)
        
        # print(new_dict)
        
        stop_words = stop_words_lst()
        new_text = ""
        for each in text:
            if each not in stop_words:
                new_text = "{} {}".format(new_text, each)

        # 生成对象
        wc = WordCloud(font_path = "/workspaces/code/msyh.ttc",width=500, height=400, mode="RGBA", background_color=None).generate(new_text)
        # 显示词云图
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")

        wc.to_file("/workspaces/code/static/wordcloud_{}.png".format(ID))
        
        print(i, " [DONE] ")
        
        
        # 再开始下一轮
        new_dict['target_URL'].append(str(df_lst[i][12]).split("#")[0])
        new_dict['score'].append(df_lst[i][16])
        new_dict['keywords'].append(df_lst[i][17])
        ID = ''.join(list(filter(str.isdigit, str(df_lst[i][12]))))


new_dict['comment_avg'].append(comment_score / count)
        
stop_words = stop_words_lst()
new_text = ""
for each in text:
    if each not in stop_words:
        new_text = "{} {}".format(new_text, each)
        
# 生成对象
wc = WordCloud(font_path = "/workspaces/code/msyh.ttc",width=500, height=400, mode="RGBA", background_color=None).generate(new_text)
# 显示词云图
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")

wc.to_file("/workspaces/code/static/wordcloud_{}.png".format(ID))

print("FINAL DONE")


# product_URL = df['页面网址']
# target_URL_lst = list(set(product_URL.values.tolist()))


# for j in range(len(target_URL_lst)):
#     print(j)
#     target_URL = target_URL_lst[j]
#     if target_URL in new_dict["target_URL"]:
#         continue
    
#     target_comment_id_lst = []
#     for i in range(len(product_URL)):
#         ID = ''.join(list(filter(str.isdigit, str(product_URL[i]))))
#         keyword_raw = df_lst[i][17]
#         score_raw = df_lst[i][16]
#         target_comment_id_lst.append(i)
            

#     text_all = []
#     for each in target_comment_id_lst:
#         text_all.append(df_lst[each][5])        

#     comment_score = 0
#     count = 0
#     for i in range(len(text_all)):
#         s = SnowNLP(str(text_all[i]))
#         t = s.sentiments
#         comment_score += t
#         count += 1
#     comment_score = comment_score / count

#     text = ' '.join(jieba.lcut(''.join(str(text_all))))
#     stop_words = stop_words_lst()
#     new_text = ""
#     for each in text:
#         if each not in stop_words:
#             new_text = "{} {}".format(new_text, each)

#     # 生成对象
#     wc = WordCloud(font_path = "/workspaces/code/msyh.ttc",width=500, height=400, mode="RGBA", background_color=None).generate(new_text)
#     # 显示词云图
#     plt.imshow(wc, interpolation="bilinear")
#     plt.axis("off")

#     wc.to_file("/workspaces/code/static/wordcloud_{}.png".format(ID))
    
#     new_dict["target_URL"].append(target_URL)
#     new_dict["keywords"].append(keyword_raw)
#     new_dict["score"].append(score_raw)
#     new_dict["comment_avg"].append(comment_score)
    
#     print(target_URL, " [DONE] ")
    
print(new_dict)
df_new = pd.DataFrame(new_dict)
df_new.to_csv("comments.csv", encoding='utf_8_sig')
    
    
    


    
    

