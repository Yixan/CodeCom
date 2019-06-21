import requests
import just
import lxml.html
from selenium import webdriver
import os

# 首先需要登录github,在USERNAME中填入github账号，在PASSWORD中填入密码
USERNAME = ""
PASSWORD = ""
# 需要chrome浏览器驱动chromedriver。安装在Chrome/Application目录下。网上有配置教程
driver = webdriver.Chrome(executable_path="C:/Program Files (x86)/Google/Chrome/Application/chromedriver")

# github login 
driver.get("https://github.com/login")
driver.find_element_by_id("login_field").send_keys(USERNAME)
driver.find_element_by_id("password").send_keys(PASSWORD)
driver.find_element_by_id("password").submit()

# 定义文件存储路径，新建文件夹存爬虫数据。
path="D:\\data\\"
isExists=os.path.exists(path)
if not isExists:
    os.makedirs(path)
# start collecting links
links = set()

# 设置搜索的内容，使用github高级搜索，网上有github高级搜索教程。
query = "keras lstm model.add sequential language:python filename:*.py"

# 生成搜索的url
for i in range(1, 60):
    try:
        # p是页数，q是搜索内容
        url = "https://github.com/search?p={}&q={}&ref=searchresults&type=Code&utf8=%E2%9C%93"
        # 填入页数
        driver.get(url.format(i, query))
        tree = lxml.html.fromstring(driver.page_source)
        page_links = [x for x in tree.xpath('//a/@href') if "/blob/" in x and "#" not in x]
        links.update(page_links)
        print(i, len(links))
    except KeyboardInterrupt:
        break

# visit and save source files
base = "https://github.com"
for num, link in enumerate(links):
    # 生成文件名
    name=path+num.__str__()+".txt"
# 生成url
    url = base + link
    html = requests.get(url).text
    tree = lxml.html.fromstring(html)
    # 取网页数据
    xpath = '//*[@class="blob-code blob-code-inner js-file-line"]'
    contents = "\n".join([x.text_content() for x in tree.xpath(xpath)])
    # 把数据存到文件里
    with open(name, 'w',encoding="utf-8") as f:
        f.write(contents)
    print(num, len(contents))
print(contents)

other_options = []
# bigquery