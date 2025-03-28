import socket
import base64
import json
import toml
from http_handlers import *
import logging


HTTPres = HTTPResponse()
HTTPreq = HTTPRequest()
filename = 'spec.toml'
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")

class Request:

    def __init__(self, send: str, recip: int, mes: str) -> None:
        self.send = send
        self.recip = recip
        self.message = mes
    
    def prepare_request(self) -> int:
        body = json.dumps({
            "sender": self.send,
            "recipient": self.recip,
            "message": self.message
        })
        if self.get_info_from_toml():

            credentials = base64.b64encode(f"{self.login}:{self.passwd}".encode()).decode()
            self.request = f"POST /{self.point} HTTP/1.1\r\n"
            host = f"Host: {self.address}:{self.port}/{self.point}\r\n"
            content_type= "Content-Type: application/json\r\n"
            content_length = f"Content-Length: {str(len(body))}\r\n"
            auth = f"Authorization: Basic {credentials}\r\n\r\n"
            self.request += "".join([host, content_type, content_length, auth, body])
            
            return 1
        return 0

    def get_info_from_toml(self) -> int:
        try:
            with open(filename, "r") as file:
                data = toml.load(file)
                self.login, self.passwd = data['user']['login'], data['user']['password']
                server = data['server']
                self.address = server['address']
                self.port = server['port']
                self.point = server['point']
            return 1
        except FileNotFoundError:
            print("Error: File not found")
            return 0

    def post_request(self) -> None:
        if self.prepare_request():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.address, self.port))
                sock.sendall(HTTPreq.to_bytes(self.request))
                data = sock.recv(4096)
                HTTPres.from_bytes(data)

                print(HTTPres.code)
                print(HTTPres.body)


a = Request("admin", "admin", "message")
a.post_request()


# HOST = "127.0.0.1"
# PORT=4010
# body = json.dumps({
#    "sender": "admin",
#   "recipient": "admin",
#    "message": "message"
# })
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     cred = (base64.b64encode("admin:admin".encode())).decode()
#     # body = "sender=admin&recipient=admin&message=admin\r\n"
#     mes = "POST /send_sms HTTP/1.1\r\n"
#     host = "Host: http://127.0.0.1:4010/send_sms\r\n"
#     content_type = "Content-Type: application/json\r\n"
#     content_length="Content-Length: " + str(len(body)) + "\r\n"
#     auth=f"Authorization: Basic {cred}\r\n\r\n"
#     mes += (host + content_type + content_length + auth + body)
#     s.sendall(mes.encode())
#     print(mes.encode())
#     data = s.recv(1024)
#     # print(data)

