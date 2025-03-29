from abc import ABC, abstractmethod
import json
import re


class HTTP(ABC):

    @classmethod
    @abstractmethod
    def to_bytes(cls, body):
        pass
    
    @classmethod
    @abstractmethod
    def from_bytes(cls, body):
        pass


class HTTPRequest(HTTP):

    @classmethod
    def to_bytes(cls, body: str) -> bytes:
        return body.encode('utf-8')    
    
    @classmethod
    def from_bytes(cls, body: bytes) -> None:
        pass


class HTTPResponse(HTTP):
    
    code: str = ""
    body: dict = ""

    @classmethod
    def to_bytes(cls) -> None:
        pass

    @classmethod
    def from_bytes(cls, body: bytes) -> None:
        response = (body.decode()).split('\r\n')
        cls.code = re.split(r'HTTP/1.1 ', response[0])[-1]
        cls.body = json.loads(response[-1])