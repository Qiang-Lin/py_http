#! -*- coding:utf-8 -*-
import cgi
import http.server
import json
import os
# import urlparse
from http.server import HTTPServer

LOCAL_FOLDERS = [
    "C:\\Users\\Administrator\\Desktop"
]
BASE_URL = "http:\\localhost"
data = {'result': 'this is a result11111', 'test': 'this is a test'}
host = ('localhost', 7777)
data_json = json.dumps({'key1': 'value1', 'key2': 'value2'})  # dumps：将python对象解码为json数据


class WebRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("Request for '%s' received." % self.path)
        self.send_response(200)  # 返回报文
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        enc = "UTF-8"
        path = str(self.path)
        # 获取POST请求的一种方式，首先受到length，然后通过self.rfile里读出该长度的数据
        # length = int(self.headers["content-length"])  # 获取除头部后的请求参数的长度
        # datas = urllib.parse.parse_qs(self.rfile.read(length), keep_blank_values=1)  # 获取请求参数数据，请求数据为json字符串
        # print(datas)
        if path == "/data":
            # pass（可以添加对参数的逻辑处理）
            # 以下是返回报文
            self.send_response(200)  # 返回状态码
            self.send_header("Content-type", "text/html;charset=%s" % enc)  # 返回响应头内容
            self.end_headers()  # 返回响应头结束
            buf = {"status": 0,  # 返回包体数据
                   "data": {"filepath": "Data done"}}
            # 这里一定要加encode(),不然会报错，bytes<-> str转换的错,bytes和str的互转有三种方式，# s.encode(encoding="utf-8")
            self.wfile.write(json.dumps(buf).encode())  # 发送json格式的返回包体
        # 上传图片
        if path == "/upload":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'post',
                         'CONTENT_TYPE': self.headers['Content-Type']
                         }
            )
            datas = form['file'].value  # 获取上传文件内容
            fname = self.headers["filename"]
            fn = os.path.join("D:\\study\\", fname)  # 生成文件存储路径
            outf = open(fn, 'wb')  # 写打开文件
            outf.write(datas)  # 将接收到的内容写入文件
            outf.close()  # 关闭文件
            self.send_response(200)
            self.send_header("Content-type", "text/html;charset=%s" % enc)
            self.send_header("test", "This is test!")
            self.end_headers()
            buf = {"status": 0,
                   "data": {
                       "msg": "Upload done"}}

            self.wfile.write(json.dumps(buf).encode())


if __name__ == '__main__':
    try:
        server = HTTPServer(host, WebRequestHandler)
        print("Starting server, listen at: %s:%s" % host)
        server.serve_forever()
    except KeyboardInterrupt:
        print('shutdown server')
        server.socket.close()
