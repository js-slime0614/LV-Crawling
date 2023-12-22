from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

#드라이버 지정
chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
"plugins.always_open_pdf_externally": True 
})
webDriver = webdriver.Chrome(options=chrome_options)

#대법원 판례 열기
base_url = 'https://www.scourt.go.kr/supreme/news/NewsViewAction2.work?pageIndex=1&searchWord=&searchOption=&seqnum=9456&gubun=4&type=5'
webDriver.get(base_url)
webDriver.implicitly_wait(10) #로딩 끝날때까지 10초 기다리기

count = 0

while(1) :
    count += 1
    #저장할 a 태그의 href 요소안에 hwp 인지 pdf인지 판단후 hwp 만 다운로드
    files_to_save = webDriver.find_elements(By.CSS_SELECTOR,'td.attTxt > a')
    for file in files_to_save:
        if 'hwp' in file.get_attribute("href") :
            file.click()
            time.sleep(5)
    #다음판례로 넘기기
    try:
        #
        webDriver.find_element(By.CSS_SELECTOR, '#content > div.contentIn > table:nth-child(3) > tbody > tr:nth-child(2) > td > a').click()
        time.sleep(5)
    except:
        print('페이지넘기기 실패')
        if count < 50:
            try :
                webDriver.find_element(By.CSS_SELECTOR, 'table:nth-child(3) > tbody > tr > td > a').click()
                time.sleep(5)
            except:
                print('알수없는이유')
                break
        else:
            print('count50초과')
            break
        