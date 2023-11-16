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
# email @ 뒤 제외, 민법내 조 
def crawling_law(user_email, num_variable, search_service):
    if search_service == 'search':
        api = send_api("OC=" + user_email + "&target=prec&type=XML&search=1&display=100&page=" + str(num_variable), "GET", search_service)
    elif search_service == 'service':
        api = send_api("OC=" + user_email + "&target=prec&type=XML&ID=" + str(num_variable), 'GET', search_service)
    print("%r" % api)
    # root = re.findall('CDATA.*]', api)
    # print("%r" % root)
    # append_csv(return_data)
    if search_service == 'search':
        root = re.findall('<판례일련번호>.*?</판례일련번호>', api)
        for data in root:
            data_num.append(re.sub('<.*?>', '', data))
        print(data_num)
        return data_num
    elif search_service == 'service':
        root = ET.fromstring(api)
        number_of_prec = root.find("판례정보일련번호")
        prec_name = root.find("사건명")
        considering_prec = root.find("판시사항")
        prec_reason = root.find("판결요지")
        prec_reference = root.find("참조조문")
        prec_contents = root.find("판례내용")
        append_csv(number_of_prec.text, prec_name.text, considering_prec.text, prec_reason.text, prec_reference.text, prec_contents.text)


# 데이터 csv 파일로 저장
f = open(search_word + '판례.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
def append_csv(num_of_prec, name_of_prec, prec_consider, why_prec, reference, prec_contents):
    num_of_prec = re.sub('<.*?>', '', num_of_prec)
    num_of_prec = re.sub('\n', '' , num_of_prec)
    try:
        name_of_prec = re.sub('<.*?>', '', name_of_prec)
        name_of_prec = re.sub('\n', '' , name_of_prec)
    except:
        name_of_prec = "판시사항"
    try:
        prec_consider = re.sub('<.*?>', '', prec_consider)
        prec_consider = re.sub('\n', '' , prec_consider)
    except:
        prec_consider = "판시사항"
    try:
        why_prec = re.sub('<.*?>', '', why_prec)
        why_prec = re.sub('\n', '' , why_prec)
    except:
        why_prec = "판결요지"
    try:
        reference = re.sub('<.*?>', '', reference)
        reference = re.sub('\n', '' , reference)
    except:
        reference = "참조조문"
    try:
        prec_contents = re.sub('<.*?>', '', prec_contents)
        prec_contents = re.sub('\n', '' , prec_contents)
    except:
        print("실패")
    wr.writerow([num_of_prec, name_of_prec , prec_consider, why_prec, reference, prec_contents])

append_csv('판례일련번호', '사건명', '판시사항', '판결요지', '참조조문','판례내용')
for page_num in range(1,864):
    data = crawling_law('parkjs0052', page_num, "search")
    print(page_num)

for crawl_data in data:
    crawling_law('parkjs0052', crawl_data, "service")



f.close()