# coding=utf-8
import requests

url = "http://localhost:7777/upload"
path = "C:\\Users\\Administrator\\Desktop\\video1_0.jpg"
print(path)
files = {'file': open(path, 'rb')}

# files = [('file1', ('test.txt', open('test.txt', 'rb'))),
#          ('file2', ('test.png', open('test.png', 'rb')))]
# r = requests.post(url, files=files)

headers = {"filename": "video1_0.jpg"}
r = requests.post(url, files=files, headers=headers)
# print(r.url)
# print(r.text)
