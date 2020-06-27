import requests
import os, time, sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def usage():
    print("USAGE : python",sys.argv[0],"Keyword")

if len(sys.argv) == 1:
    usage()
    quit(-1)

# launch chrome browser
driver = webdriver.Chrome()
# google image search
driver.get('https://www.google.co.jp/imghp?hl=ja&tab=wi&ogbl')
# execute search
keyword = sys.argv[1]
print(keyword)
driver.find_element_by_name('q').send_keys(keyword, Keys.ENTER)

current_url = driver.current_url
print(current_url)
html = requests.get(current_url)
bs = BeautifulSoup(html.text, 'lxml')
images = bs.find_all('img', limit=50)
print(images)

os.makedirs(keyword)
WAIT_TIME = 3

for i, img in enumerate(images, 1):
    src = img.get('src')
    print(src)
    print("i",i)
    a ,e = os.path.splitext(src)
    print(a,e)
    if e == ".gif":
        continue
    print("e",e)
    response = requests.get(src)
    print(response)
    with open(keyword + '/' + '{}.jpg'.format(i), 'wb') as f:
        f.write(response.content)
    time.sleep(WAIT_TIME)

driver.quit()
