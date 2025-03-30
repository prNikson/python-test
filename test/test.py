import pytest
import sys
sys.path.append('src')
from http_handlers import *

class HTTPResp:
    def data_from_bytes(self):
        resp = b'HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Headers: *\r\nAccess-Control-Allow-Credentials: true\r\nAccess-Control-Expose-Headers: *\r\nContent-type: application/json\r\nContent-Length: 42\r\nDate: Sun, 30 Mar 2025 16:18:41 GMT\r\nConnection: keep-alive\r\nKeep-Alive: timeout=5\r\n\r\n{"status":"success","message_id":"123456"}'
        response = HTTPResponse.from_bytes(resp)
        assert response.code == '200 OK'
        assert response.body == {"status":"success","message_id":"123456"}

    def data_to_bytes(self):
        response = HTTPResponse('200 OK', {"status": "success", "message_id": "123456"})
        byte_string = b"HTTP/1.1 200 OK\r\n\r\n{'status': 'success', 'message_id': '123456'}"
        assert HTTPResponse.to_bytes(response) == byte_string
    
    def status_404(self):
        resp = b'HTTP/1.1 404 Not Found\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Headers: *\r\nAccess-Control-Allow-Credentials: true\r\nAccess-Control-Expose-Headers: *\r\ncontent-type: application/problem+json\r\nContent-Length: 201\r\nDate: Sun, 30 Mar 2025 16:28:51 GMT\r\nConnection: keep-alive\r\nKeep-Alive: timeout=5\r\n\r\n{"type":"https://stoplight.io/prism/errors#NO_PATH_MATCHED_ERROR","title":"Route not resolved, no path matched","status":404,"detail":"The route /127.0.0.1 hasn\'t been found in the specification file"}'
        response = HTTPResponse.from_bytes(resp)
        assert response.code == '404 Not Found'
        assert response.body == {"type": "https://stoplight.io/prism/errors#NO_PATH_MATCHED_ERROR", "title": "Route not resolved, no path matched", "status": 404, "detail": "The route /127.0.0.1 hasn\'t been found in the specification file"}

class HTTPReq:

    def data_to_bytes(self):
        request = HTTPRequest(
            body={"k1": "v1", "k2": "v2"},
            address="http://127.0.0.1/send_sms",
            headers = {"Content-Type": "application/json", "Authorization": "Basic"},
        )
        byte_string = b'POST /send_sms HTTP/1.1\r\nHost: http://127.0.0.1/send_sms\r\nContent-Type: application/json\r\nAuthorization: Basic\r\n\r\n{"k1": "v1", "k2": "v2"}'
        assert request.to_bytes() == byte_string

    def data_from_bytes(self):
        data = b'POST /send_sms HTTP/1.1\r\nHost: http://127.0.0.1/send_sms\r\nContent-Type: application/json\r\nAuthorization: Basic\r\n\r\n{"k1": "v1", "k2": "v2"}'
        request = HTTPRequest.from_bytes(data)
        assert request.address == "http://127.0.0.1/send_sms"
        assert request.headers == {'Content-Type': 'application/json', 'Authorization': 'Basic'}
        assert request.body == {"k1": "v1", "k2": "v2"}