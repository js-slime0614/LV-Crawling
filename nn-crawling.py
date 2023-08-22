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

# 100 - 정치 
# 101 - 경제
# 102 - 사회 
# 103 - 생활문화 
# 104 - 세계 
# 105 - IT/과학

search_num = 2

category_num = ['100', '101', '102', '103','104','105']
category_name = ['정치', '경제', '사회','생활문화', '세계','IT과학']
current_page = 1
#네이버뉴스 사이트 열기
base_url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=' + category_num[search_num]
webDriver.get(base_url)
webDriver.implicitly_wait(2) #로딩 끝날때까지 10초 기다리기

#데이터 csv 저장
f = open(todayTime + category_name[search_num] + '.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)

def append_csv(column, news_date, news_company ,news_title, news_url):
    wr.writerow([column, news_date, news_company, news_title, news_url])
    print(str(column) + '번째 csv 요소 삽입완료')

append_csv('column','date','언론사','헤드라인','URL')

while(1) :

    #뉴스 클릭
    ems = webDriver.find_elements(By.CSS_SELECTOR, 'dl > dt:nth-child(2) > a')
    
    #뉴스 타이틀, url 수짐
    for i in ems:
        news_titles.append(i.text)
        print(i.text)
        news_urls.append(i.get_attribute("href"))
        print(i.get_attribute("href"))

    #언론사 정보 수집
    companys = webDriver.find_elements(By.CSS_SELECTOR, 'span.writing')
    for i in companys:
        news_companys.append(i.text)

    #페이지 바꾸기
    webDriver.get(base_url + '#&date=%2000:00:00&page=' + str(current_page))
    time.sleep(10)
    current_page += 1

    #csv 파일에 데이터 입력
    if len(news_urls) != 0:
        csv_input_length = len(news_urls) - news_column
        for i in range(csv_input_length):
            append_csv(news_column, todayTime, news_companys[news_column], news_titles[news_column], news_urls[news_column])
            news_column += 1

    if current_page >= 50: break

f.close()