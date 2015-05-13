# Tagshell

Execute ssh commands to multiple hosts in parallel based on host tags

## Installation
```bash
git clone https://github.com/bcicen/tagshell.git
cd tagshell/
python setup.py install
```

If this is your first time installing tagshell, a default configuration and tag file will be created in ~/.tagshell

## Usage
```bash
tagshell -t webservers -nt region1 "w"
```
Where **-t** designates the host tags to match and **-nt** designates tags to explictly not match. The above would execute the "w" command on all webservers and lb not in region1. **-t** and **-nt** options can both be specified multiple times for more granular matches. 

## Tag file 
Tagshell depends on a yaml file describing hosts and tags like:

```yaml
---
  hostname: host1.domain.com
  tags: [domain, lb, app1]
---
  hostname: host2.domain.com
  tags: [domain, webserver, app1]
```

## Config file
Default location of ~/.tagshell/config.yaml

Currently supports the following configuration options:
```
tag_file: path to host tags file
errdir: directory to log stderr
outdir: directory to log stdout.
```

## Options
```bash
  -h, --help      show this help message and exit
  -v, --version   show program's version number and exit
  -b              batch mode. supress asking for confirmation and immediately
                  execute
  -t TAGS         tag to match. can be specified multiple times
  -nt NOT_TAGS    tag to NOT match. can be specified multiple times
  -c CONFIG_FILE  tagshell config file
```
