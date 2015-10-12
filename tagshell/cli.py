import sys,os,yaml
from argparse import ArgumentParser
from . import __version__
from core import TagShell, TagManager

def main():
    pwd = os.getcwd()
    description = 'parallel remote shell execution and inventory utility'

    parser = ArgumentParser(version=__version__, description=description)

    parser.add_argument('-c',
            dest='config_file',
            help='path to tagshell config file',
            default=os.path.expanduser('~/.tagshell/config.yaml'))

    parser.add_argument('-b',
            action='store_true',
            help='batch mode. supress confirmation and immediately execute')

    parser.add_argument('-t',
            dest='tags',
            type=str,
            default=[],
            action='append',
            help='tag to match. can be specified multiple times')

    parser.add_argument('-nt',
            dest='not_tags',
            type=str,
            action='append',
            default=[],
            help='tag to NOT match. can be specified multiple times')

    parser.add_argument('-l',
            action='store_true',
            help='list all available tags and inventory hosts')

    parser.add_argument('command', nargs='?', help='command to execute')

    args = parser.parse_args()

    try:
        with open(args.config_file,'r') as f:
            config = yaml.load(f)
    except Exception as ex:
        print('unable to open config file %s\n%s' % (args.config_file, ex))
        sys.exit(1)

    tagfile = os.path.expanduser(config['tag_file'])

    tagman = TagManager(tagfile)

    if args.l:
        all_tags = tagman.all_tags()
        print('All Tags (%d):' % len(all_tags))
        for tag in all_tags:
            print('  %s' % tag)

        all_hosts = tagman.all_hosts()
        print('All Hosts (%d):' % len(all_hosts))
        for host in all_hosts:
            print('  %s' % host)

        sys.exit(0)

    if not args.tags and not args.not_tags:
        print('you must specify at least one -nt or -t option')
        sys.exit(1)

    nodes = tagman.get(tags=args.tags,exclude_tags=args.not_tags)

    if not nodes:
        print('no nodes found to execute against')
        sys.exit(1)

    if args.b:
       TagShell(args.command,nodes,config,confirm=False)
    else:
       TagShell(args.command,nodes,config)

if __name__ == '__main__':
    main()
