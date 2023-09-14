from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
from datetime import datetime

#드라이버 지정
webDriver = webdriver.Chrome()

#사이트 열기
webDriver.get('https://www.easylaw.go.kr/CSP/OnhunqueansLstRetrieve.laf?&search_put=')
webDriver.implicitly_wait(10) #로딩 끝날때까지 10초 기다리기

#데이터 csv 저장
f = open('백문백답.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)

def append_csv(category, question, answer):
    wr.writerow([category, question, answer])
    print('csv 요소 삽입완료')

#카테고리 선언
categories = []
category_num = 1

while(1) :

    #csv 파일에 저장할 요소 리스트 선언
    answers = []
    questions = []

    #크롤링하기 위해 카테고리 클릭 및 categories 배열에 카테고리명 append
    cliked_category = webDriver.find_element(By.CSS_SELECTOR,'#ast_' + str(category_num))
    categories.append(cliked_category.text)
    cliked_category.click()
    time.sleep(2)

    while(1) :

        #백문백답 현재 페이지의 Question append
        current_page_questions = webDriver.find_elements(By.CSS_SELECTOR, 'div > div.ttl > a')
        for append_questions in current_page_questions:
            questions.append(append_questions.text)

        #백문백답 현재 페이지의 Answer append
        current_page_answers = webDriver.find_elements(By.CSS_SELECTOR, 'div > div.ans > p')
        for append_answers in current_page_answers:
            answers.append(append_answers.text)

        #다음페이지로 넘어가는 btn 클릭
        try:
            btn_next = webDriver.find_element(By.CSS_SELECTOR, '#Ak_contents > div.vote_list > div.paging > a.nex1')
            btn_next.click()
        except:
            break

    #저장한 데이터 csv 파일에 저장
    if len(questions) != 0:
        csv_input_length = len(questions)
        for i in range(csv_input_length):
            append_csv(categories[category_num - 1],questions[i],answers[i])
    if category_num >= 18:
        break
    else:
        category_num += 1

f.close()