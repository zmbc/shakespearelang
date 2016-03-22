#! /usr/bin/env python

from shakespeare_parser import shakespeareParser
import argparse

argparser = argparse.ArgumentParser(description = "Run files in Shakespeare Programming Language.")
argparser.add_argument('filename', type=str, help="SPL file location")

args = argparser.parse_args()
filename = args.filename

if(filename):
    with open(filename, 'r') as f:
        text = f.read().replace('\n', ' ')

    parser = shakespeareParser(parseinfo=True)
    ast = parser.parse(text, rule_name='play')
    print(ast)