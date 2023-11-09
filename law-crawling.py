from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 드라이버 지정
webDriver = webdriver.Chrome()

# 법제처 국가법령정보센터 사이트열기
base_url = 'https://www.law.go.kr/expcSc.do?menuId=7&subMenuId=51&tabMenuId=237&query=#AJAX'
webDriver.get(base_url)
webDriver.implicitly_wait(10) #로딩 끝날때까지 10초 기다리기
time.sleep(5)

# 크롤링중 끊겼을시 끊긴위치로 이동
for i in range(0, 26): # 반복문으로 최적화 처리
    webDriver.find_element(By.CSS_SELECTOR, '#listDiv > div.paging > a:nth-child(4)').click()
    time.sleep(3)
    i += 1
webDriver.find_element(By.CSS_SELECTOR,'#listDiv > div.paging > ol > li:nth-child(2) > a').click()

# 현재 페이지 반영
# Current Page 132 from
pageNum = 3
checknum = 1
while(1) :
    
    time.sleep(10)
    contents = webDriver.find_elements(By.CSS_SELECTOR, 'ul.left_list_bx > li > a')
    for content in contents:
        try : 
            # 원하는부분에서 크롤링 하기 위해 넘기기
            if checknum <= 0:
                checknum += 1
                continue

            content.click()
            webDriver.implicitly_wait(100)
            time.sleep(20)
            
            webDriver.find_element(By.CSS_SELECTOR, '#bdySaveBtn').click()
            webDriver.implicitly_wait(20)
            time.sleep(5)
            webDriver.find_element(By.CSS_SELECTOR, 'select#EmpDocSelectId').click()
            webDriver.find_element(By.CSS_SELECTOR,'#EmpDocSelectId > option:nth-child(2)').click()
            webDriver.find_element(By.CSS_SELECTOR,'input#empSaveBtn').click()
            webDriver.implicitly_wait(20) 
            time.sleep(5)

        except:
            print("Get Exception")
            continue
    
    # 5단위 페이지 넘기기
    if pageNum >= 6 :
        time.sleep(10)
        webDriver.find_element(By.CSS_SELECTOR, '#listDiv > div.paging > a:nth-child(4)').click()
        webDriver.implicitly_wait(20) 
        time.sleep(5)
        pageNum = 2

    # 페이지 넘기기
    else :
        time.sleep(10)
        webDriver.find_element(By.CSS_SELECTOR,'#listDiv > div.paging > ol > li:nth-child('+ str(pageNum) +') > a').click()
        webDriver.implicitly_wait(20) 
        time.sleep(5)
        pageNum += 1