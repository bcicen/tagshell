#!/usr/bin/env python # coding: utf-8
import sys,os
from argparse import ArgumentParser
#from . import __version__
from core import TagShell, TagManager

__version__ = "0.1.0"

def main():
    pwd = os.getcwd()

    parser = ArgumentParser(description='execute, in parallel, a given command against \
            nodes matching given tags from pre-built yaml file',version=__version__)
    parser.add_argument('-b', action='store_true', help='batch mode. supress asking for \
            confirmation and immediately execute')
    parser.add_argument('-t', dest='tags', type=str, action='append', default=[], 
            help='tag to match. can be specified multiple times')
    parser.add_argument('-nt', dest='not_tags', type=str, action='append', default=[],  
            help='tag to NOT match. can be specified multiple times ')
    parser.add_argument('-f', dest='tagsfile', help='path to tags file store in yaml format',
            default=pwd + '/tags.yaml')
    parser.add_argument('command', help='command to execute')

    args = parser.parse_args()
    if not args.tags:
        print('you must specify the -t option')
        sys.exit(1)

    t = TagManager(args.tagsfile)

    nodes = [ node for node in t.get(tags=args.tags,exclude_tags=args.not_tags) ] 

    if not nodes:
        print('no nodes found to execute against')
        sys.exit(1)

    if args.b:
       TagShell(args.command,nodes,confirm=False)
    else:
       TagShell(args.command,nodes)

if __name__ == '__main__':
    main()
