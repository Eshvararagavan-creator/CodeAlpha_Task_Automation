"""Small file-automation utilities for the CodeAlpha internship task."""

import argparse
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import urlopen

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def move_jpg_files(source, destination):
    """Move .jpg/.jpeg files from source into destination and return count."""
    source, destination = Path(source), Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    moved = 0
    for file in source.iterdir():
        if file.is_file() and file.suffix.lower() in {".jpg", ".jpeg"}:
            shutil.move(str(file), str(destination / file.name))
            moved += 1
    return moved


def extract_emails(input_file, output_file):
    """Extract unique email addresses from a text file and save them one per line."""
    text = Path(input_file).read_text(encoding="utf-8")
    emails = sorted(set(EMAIL_PATTERN.findall(text)))
    Path(output_file).write_text("\n".join(emails) + ("\n" if emails else ""), encoding="utf-8")
    return emails


class _TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.parts = []
    def handle_starttag(self, tag, attrs):
        self.in_title = tag.lower() == "title"
    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False
    def handle_data(self, data):
        if self.in_title:
            self.parts.append(data.strip())


def scrape_title(url):
    """Fetch a webpage and return its title."""
    with urlopen(url, timeout=10) as response:
        parser = _TitleParser()
        parser.feed(response.read().decode("utf-8", errors="replace"))
    return " ".join(part for part in parser.parts if part)


def main():
    parser = argparse.ArgumentParser(description="CodeAlpha file automation tools")
    subparsers = parser.add_subparsers(dest="command", required=True)
    move = subparsers.add_parser("move-jpg")
    move.add_argument("source")
    move.add_argument("destination")
    emails = subparsers.add_parser("extract-emails")
    emails.add_argument("input_file")
    emails.add_argument("output_file")
    title = subparsers.add_parser("scrape-title")
    title.add_argument("url")
    args = parser.parse_args()
    if args.command == "move-jpg":
        print(f"Moved {move_jpg_files(args.source, args.destination)} image(s).")
    elif args.command == "extract-emails":
        print(f"Extracted {len(extract_emails(args.input_file, args.output_file))} email(s).")
    else:
        print(scrape_title(args.url))


if __name__ == "__main__":
    main()
