import pandas as pd
import numpy as np

def get_products():
    df = pd.read_csv("data.csv")

    products = []
    for each in df.values.tolist():
        info = dict()
        info["title"] = each[0]
        info["product_url"] = each[1]
        info["pic_url"] = each[2]
        info["price"] = str(each[3])
        info["advertisement"] = each[5]
        info["comments"] = each[6]
        info["shop_url"] = each[7]
        info["shop"] = each[8]
        info["keyword"] = each[9]
        products.append(info)

    return products
# print(products[0])
# print(type(products[0]["advertisement"]))