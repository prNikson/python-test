import socket
import base64
import json
import toml
from http_handlers import *
import logging
from exception import ParseFileError


filename = 'spec.toml'
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="a",
                    format="%(asctime)s\n%(levelname)s\n%(message)s\n")

class Request:

    def __init__(self, send: str, recip: int, mes: str) -> None:
        self.send = send
        self.recip = recip
        self.message = mes
    
    def __prepare_request(self) -> int:
        self.body = {
            "sender": self.send,
            "recipient": self.recip,
            "message": self.message
        }
        self.body = json.dumps(self.body)
        if self.__get_info_from_toml():

            credentials = base64.b64encode(f"{self.login}:{self.passwd}".encode()).decode()
            self.headers = {
                "Content-Type": "application/json",
                "Content-Length": f"{str(len(self.body))}",
                "Authorization": f"Basic {credentials}"
            }
            return 1
        return 0

    def __get_info_from_toml(self) -> int:
        try:
            with open(filename, "r") as file:
                data = toml.load(file)
        except FileNotFoundError:
            logging.error(f"Error: File {filename} not found")
            return 0
        try:
            self.login, self.passwd = data['user']['login'], data['user']['password']
            server = data['server']
            self.address = server['address']
            self.port = server['port']
        except Exception:
            logging.error("Error: The field(s) don`t parse from file")
            return 0
        return 1

    def post_request(self) -> None:
        if self.__prepare_request():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                HTTPreq = HTTPRequest(self.body, self.address, self.headers)
                address = re.search(r'^(https?:\/\/)?([^\/?:]+)(:\d+)?(\/|$)', self.address)
                address = address.group(2)
                sock.connect((address, self.port))
                sock.sendall(HTTPreq.to_bytes())
                data = sock.recv(4096)
                HTTPresp = HTTPResponse.from_bytes(data)

                print(HTTPresp.code)
                print(HTTPresp.body)
                logging.info(f"Host:{self.address} Port:{self.port}\nsend:{self.send}\n" +\
                f"recipient:{self.recip}\nmessage:{self.message}\n" +
                HTTPresp.code + "\n" + json.dumps(HTTPresp.body))
