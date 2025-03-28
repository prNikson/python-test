import argparse
from sock import Request


parser = argparse.ArgumentParser(description="Explanation")
parser.add_argument('send', type=str, help='Sender number')
parser.add_argument('recip', type=str, help='Recipient number')
parser.add_argument('mes', type=str, help='Message')

if __name__ == "__main__":
    args=parser.parse_args()
    req = Request(args.send, args.recip, args.mes)
    req.post_request()