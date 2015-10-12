import os
import sys
import yaml
import logging
import ConfigParser

from psshlib import psshutil
from psshlib.manager import Manager, FatalError
from psshlib.task import Task

log = logging.getLogger('tagshell')

class TagManager(object):
    def __init__(self, tagsfile):
        tagsfile = os.path.expanduser(tagsfile)
        if not os.path.isfile(tagsfile):
            raise Exception('unable to open tags file %s', (tagsfile))

        with open(tagsfile,'r') as f:
            self.nodes = [ n for n in yaml.load_all(f) ]
   
    def all_tags(self):
        return list(set([ t for n in self.nodes for t in n.get('tags') ]))

    def all_hosts(self):
        return list(set([ n['hostname'] for n in self.nodes ]))

    def get(self,attribute='hostname',tags=[],exclude_tags=[]):
        """
        Return list of nodes, filtered by tags or exclude tags
        """
        node_lists = []

        for tag in tags:
            node_lists.append([ n[attribute] for n in self.nodes if tag in n['tags']])

        for tag in exclude_tags:            
            node_lists.append([ n[attribute] for n in self.nodes if tag not in n['tags']])

        if len(node_lists) == 0:
            return None

        return set(node_lists[0]).intersection(*node_lists[1:])

class TagShell(object):
    """
    TagShell class is a wrapper around the psshlib package.
    params:
    cmd - string of command to run
    nodes - list of hosts to execute against
    config - dict of config values to override default
    """
    def __init__(self, cmd, nodes, config, confirm=True):
        self.opts = TagShellConfig(config)
        self.opts.cmdline = cmd

        log.info('executing %s against %s' % (cmd,nodes))
        self.color = TermColors()

        print('executing "%s" against:' % cmd)
        [ self.color.red(node) for node in nodes ]

        if confirm:
           self._confirm()

        opts = self.opts
        
        logdirs = [ opts.outdir,opts.errdir ]
        [ os.makedirs(d) for d in logdirs if not os.path.exists(d) ] 

        self.manager = Manager(opts)
        for node in nodes:
            t = self._maketask(node,cmd)
            self.manager.add_task(t)
        try:
            statuses = self.manager.run()
        except FatalError:
            sys.exit(1)

        if min(statuses) < 0:
            # At least one process was killed.
            sys.exit(3)
        elif any(x==255 for x in statuses):
            sys.exit(4)
        for status in statuses:
            if status != 0:
                sys.exit(5)

    def _maketask(self,node,cmd):
        """
        assemble command and return a pssh task object suitable
        for submitting to psshlib manager
        """
        opts = self.opts
        cmd = ['ssh', node, '-o', 'NumberOfPasswordPrompts=1',
                '-o', 'SendEnv=PSSH_NODENUM PSSH_HOST']
        if opts.options:
            for opt in opts.options:
                cmd += ['-o', opt]
        if opts.user:
            cmd += ['-l', opts.user]
        if opts.port:
            cmd += ['-p', opts.port]
        if opts.cmdline:
            cmd.append(opts.cmdline)
        log.debug('full command compiled as: %s' % ' '.join(cmd))

        return Task(node,opts.port,opts.user,cmd,opts,opts.stdin)

    def _confirm(self):
        s = raw_input('confirm?(yes/no):')
        if s != 'yes':
            print('execution aborted')
            sys.exit(1)

class TagShellConfig(TagShell):
    defaults = {
        'send_input': None,
        'par': 200,
        'verbose': False,
        'inline_stdout': False,
        'extra': None,
        'askpass': None,
        'errdir': os.path.expanduser('~/.tagshell/logs/'),
        'outdir': os.path.expanduser('~/.tagshell/logs/'),
        'print_out': True,
        'options': [ 'BatchMode=yes' ],
        'host_files': None,
        'user': None,
        'timeout': 300,
        'inline': None,
        'host_strings': None,
        'stdin': None,
        'port': None,
    }
    def __init__(self, config):
        #override defaults with any provided config
        self.defaults.update(config)
        for k in self.defaults:
            self.__setattr__(k,self.defaults[k])

        log.debug('loaded config as:\n%s' % yaml.dump(self.defaults))

class TermColors:
    _red = '\033[91m'
    _whitebg = '\033[107m'
    _green = '\033[92m'
    _yellow = '\033[93m'
    _blue = '\033[94m'
    _magenta = '\033[95m'
    _cyan = '\033[96m'
    _end = '\033[0m'
    def red(self,msg):
        print(self._red + msg + self._end)
    def redonwhite(self,msg):
        print(self._red + self._whitebg + msg + self._end)
    def green(self,msg):
        print(self._green + msg + self._end)
    def yellow(self,msg):
        print(self._yellow + msg + self._end)
    def blue(self,msg):
        print(self._blue + msg + self._end)
    def magenta(self,msg):
        print(self._magenta + msg + self._end)
    def cyan(self,msg):
        print(self._cyan + msg + self._end)
