import sys
import os
import yaml
from argparse import ArgumentParser
from tagshell.version import version
from tagshell.core import TagShell, TagManager

class TagShellCli(object):
    def __init__(self):
        description = 'parallel remote shell execution and inventory utility'

        parser = ArgumentParser(version=version, description=description)
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

        config = self.read_config(args.config_file)

        tagfile = os.path.expanduser(config['tag_file'])
        self.tagman = TagManager(tagfile)

        if args.l:
            self.list_all()
            sys.exit(0)

        if not args.tags and not args.not_tags:
            print('you must specify at least one -nt or -t option')
            sys.exit(1)

        nodes = self.tagman.get(tags=args.tags, exclude_tags=args.not_tags)

        if not nodes:
            print('no nodes found to execute against')
            sys.exit(1)

        if args.b:
            TagShell(args.command, nodes, config, confirm=False)
        else:
            TagShell(args.command, nodes, config)

    def list_all(self):
        all_tags = self.tagman.all_tags()
        print('All Tags (%d):' % len(all_tags))
        for tag in all_tags:
            print('  %s' % tag)

        all_hosts = self.tagman.all_hosts()
        print('All Hosts (%d):' % len(all_hosts))
        for host in all_hosts:
            print('  %s' % host)

    @staticmethod
    def read_config(path):
        try:
            with open(path, 'r') as f:
                return yaml.load(f)
        except Exception as ex:
            print('unable to read config %s\n%s' % (path, ex))
            sys.exit(1)

def main():
    cli = TagShellCli()
