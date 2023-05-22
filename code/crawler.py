from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import xlwt  # 进行excel操作
#谷歌驱动 告诉电脑在哪打开浏览器
def crawler(pages):
    driver=webdriver.Chrome(executable_path=r"C:/Users/OMEN/AppData/Local/Programs/Python/Python39/chromedriver.exe")
    #打开网页
    driver.get("https://www.jd.com")
    driver.implicitly_wait(5)#隐式休息5s
    driver.maximize_window()
    #通过xpath找到输入框输入要搜索的
    driver.find_element(By.XPATH, "//*[@id='key']").send_keys("耳机")
    #通过xpath找到搜索按钮点击
    driver.find_element(By.XPATH, "//*[@id='search']/div/div[2]/button").click()
    driver.implicitly_wait(5)#隐式休息5s
    pics = []
    titles = []
    links = []
    prices=[]
    comments=[]
    shops=[]
    shop_urls = []
    keywords = []
    
    #存数据
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('京东', cell_overwrite_ok=True)  # 创建工作表
    col = ("标题", "标题链接", "图片", "价格", "评论", "商店", "商店链接", "关键词")
    w = 0
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 列名
    def data_write(w, item, line):
        for m in item:
            w += 1
            sheet.write(w, line, m)
            
    for j in range(1, pages + 1):
        # 获取当前第一页所有商品的li标签
        for n in [titles, links, pics, prices, comments, shops, shop_urls, keywords]:
            n.clear()
        goods = driver.find_element(By.CSS_SELECTOR, "#J_goodsList > ul")
        print(0)
        for i in range(1, 61):              
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,f'//*[@id="J_goodsList"]/ul/li[{i}]')))        
            good = goods.find_element(By.XPATH, f'//*[@id="J_goodsList"]/ul/li[{i}]')
            driver.execute_script("arguments[0].scrollIntoView(false);",good)
            print(1)
            # 获取商品图片
            try:
                pic = good.find_element(By.CSS_SELECTOR, ".p-img img").get_attribute("src")                
            except:
                pic = " "
            print("pic: ", pic)
            # 获取商品标题
            try:               
                title = good.find_element(By.CSS_SELECTOR, ".p-name em").text.replace('\n', '')
            except:
                title = " "
            print("title: ", title)
            # 获取商品链接
            try:
                link = good.find_element(By.CSS_SELECTOR, ".p-name a").get_attribute('href')
            except:
                link = " "
            print("link: ", link)
            # 获取商品价格
            try:
                price = good.find_element(By.CSS_SELECTOR, ".p-price strong").text.replace('\n', '')
            except:
                price = " "
            print("price: ", price)
            # 获取商品评价数量
            try:
                comment = good.find_element(By.CSS_SELECTOR, ".p-commit strong a").text
            except:
                comment = " "
            print("comment: ", comment)
            # 获取店铺名称
            try:
                shop = good.find_element(By.CSS_SELECTOR, ".p-shop a").text
            except:
                shop = " "
            print("shop: ", shop)
            # 获取店铺链接
            try:
                shop_url = good.find_element(By.CSS_SELECTOR, ".p-shop a").get_attribute("href")
            except:
                shop_url = " "          
            print("shop_url: ", shop_url)
            # 获取关键词
            try:
                keyword = " "
                keyword_shop = good.find_elements(By.CSS_SELECTOR, ".p-icons i")
                for each in keyword_shop:
                    keyword = keyword + each.text + " "
            except:
                keyword = " "
            pics.append(pic), titles.append(title), links.append(link), prices.append(price)
            comments.append(comment), shops.append(shop), shop_urls.append(shop_url), keywords.append(keyword)
        
        driver.find_element(By.XPATH, "//*[@id='J_bottomPage']/span[1]/a[9]").click()
        sleep(2)
        line = 0       
        for n in [titles, links, pics, prices, comments, shops, shop_urls, keywords]:
            data_write(w, n, line)
            line += 1
        w += 60
        print("第"+str(j)+"页")
        
    print("爬取完毕！")

    book.save("京东.xls")  # 保存
    print("关闭浏览器，保存数据")

if __name__ == "__main__":
    pages = 3   #爬取商品网站的页数（每一页有60件商品）1-base
    crawler(pages)
    print("完成！")