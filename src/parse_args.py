import args
import argparse


data = args.load('spec.toml')

print(data)

parser = argparse.ArgumentParser(description="Explanation")
parser.add_argument('send', type=str, help='Sender number')
parser.add_argument('recip', type=str, help='Recipient number')
parser.add_argument('mes', type=str, help='Message')
args=parser.parse_args()
print(args)
