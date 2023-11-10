import requests
import json
import xml
import xml.etree.ElementTree as ET

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
        print("response text %r" % response.text)
        return response.text
    except Exception as ex:
        print(ex)
        
# 호출 예시
api = send_api("OC=parkjs0052&target=law&type=XML&ID=001706&JO=083400", "GET", "service")
"djEJgrp qhauscka wjswodrkxdkTekdnfl godqhrgks skskfdp dnffuTejs akfeh aksgdkTdj rlfdjTejs tlrksdmf wlzuwnjTes sjdi sjfmf sjantkfkdgotj rmrp ajfdjwlrp gksrjfRk djfltnrgks sowkfahtdlsrk tkfkddl tlrdjTekrh thfwlrgl akfgoeheho rktmaEnlsms tjffpadl sprp~ dhsrjfkrh skqhek whgdmstkfkadl sjdprp todrlsrjfkrh ekfmsvldrPrpTwl dnflsdksakwsmsekrh wlfflrp emfdjTdj slakadl Ejskrksgnfh ghrtlsk dnflrk rhoscksgdms tlwjfdp akssk wkfgownjTekausdms dnflwhrmadms ekfmfRk ghdndnn sjfmf sjantkfkdgotj rmrp ajfdjwlrpgksrjfRK cjfdldjqtsms sodyrtladlsrk tkfkddl tlrdjTekrh thfwlrgl akfgoeheho rktmaEnlsms tjffpadl sorp dhsrjfkrh skqhek whgdmstkfkadl sjdprp todrlsrjfkrh dkclaRkakgehfhr cnlgo dlwdmfu skfakdrkEMfueh skadkdlTsmssj skqhekej djelrk whgdktj Ejsksrjsl dlwdjqhfu goqhkeh aldnj sorkwhaej wkfsktj tjdrhdgkfEoWma sldkvdptj qhfrp rmEosjs ghffh dlrlfmf"

root = ET.fromstring(api)
