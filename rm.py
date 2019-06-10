#!/usr/bin/env python2

from __future__ import print_function
import seafileapi
import time
import sys

keep_days = 7
if len(sys.argv) > 1:
  keep_days = int(sys.argv[1])
  print('Day to keep: %s' % keep_days)

freed_size = 0
my_login = 'me@example.com'
my_password = 'asecret'
time_to_eternity = keep_days * 24 * 60 * 60

def list_dir(repo, path, indent=0):
  global freed_size
  seafdir = repo.get_dir(path)
  lst = seafdir.ls(force_refresh=True)
  for dirent in lst:
    file_age = (int(time.time())-dirent.mtime)
    if file_age > time_to_eternity and not dirent.isdir:
      print("   " * indent, dirent.name, dirent.size, 'age', file_age / 60/ 60/ 24)
      to_delete = repo.get_file(dirent.path)
      to_delete.delete()
      freed_size += dirent.size
    if dirent.isdir:
      list_dir(repo, dirent.path, indent+1)
      if dirent.num_entries == 0:
        print('-- Empty dir: ', dirent.path)
        to_delete = repo.get_dir(dirent.path)
        to_delete.delete()

client = seafileapi.connect('http://127.0.0.1:80', my_login, my_password)
repo_list = client.repos.list_repos()
for repo in repo_list:
  list_dir(repo, '/')
print('Total freed size: %d' % freed_size)
