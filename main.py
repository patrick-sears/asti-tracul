#!/usr/bin/python3

from modules.loshape import *
from modules.c_fafov import c_fafov

import sys
from matplotlib import pyplot as plt



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
  elif key == '!dir_traspe_1':  dir_traspe_1 = ll[1]
  elif key == '!ougfname1':  ougfname1 = ll[1]
  elif key == '!scale_fov_to_layout':  scale_fov_to_layout = float(ll[1])
  elif key == '!standard_flow_axis_mag_on_graph':
    standard_flow_axis_mag_on_graph = float(ll[1])
  elif key == '!fov_pos':
    fov_pos_x = []
    fov_pos_y = []
    i = -1
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      ll = l.split(' ')
      fov_pos_x.append( float(ll[0]) )
      fov_pos_y.append( float(ll[1]) )
      #
      i += 1
      fafov[i].set_fov_pos( float(ll[0]), float(ll[1]) )
  elif key == '!vid':
    fafov = []
    vid = []
    #
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      ll = l.split(' ')
      #
      for v in ll:
        if v.startswith('#'):  continue
        vid.append( int(v) )
        fafov.append( c_fafov( int(v) ) )
  elif key == '!standard_flow_axis':
    i = -1
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      i += 1
      fafov[i].read_standard_flow_axis(l)
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


n_culay = len(culay)

n_fafov = len(fafov)
for i in range(n_fafov):
  fafov[i].sfa_mag_on_graph = standard_flow_axis_mag_on_graph
  fafov[i].set_dir_traspe_1(dir_traspe_1)
  fafov[i].set_scale_fov_to_layout(scale_fov_to_layout)
  fafov[i].load_vecs()
  fafov[i].pro1()



##################################################################
### !graph #######################################################
# The layout.
fig = plt.figure()

for i in range(n_culay):
  culay[i].plot()

plt.plot(fov_pos_x, fov_pos_y,
  linestyle='none',
  marker='s',
  markerfacecolor='none',
  markeredgecolor='#000000',
  markersize=12.0
  )

for i in range(n_fafov):
  fafov[i].plot_vecs_on_layout()

ca = fig.gca()
# plt.xlim(-10, atrack[0].im_w+10 )
# plt.ylim(-10, atrack[0].im_h+10 )
plt.gca().set_aspect('equal', adjustable='box')

plt.title("scale:  mm")

# plt.savefig(oudir+'/'+ougfname1)
plt.savefig(ougfname1)





##################################################################
### !graph #######################################################
# End of graphs.
##################################################################






