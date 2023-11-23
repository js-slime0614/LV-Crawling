import xml.etree.ElementTree as ET
import requests
import re
import json
import csv

data_num = []

def send_api(path, method, type):
    API_HOST1 = "https://www.law.go.kr/DRF/lawSearch.do?"
    API_HOST2 = "https://www.law.go.kr/DRF/lawService.do?"
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
        # print("response status %r" % response.status_code)
        # print("response text %r" % response.text)
        print(url)
        return response.text
    except Exception as ex:
        print(ex)

def crawling_law(user_email, num_variable):
    api = send_api("OC=" + user_email + "&target=law&type=XML&search=1&display=100&page=" + str(num_variable), "GET", 'search')
    # print(api)
    # root = re.findall('CDATA.*?]', api)
    # print("%r" % root)
    # append_csv(return_data)
    root = re.findall('<법령ID>.*?</법령ID>', api)
    for data in root:
        data_num.append(re.sub('<.*?>', '', data))
    print(data_num)
    return data_num

for i in range(1, 54):
    lawID_list = crawling_law('parkjs0052', i)

def crawling_law_data(user_email, law_ID):
    api = send_api("OC=" + user_email + "&target=law&type=XML&ID=" + str(law_ID), "GET", 'service')
    # print(api)
    root = re.sub("\n", '' , api)
    root = re.sub("\t", '' , root)
    root = re.findall('<조문단위.*?</조문단위>', root)
    law_name_root = re.findall("<법령명_한글>.*?</법령명_한글>", api)
    law_name = re.sub("<.?법령명_한글>", '', law_name_root[0])
    #조문내용 항내용 호내용 담을 리스트
    law_content_data = []
    #조문내용, 항내용, 호내용 포함 크롤링
    for data in root:
        law_contents = []
        law_contents = re.findall('<..?내용>.*?</..?내용>', data)
        #조문내용 항내용 호내용 하나로 합치기
        # print(law_contents)
        temp = ""
        for i in range(len(law_contents)):
            law_contents[i] = re.sub('<..?내용>', '',  law_contents[i])
            law_contents[i] = clean_string(law_contents[i])
            # print(law_contents[i])
            temp = temp + law_contents[i]
        law_content_data.append(temp)
        # print(law_content_data)

    print(clean_string(law_name))
    for law_content in law_content_data:
        append_csv(clean_string(law_name), law_content)


#CDATA 부분 제거
def clean_string(string_data):
    return_data = re.sub("<!.CDATA.", '', string_data)
    return_data = re.sub("].*", "", return_data)
    return return_data
# 데이터 csv 파일로 저장
f = open('현행법령.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
def append_csv(law_name, law_content):
    wr.writerow([law_name, law_content])

append_csv("법령명", "법령조문내용")
for data in lawID_list:
    crawling_law_data('parkjs0052', data)

f.close()