import requests
import json
import xml.etree.ElementTree as ET
import csv
import re

to_crawling_jo_num = 931
search_word = ""
data_num = []

def send_api(path, method, type):
    API_HOST1 = "http://www.law.go.kr/DRF/lawSearch.do?"
    API_HOST2 = "http://www.law.go.kr/DRF/lawService.do?"
    if type == "service":
        url = API_HOST2 + path
    else: 
        url = API_HOST1 + path
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    body = {
        
    }

    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
        print("response status %r" % response.status_code)
        # print("response text %r" % response.text)
        return response.text
    except Exception as ex:
        print(ex)

# 호출 예시
# email @ 
def crawling_law(user_email, num_variable, search_service):
    if search_service == 'search':
        api = send_api("OC=" + user_email + "&target=expc&type=XML&display=100&page=" + str(num_variable), "GET", search_service)
    elif search_service == 'service':
        api = send_api("OC=" + user_email + "&target=expc&type=XML&ID=" + str(num_variable), 'GET', search_service)
    print("%r" % api)
    # root = re.findall('CDATA.*]', api)
    # print("%r" % root)
    # append_csv(return_data)
    if search_service == 'search':
        root = re.findall('<법령해석례일련번호>.*?</법령해석례일련번호>', api)
        for data in root:
            data_num.append(re.sub('<.*?>', '', data))
        print(data_num)
        return data_num
    elif search_service == 'service':
        root = ET.fromstring(api)
        name_of_expc = root.find("안건명")
        question_expc = root.find("질의요지")
        answer_expc = root.find("회답")
        expc_reason = root.find("이유")
        append_csv(name_of_expc.text, question_expc.text, answer_expc.text, expc_reason.text)

# 데이터 csv 파일로 저장
f = open(search_word + '법령해석례.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
def append_csv(name_of_expc, question_expc, answer_expc, expc_reason):
    name_of_expc = re.sub('<.*?>', '', name_of_expc)
    name_of_expc = re.sub('\n', '' , name_of_expc)
    
    try:
        question_expc = re.sub('<.*?>', '', question_expc)
        question_expc = re.sub('\n', '' , question_expc)
    except:
        question_expc = "질의요지"
    try:
        answer_expc = re.sub('<.*?>', '', answer_expc)
        answer_expc = re.sub('\n', '' , answer_expc)
    except:
        answer_expc = "회답"
    try:
        expc_reason = re.sub('<.*?>', '', expc_reason)
        expc_reason = re.sub('\n', '' , expc_reason)
    except:
        expc_reason = "이유"
    wr.writerow([name_of_expc, question_expc , answer_expc, expc_reason])

append_csv('안건명', '질의요지', '회답', '이유')
for page_num in range(1,78):
    data = crawling_law('parkjs0052', page_num, "search")
    print(page_num)

for crawl_data in data:
    crawling_law('parkjs0052', crawl_data, "service")

f.close()