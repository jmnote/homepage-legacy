#!/usr/bin/env python3
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


class Repos(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_heading = False
        self.in_row = False
        self.group = None
        self.groups = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h3':
            self.in_heading = True
        elif tag == 'tr':
            self.in_row = True
        elif tag == 'a':
            url = urlparse(attrs.get('href', ''))
            parts = url.path.strip('/').split('/')
            if url.netloc != 'github.com':
                return
            if self.in_heading and len(parts) == 1 and parts[0] in ('jmnote', 'mailapi'):
                self.group = parts[0]
                if self.group in self.groups:
                    raise ValueError(f'duplicate group: {self.group}')
                self.groups[self.group] = []
            elif self.in_row and self.group and len(parts) == 2 and parts[0] == self.group:
                self.groups[self.group].append(parts[1])

    def handle_endtag(self, tag):
        if tag == 'h3':
            self.in_heading = False
        elif tag == 'tr':
            self.in_row = False


parser = Repos()
parser.feed(Path(sys.argv[1]).read_text(encoding='utf-8'))
if list(parser.groups) != ['jmnote', 'mailapi']:
    sys.exit('Missing or incorrectly ordered repository groups')
for group, repos in parser.groups.items():
    if not repos:
        sys.exit(f'No repositories found for {group}')
    if repos != sorted(repos, key=str.lower):
        sys.exit(f'{group} repositories are not sorted alphabetically: {repos}')
print('Repo order is valid.')
