import asyncio
import base64
import json
import toml
from http_handlers import *
import logging


filename = 'spec.toml'
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="a",
                    format="%(asctime)s %(levelname)s\n%(message)s\n")

class Request:

    def __init__(self, send: str, recip: int, mes: str) -> None:
        self.send = send
        self.recip = recip
        self.message = mes
    
    async def __prepare_request(self) -> int:
        self.body = {
            "sender": self.send,
            "recipient": self.recip,
            "message": self.message
        }
        self.body = json.dumps(self.body)
        if await self.__get_info_from_toml():

            credentials = base64.b64encode(f"{self.login}:{self.passwd}".encode()).decode()
            self.headers = {
                "Content-Type": "application/json",
                "Content-Length": f"{str(len(self.body))}",
                "Authorization": f"Basic {credentials}"
            }
            return 1
        return 0

    async def __get_info_from_toml(self) -> int:
        try:
            with open(filename, "r") as file:
                data = toml.load(file)
                self.login, self.passwd = data['user']['login'], data['user']['password']
                server = data['server']
                self.address = server['address']
                self.port = server['port']
        except FileNotFoundError:
            logging.error(f"Error: File {filename} not found")
            return 0
        except KeyError:
            logging.error("Error: The field(s) don`t parse from file")
            return 0
        return 1

    async def post_request(self) -> None:
        if await self.__prepare_request():
            address = re.search(r'^(https?:\/\/)?([^\/?:]+)(:\d+)?(\/|$)', self.address)
            address = address.group(2)
            reader, writer = await asyncio.open_connection(address, self.port)
            HTTPreq = HTTPRequest(self.body, self.address, self.headers)
            writer.write(HTTPreq.to_bytes())
            await writer.drain()
            response = await reader.read(4096)
            HTTPresp = HTTPResponse.from_bytes(response)
            print(HTTPresp.code, HTTPresp.body)
            writer.close()

            logging.info(f"Host:{self.address} Port: {self.port}\nsend:{self.send}\n" +\
                f"recipient:{self.recip}\nmessage:{self.message}\n" +
                HTTPresp.code + "\n" + json.dumps(HTTPresp.body))