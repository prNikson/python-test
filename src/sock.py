import socket
import base64
import json
import toml
from http_handlers import *
import logging


filename = 'spec.toml'
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="a",
                    format="%(asctime)s\n%(levelname)s\n%(message)s\n")

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
            logging.error(f"Error: File {filename} not found")
            return 0

    def post_request(self) -> None:
        if self.prepare_request():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.address, self.port))
                sock.sendall(HTTPRequest.to_bytes(self.request))
                data = sock.recv(4096)
                HTTPResponse.from_bytes(data)

                print(HTTPResponse.code)
                print(HTTPResponse.body)
                logging.info(f"Host:{self.address}:{self.port}/{self.point}\nsend:{self.send}\n" +\
                f"recipient:{self.recip}\nmessage:{self.message}\n" +
                HTTPResponse.code + "\n" + json.dumps(HTTPResponse.body))
