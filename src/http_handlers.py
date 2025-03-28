from abc import ABC, abstractmethod
import json
import re


class HTTP(ABC):

    @abstractmethod
    def to_bytes(self, body):
        pass
    
    @abstractmethod
    def from_bytes(self, body):
        pass


class HTTPRequest(HTTP):

    def to_bytes(self, body: str) -> bytes:
        return body.encode('utf-8')        
    
    def from_bytes(self, body: bytes) -> None:
        pass


class HTTPResponse(HTTP):
    
    def __init__(self):
        self.code: str
        self.body: dict

    def to_bytes(self) -> None:
        pass
    
    def from_bytes(self, body: bytes) -> None:
        response = (body.decode()).split('\r\n')
        self.code = re.split(r'HTTP/1.1 ', response[0])[-1]
        self.body = json.loads(response[-1])