from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
from datetime import datetime

#드라이버 지정
webDriver = webdriver.Chrome()

#csv 파일에 저장할 요소 리스트 선언
news_urls = []
news_companys = []
news_titles = []
news_column = 0

#csv 파일 이름에 지정할 datetime 출력
todayTime = datetime.today().strftime("%Y-%m-%d")

#사이트 열기
webDriver.get('https://news.naver.com/')
webDriver.implicitly_wait(10) #로딩 끝날때까지 10초 기다리기

#뉴스 검색돋보기 클릭
webDriver.find_element(By.CSS_SELECTOR,'a.Ntool_button._search_content_toggle_btn').click()
time.sleep(2)

#뉴스 검색 Input 클릭
search = webDriver.find_element(By.CSS_SELECTOR, 'input.u_it._search_input')
search.click()

#검색어 입력
searchWord = '부동산'
search.send_keys(searchWord)
search.send_keys(Keys.ENTER)
webDriver.switch_to.window(webDriver.window_handles[1])

#데이터 csv 저장
f = open(searchWord + todayTime + '.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
def append_csv(column, category, news_company ,news_title, news_url):
    wr.writerow([column, news_company, category, news_title, news_url])
    print(column, '번째 csv 요소 삽입완료')

while(1) :
    #네이버뉴스 클릭
    ems = webDriver.find_elements(By.CSS_SELECTOR, 'div.news_info > div.info_group > a:nth-child(3)')
    titles = webDriver.find_elements(By.CSS_SELECTOR,'a.news_tit')
    for i in titles:
        news_titles.append(i.text)
    companys = webDriver.find_elements(By.CSS_SELECTOR, "div.news_info > div.info_group > a.info.press")
    for i in companys:
        news_companys.append(i.text)

    for i in ems:
        i.click()

        # 현재탭에 접근
        webDriver.switch_to.window(webDriver.window_handles[2])
        time.sleep(2) #대기시간 변경 가능

        # 네이버 뉴스 url만 가져오기
        url = webDriver.current_url

        #네이버 뉴스 일시 url append
        if "news.naver.com" in url:
            news_urls.append(url)

        else:
            pass

        # 현재 탭 닫기
        webDriver.close()

        # 다시처음 탭으로 돌아가기
        webDriver.switch_to.window(webDriver.window_handles[1])

    #다음페이지로 넘어가는 btn 클릭
    btn_next = webDriver.find_element(By.CSS_SELECTOR, '#main_pack > div.api_sc_page_wrap > div > a.btn_next')
    is_disabled = True if btn_next.get_attribute("aria-disabled") == 'true' else False
    if is_disabled : break
    btn_next.click()

    #csv 파일에 데이터 입력
    if len(news_urls) != 0:
        csv_input_length = len(news_urls) - news_column
        for i in range(csv_input_length):
            append_csv(news_column, news_companys[news_column], searchWord, news_titles[news_column], news_urls[news_column])
            news_column += 1

f.close()