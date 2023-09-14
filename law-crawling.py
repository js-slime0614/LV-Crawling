from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

#드라이버 지정
webDriver = webdriver.Chrome()

#법제처 국가법령정보센터 사이트열기
base_url = 'https://www.law.go.kr/lsSc.do?menuId=1&subMenuId=15&tabMenuId=81#undefined'
webDriver.get(base_url)
webDriver.implicitly_wait(10) #로딩 끝날때까지 10초 기다리기

#사이트 접속후 pdf 저장을 위해 리스트 밀어넣기
webDriver.find_element(By.CSS_SELECTOR, 'div.westClose').click()

webDriver.find_element(By.CSS_SELECTOR, '#listDiv > div.paging > a:nth-child(5)').click()
time.sleep(5)

webDriver.find_element(By.CSS_SELECTOR,'#listDiv > div.paging > ol > li:nth-child(3) > a').click()
time.sleep(5)

pageNum = 2

while(1) :
    #법령 본문 넘기기 위해정의
    contentNum = 0

    #해당법령클릭후 pdf 저장까지 구현
    while(1) :
        if contentNum >= 50: break
        webDriver.find_element(By.CSS_SELECTOR, '#liBgcolor' + str(contentNum) + ' > a').click()
        time.sleep(10)
        webDriver.find_element(By.CSS_SELECTOR, '#bdySaveBtn').click()
        time.sleep(5)
        webDriver.find_element(By.CSS_SELECTOR, 'input#FileSavePdf1.radio').click()
        webDriver.find_element(By.CSS_SELECTOR,'a#aBtnOutPutSave').click()
        time.sleep(5)
        contentNum += 1

    #5단위 페이지 넘기기
    if pageNum >= 6 :
        webDriver.find_element(By.CSS_SELECTOR, '#listDiv > div.paging > a:nth-child(4)').click()
        time.sleep(5)
        pageNum = 2

    #페이지 넘기기
    else :
        webDriver.find_element(By.CSS_SELECTOR,'#listDiv > div.paging > ol > li:nth-child('+ str(pageNum) +') > a').click()
        time.sleep(5)
        pageNum += 1