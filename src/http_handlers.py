import json
import re
from typing import Self


class HTTPRequest:

    def __init__(self, body: str, address: str, headers: dict[str, str]):
        self.body = body
        self.headers = headers
        self.address = address

    def to_bytes(self) -> bytes:
        point = self.address.split('/')[-1]
        request = f"POST /{point} HTTP/1.1\r\n"
        host = f"Host: {self.address}\r\n"
        gen = [f"{k}: {v}" for k, v in self.headers.items()]
        request += "".join([host, "".join(gen), self.body])
        print(request)
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
        self.body = body

    def to_bytes(self) -> bytes:
        code = f"HTTP/1.1 {self.code}"
        return (code + '\r\n\r\n' + self.body).encode()

    @classmethod
    def from_bytes(cls, resp: bytes) -> Self:
        response = (resp.decode()).split('\r\n')
        code = (re.split(r'HTTP/1.1', response[0])[-1]).strip()
        body = json.loads(response[-1])
        return cls(code, body)