#!/usr/bin/env python

import argparse
import re

import betacode.conv
import lxml.etree

parser = argparse.ArgumentParser()
parser.add_argument('perseus', help='Name of perseus file to extract.')
args = parser.parse_args()

perseus_parser = lxml.etree.XMLParser(no_network=False)
with open(args.perseus) as f:
    tree = lxml.etree.parse(f, perseus_parser)

components = []
for node in tree.xpath('//p/*'):
    if node.tag != 'note':
        text = lxml.etree.tostring(node, method='text', encoding='unicode')
        if text is not None:
            components.append(text)
    else:
        text = node.tail
        if text is not None:
            components.append(text)

for component in components:
    component = component.strip()
    component = re.sub('\n{3,}', '\n\n', component)
    print(betacode.conv.beta_to_uni(component))
