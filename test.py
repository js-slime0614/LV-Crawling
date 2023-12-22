import json

sample = []

sample.append({'name': '이름', 'content': '법률내용'})

print(sample)

with open('./현행법령.json', 'w', encoding='UTF-8-sig') as f:
    json.dump(sample, f, ensure_ascii=False, indent=4)