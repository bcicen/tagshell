import sys,os,yaml
from argparse import ArgumentParser
from . import __version__
from core import TagShell, TagManager

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
    parser.add_argument('-c', dest='config_file', help='tagshell config file',
            default=os.path.expanduser('~/.tagshell'))
    parser.add_argument('command', help='command to execute')

    args = parser.parse_args()

    if os.path.isfile(args.config_file) and os.access(args.config_file, os.R_OK):
        with open(args.config_file,'r') as f:
            config = yaml.load(f)
    else:
        print('unable to open config file %s' % args.config_file)
        sys.exit(1)

    if not args.tags and not args.not_tags:
        print('you must specify at least one -nt or -t option')
        sys.exit(1)

    tagfile = config['tag_file'] 

    t = TagManager(tagfile)

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
