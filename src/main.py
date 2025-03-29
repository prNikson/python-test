import argparse
import asyncio
from async_sock import Request

parser = argparse.ArgumentParser(description="Explanation")
parser.add_argument('send', type=str, help='Sender number')
parser.add_argument('recip', type=str, help='Recipient number')
parser.add_argument('mes', type=str, help='Message')
args=parser.parse_args()


async def main(send: str, recip: str, mes: str) -> None:
    a = Request(str(send), str(recip), str(mes))
    await a.post_request()
    
if __name__ == "__main__":
    asyncio.run(main(args.send, args.recip, args.mes))