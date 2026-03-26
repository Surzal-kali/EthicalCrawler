import textwrap
import asyncio
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import cli.main

PROG_NAME = "PROG"
DEFAULT_KEYWORD = "demo"
KEYWORD_PROMPT = (
    f"Please enter the keyword you want to search for, default ({DEFAULT_KEYWORD}): "
)
WELCOME_MESSAGE = (
    "\nWelcome to EthicalCrawler! This tool is designed to demonstrate how to use "
    "Python for OSINT gathering in a playful yet invasive way. Please follow the prompts to get started.\n"
)


def build_parser() -> ArgumentParser:
    return ArgumentParser(
        prog=PROG_NAME,
        formatter_class=RawDescriptionHelpFormatter,
        description=HELP_TEXT,
    )


def show_startup_message() -> None:
    parser = build_parser()
    parser.print_help()
    print(WELCOME_MESSAGE)


def get_keyword() -> None:
    keyword = input(KEYWORD_PROMPT).strip()
    key = keyword.strip()
    return key or DEFAULT_KEYWORD


def startup() -> None:
    show_startup_message()
    get_keyword()


if __name__ == "__main__":
    asyncio.run(cli.main.main())