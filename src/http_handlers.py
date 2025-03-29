import json
import re
from typing import Self


class HTTPRequest:

    def __init__(self, body: dict[str, str], address: str, headers: dict[str, str]):
        self.body = body
        self.headers = headers
        self.address = address

    def to_bytes(self) -> bytes:
        point = self.address.split('/')[-1]
        self.body = json.dumps(self.body)
        self.headers = json.dumps(self.headers)
        request = f"POST /{point} HTTP/1.1\r\n"
        host = f"Host: {self.address}\r\n"
        # content_type = "Content-Type: application/json\r\n"
        # content_length = f"Content-Length: {str(len(self.body))}\r\n"
        # auth = f"Authorization: Basic {self.credentials}\r\n\r\n"
        request += "".join([host, self.headers, self.body])
        return request.encode('utf-8')
    
    @classmethod
    def from_bytes(cls, req: bytes) -> Self:
        req = (req.decode()).split('\r\n')
        body = json.loads(req[-1])
        address = re.split(r'Host:', req[1])[-1]
        hed = [i.split(":") for i in req[2:5]]
        headers = {key.strip(): value.strip() for key, value in hed}
        return cls(body, address, headers)


class HTTPResponse:
    
    def __init__(self, code, body):
        self.code = code
        # self.headers = headers
        self.body = body

    def to_bytes(self) -> bytes:
        code = f"HTTP/1.1 {self.code}"
        return (self.code + '\r\n\r\n' + self.body).encode()

    @classmethod
    def from_bytes(cls, resp: bytes) -> Self:
        response = (resp.decode()).split('\r\n')
        # print(response)
        code = (re.split(r'HTTP/1.1', response[0])[-1]).strip()
        body = json.loads(response[-1])
        # response = [i.split(':') for i in response[5:7]]
        # headers = {key.strip(): value.strip() for key, value in response}
        return cls(code, body)

a = HTTPResponse.from_bytes(b'HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Headers: *\r\nAccess-Control-Allow-Credentials: true\r\nAccess-Control-Expose-Headers: *\r\nContent-type: application/json\r\nContent-Length: 42\r\nDate: Sat, 29 Mar 2025 11:01:42 GMT\r\nConnection: keep-alive\r\nKeep-Alive: timeout=5\r\n\r\n{"status":"success","message_id":"123456"}')
print(vars(a))