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
  elif key == '!oufname1':  oufname1 = ll[1]
  elif key == '!oufname2':  oufname2 = ll[1]
  elif key == '!ougfname1':  ougfname1 = ll[1]
  elif key == '!scale_fov_to_layout':  scale_fov_to_layout = float(ll[1])
  # elif key == '!standard_flow_axis_mag_on_graph':
  #   standard_flow_axis_mag_on_graph = float(ll[1])
  elif key == '!vovg_scale_bar_length':
    vovg_scale_bar_length = float(ll[1])
  elif key == '!vovg_scale_bar_pos':
    vovg_scale_bar_pos_x = float(ll[1])
    vovg_scale_bar_pos_y = float(ll[2])
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
  # fafov[i].sfa_mag_on_graph = standard_flow_axis_mag_on_graph
  fafov[i].sbar_len = vovg_scale_bar_length
  fafov[i].sbar_x1 = vovg_scale_bar_pos_x
  fafov[i].sbar_y1 = vovg_scale_bar_pos_y
  #
  fafov[i].set_dir_traspe_1(dir_traspe_1)
  fafov[i].set_scale_fov_to_layout(scale_fov_to_layout)
  fafov[i].load_vecs()
  fafov[i].pro1()



############################################
# Calculate global direction and speed in
# global direction.
# Global direction for an mctd is between +1 (2pi.u+)
# or -1 (2pi.u-).  The absolute value is less than
# 1 for less than perfect alignment.
# vu is a vector calculated from unit vectors.
# It might be a mean, or a component of a unit vector
# along another.
# In this case it's a component.
glob_vu_mag = 0.0
for i in range(n_fafov):
  glob_vu_mag += fafov[i].sfa_vu_val
glob_vu_mag /= n_fafov
glob_vu_dir = 1
if glob_vu_mag < 0:  glob_vu_dir = -1

# Find the component of the velocity direction in
# the global direction as defined by unit vectors.
# Note it can be negative.
glob_v_val = 0.0
for i in range(n_fafov):
  mag = fafov[i].sfa_v_mag
  if fafov[i].sfa_vu_val < 0:  mag *= -1
  glob_v_val += mag
glob_v_val /= n_fafov
############################################




#######################################################
# oufname1 data
ou = ''
ou += 'i: i_fov,\n'
ou += 'mean_ux mean_uy\n'
ou += 'sfa_mag:  sfa_v_mag\n'
ou += 'sfa_vuv:  sfa_vu_val\n'
ou += '-----------------------\n'
ou += 'i    mean_ux   mean_uy   sfa_mag   sfa_vuv\n'
ou += '---  --------  --------  --------  --------\n'
for i in range(n_fafov):
  ou += '{0:3d}'.format(i)
  ou += '  {0:8.5f}'.format( fafov[i].mean_ux )
  ou += '  {0:8.5f}'.format( fafov[i].mean_uy )
  ou += '  {0:8.3f}'.format( fafov[i].sfa_v_mag )
  ou += '  {0:8.3f}'.format( fafov[i].sfa_vu_val )
  ou += '\n'
fz = open(oufname1, 'w')
fz.write(ou)
fz.close()
#######################################################


#######################################################
# oufname2 data
ou = ''
ou += '\n'
ou += 'glob_vu_mag (1):    {0:8.3f}\n'.format( glob_vu_mag )
ou += 'glob_vu_dir (1):    {0:8.3f}\n'.format( glob_vu_dir )
ou += 'glob_v_val (um/s):  {0:8.3f}\n'.format( glob_v_val )
ou += '\n'
fz = open(oufname2, 'w')
fz.write(ou)
fz.close()
#######################################################





##################################################################
### !graph #######################################################
# Graph 1 -- The layout.
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






