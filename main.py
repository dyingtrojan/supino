import argparse
from misc import title_text
import chat
from config import setup

title_text.show_title()
parser = argparse.ArgumentParser(description="An AI agent app.")
subparser = parser.add_subparsers(dest="mode", required=True, help="Mode for SUPINO")

parser_start = subparser.add_parser("start", help="Starts SUPINO")
parser_start.set_defaults(function=chat.start_chat)

parser_settings = subparser.add_parser("setup", help="Starts the setup program for SUPINO")
parser_settings.set_defaults(function=setup.run_setup)

args = parser.parse_args()

if __name__ == "__main__":
    match args.mode:
        case "start":
            chat.start_chat()