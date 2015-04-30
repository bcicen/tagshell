# Tagshell

Execute ssh commands to multiple hosts in parallel based on host tags

## Usage

Tagshell depends on a hosts.yaml file like:

```
---
  hostname: host1.domain.com
  tags: [domain, lb, app1]
---
  hostname: host2.domain.com
  tags: [domain, webserver, app1]
```

and provides the following options:
```
  -b             batch mode. supress asking for confirmation and immediately
                 execute
  -t TAGS        tag to match. can be specified multiple times
  -nt NOT_TAGS   tag to NOT match. can be specified multiple times
  -f TAGSFILE    path to tags file store in yaml format
```
