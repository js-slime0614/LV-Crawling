import requests
import json
import xml.etree.ElementTree as ET
import csv
import re

to_crawling_jo_num = 931

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
# email @ 뒤 제외, 민법내 조 
def crawling_law_from_civil(user_email, jo_num):
    api = send_api("OC=" + user_email + "&target=law&type=XML&ID=001706&JO=" + str(jo_num), "GET", "service")
    print("%r" % api)
    root = re.findall('CDATA.*]', api)
    print("%r" % root)
    return_data = ''
    for content in root:
        content = content.replace('CDATA', '')
        content = content.replace('[', '')
        content = content.replace(']', '')
        return_data = return_data + ' ' + content
    print(return_data)
    append_csv(return_data)
    return return_data

# 데이터 csv 파일로 저장
f = open('민법' + str(to_crawling_jo_num) +'조항.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
def append_csv(append_string):
    wr.writerow([append_string])
   
data = crawling_law_from_civil('parkjs0052','0' + str(to_crawling_jo_num) + '00') 
f.close()
