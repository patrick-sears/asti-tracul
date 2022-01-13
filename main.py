#!/usr/bin/python3

from modules.loshape import *

import sys


fname_conf = sys.argv[1]

############################################
f = open(fname_conf)
for l in f:
  if not l.startswith('!'):  continue
  l = l.strip()
  ll = l.split(' ')
  key = ll[0]
  ###
  if key == '!run_name':  run_name = ll[1]
  elif key == '!cul_name':  cul_name = ll[1]
  elif key == '!vid':
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      ll = l.split(' ')
      #
      vid = []
      for v in ll:
        if v.startswith('#'):  continue
        vid.append( int(v) )
  elif key == '!culture_layout':
    culay = []
    i = -1
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      i += 1
      #
      # print("Checking: ["+l+"]")
      if l.startswith('canvas'):
        culay.append( c_loshape_canvas() )
        culay[i].set(l)
      elif l.startswith('line'):
        culay.append( c_loshape_line() )
        culay[i].set(l)
      elif l.startswith('circle'):
        culay.append( c_loshape_circle() )
        culay[i].set(l)
      else:
        print("Error.  Unrecognized shape in !culture_layout.")
        print("  line: ", l)
        sys.exit(1)
  else:
    print("Error.  Unrecognized key.")
    print("  key: ", key)
    sys.exit(1)
  #
f.close()
############################################






