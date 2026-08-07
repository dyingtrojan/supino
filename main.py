import argparse
from misc import title_text
import chat

title_text.show_title()
parser = argparse.ArgumentParser(description="An AI agent app.")
parser.add_argument("start", help="Starts SUPINO")

args = parser.parse_args()

if args.start:
    chat.start_chat()