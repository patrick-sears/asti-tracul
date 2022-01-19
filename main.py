#!/usr/bin/python3

from modules.loshape import *
from modules.c_fafov import c_fafov
from modules import funb
from modules.c_meaner import c_meaner

import sys
from matplotlib import pyplot as plt



fname_conf = sys.argv[1]

print("Reading configs...")
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
  elif key == '!dir_traspe_2':  dir_traspe_2 = ll[1]
  elif key == '!oudir':  oudir = ll[1]
  elif key == '!oufname1':  oufname1 = ll[1]
  elif key == '!oufname2':  oufname2 = ll[1]
  elif key == '!oufname_g1':  oufname_g1 = ll[1]
  elif key == '!use_g1b':
    if ll[1] == '1':  use_g1b = True
    else:             use_g1b = False
  elif key == '!oufname_g1b':  oufname_g1b = ll[1]
  elif key == '!scale_fov_to_layout':  scale_fov_to_layout = float(ll[1])
  elif key == '!vovg_scale':
    v1 = float(ll[1]) / 1E6  # um/s -> m/s
    v2 = float(ll[2]) / 1E3  # mm -> m
    vovg_scale = v2 / v1
  elif key == '!vovg_sbar_val':
    # convert input um/s to m/s.
    vovg_sbar_val = float(ll[1]) / 1.0E6
  elif key == '!vovg_sbar_pos':
    # convert input (mm) to m.
    vovg_sbar_x1 = float(ll[1]) / 1E3
    vovg_sbar_y1 = float(ll[2]) / 1E3
  elif key == '!fov_pos':
    # fov pos entered in mm, convert to m.
    fov_pos_x = []
    fov_pos_y = []
    i = -1
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      ll = l.split(' ')
      fpx = float(ll[0]) / 1E3
      fpy = float(ll[1]) / 1E3
      fov_pos_x.append( fpx )
      fov_pos_y.append( fpy )
      #
      i += 1
      fafov[i].set_fov_pos( fpx, fpy )
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
  elif key == '!sysB_basis':
    i = -1
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      i += 1
      fafov[i].read_sysB_basis(l)
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
  fafov[i].sbar_val = vovg_sbar_val
  fafov[i].sbar_x1 = vovg_sbar_x1
  fafov[i].sbar_y1 = vovg_sbar_y1
  #
  fafov[i].set_dir_traspe(dir_traspe_1, dir_traspe_2)
  fafov[i].set_scale_fov_to_layout(scale_fov_to_layout)
  fafov[i].set_vovg_scale(vovg_scale)
  #
  # This is loaded from the traspe output files.
  fafov[i].load_vecs()
  fafov[i].load_ats_data()
  #
  fafov[i].pro1()


n_fafov_valid = 0
for i in range(n_fafov):
  if fafov[i].n_vela > 0:  n_fafov_valid += 1


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
glob1_vu_mag = 0.0
glob1_vu_dir = None
for i in range(n_fafov):
  if fafov[i].n_vela > 0:
    glob1_vu_mag += fafov[i].sysB_vu_val
if n_fafov_valid > 0:
  glob1_vu_mag /= n_fafov_valid
  glob1_vu_dir = 1
  if glob1_vu_mag < 0:  glob1_vu_dir = -1
# I'm not sure yet but I think I might do the following
# for glob1_vu_dir:  None for when there are no tracks,
# 0 for when there are tracks but they don't all go
# in the same global direction.



glob1_sysC_valid = True
# The sysC is the basis system of global flow.
# It is only valid if there is a coordinated global flow.
# System C must be global.  The glob1_ prefix is just
# here as a reminder that it goes with other global
# variables.

if glob1_vu_dir == None:
  glob1_sysC_valid = False
else:
  for i in range(n_fafov):
    if fafov[i].n_vela == 0:
      glob1_sysC_valid = False
      break
    if fafov[i].sysB_vu_val * glob1_vu_dir <= 0:
      # sysB_vu_val and glob1_vu_dir have opposite
      # signs.  The global direction should only
      # be valid if all FOVs go in the same direction.
      glob1_sysC_valid = False


# Find the component of the velocity direction in
# the global direction as defined by unit vectors.
# Note it can be negative.
glob1_v_val = 0.0
for i in range(n_fafov):
  if fafov[i].n_vela > 0:
    mag = fafov[i].sysB_vel_mean_mag
    if fafov[i].sysB_vu_val < 0:  mag *= -1
    glob1_v_val += mag
if fafov[i].n_vela > 0:
  glob1_v_val /= n_fafov_valid
############################################



for i in range(n_fafov):
  ### print("&&> glob1_vu_dir: ", glob1_vu_dir)
  fafov[i].sysC_valid = glob1_sysC_valid
  #
  fafov[i].set_sysC( glob1_vu_dir )
  # if glob1_vu_dir == 1, it's the same as sysB.
  # If -1, there is a pi rotation of the basis
  # vectors.
  #
  fafov[i].pro2()


gef_mag_mean = 0.0
if glob1_sysC_valid:
  for i in range(n_fafov):
    gef_mag_mean += fafov[i].gef_mag
gef_mag_mean /= n_fafov



#######################################################
# glob2:  global mean values derived from ats data

glob2_mean_v_mag = c_meaner()
glob2_mean_speed = c_meaner()
glob2_v_align_mag = c_meaner()
glob2_wmean_curv = c_meaner()

for i in range(n_fafov):
  glob2_mean_v_mag.add( fafov[i].ats_mean_v_mag )
  glob2_mean_speed.add( fafov[i].ats_mean_speed )
  glob2_v_align_mag.add( fafov[i].ats_v_align_mag )
  glob2_wmean_curv.add( fafov[i].ats_wmean_curv )

glob2_mean_v_mag.pro1()
glob2_mean_v_mag.set_name('glob2_mean_v_mag', 'um/s', 1E6)
glob2_mean_v_mag.set_form(' ; ', '{0:18}', '{0:7}', '{0:3d}', '{0:9.3f}')

glob2_mean_speed.pro1()
glob2_mean_speed.set_name('glob2_mean_speed', 'um/s', 1E6)
glob2_mean_speed.set_form(' ; ', '{0:18}', '{0:7}', '{0:3d}', '{0:9.3f}')

glob2_v_align_mag.pro1()
glob2_v_align_mag.set_name('glob2_v_align_mag', '1', 1)
glob2_v_align_mag.set_form(' ; ', '{0:18}', '{0:7}', '{0:3d}', '{0:9.3f}')

glob2_wmean_curv.pro1()
glob2_wmean_curv.set_name('glob2_wmean_curv', 'um^-1', 1E-6)
glob2_wmean_curv.set_form(' ; ', '{0:18}', '{0:7}', '{0:3d}', '{0:9.3f}')
#######################################################




##################################################################
##################################################################
##################################################################
print("Saving output...")

#######################################################
# oufname1 data
ou = ''
ou += '-----------------------------------------------------\n'
ou += 'i: i_fov,\n'
ou += 'mean_ux mean_uy:  vel_mean_u{x y}\n'
ou += 'vel_mag:  vel_mean_mag, the mag of the mean vel.\n'
ou += 'sysB_mag:  sysB_vel_mean_mag, should be same as vel_mag.\n'
ou += 'sysB_vuv:  sysB_vu_val\n'
ou += '-----------------------\n'
ou += '!data_table_1\n'  # This will be useful for external files reading.
ou += 'i    mean_ux   mean_uy   vel_mag   sysB_mag  sysB_vuv\n'
ou += '---  --------  --------  --------  --------  --------\n'
for i in range(n_fafov):
  ou += '{0:3d}'.format(i)
  ou += fafov[i].ouline1()
  ou += '\n'
ou += '-----------------------------------------------------\n'
ou += '\n\n\n'
#################
ou += '-----------------------------------------------------\n'
ou += 'gef_mag (um/s)\n'
ou += '-----------------------\n'
ou += '!data_table_2\n'  # This will be useful for external files reading.
ou += 'i    gef_mag\n'
ou += '---  --------  --------  --------  --------  --------\n'
for i in range(n_fafov):
  ou += '{0:3d}'.format(i)
  ou += fafov[i].ouline2()
  ou += '\n'
ou += '-----------------------------------------------------\n'
ou += '\n\n\n'
#################
ou += '-----------------------------------------------------\n'
ou += 'v_mag:    ats_mean_v_mag (um/s)\n'
ou += 'speed:    ats_mean_speed (um/s)\n'
ou += 'ali_mag:  ats_v_align_mag (1)\n'
ou += 'wm_curv:  ats_wmean_curv (um^{-1})\n'
ou += '-----------------------\n'
ou += '!data_table_3 - traspe ats data\n'
ou += 'i    v_mag     speed     ali_mag   wm_curv\n'
ou += '---  --------  --------  --------  --------  --------\n'
for i in range(n_fafov):
  ou += '{0:3d}'.format(i)
  ou += fafov[i].ouline3()
  ou += '\n'
ou += '-----------------------------------------------------\n'
ou += '\n\n\n'
#################
fz = open(oudir+'/'+oufname1, 'w')
fz.write(ou)
fz.close()
#######################################################


#######################################################
# oufname2 data
ou = ''
ou += '\n'
ou += '-------------------------------------------------\n'
ou += '!table_1\n'
ou += 'n_fafov:              {0:8d}\n'.format(n_fafov)
ou += 'n_fafov_valid:        {0:8d}\n'.format(n_fafov_valid)
if glob1_vu_dir != None:
  ou += 'glob1_vu_mag (1):      {0:8.3f}\n'.format( glob1_vu_mag )
  ou += 'glob1_vu_dir (1):      {0:8.3f}\n'.format( glob1_vu_dir )
  ou += 'glob1_v_val (um/s):    {0:8.3f}\n'.format( glob1_v_val *1E6 ) # m/s->um/s
else:
  ou += 'glob1_vu_mag (1):      --------\n'
  ou += 'glob1_vu_dir (1):      --------\n'
  ou += 'glob1_v_val (um/s):    --------\n'
if glob1_sysC_valid:
  ou += 'glob1_sysC_valid:      yes\n'
  ou += 'gef_mag_mean (um/s):  {0:8.3f}\n'.format( gef_mag_mean *1E6 ) # m/s->um/s
else:
  ou += 'glob1_sysC_valid:      no\n'
  ou += 'gef_mag_mean (um/s):  --------\n'
ou += '-------------------------------------------------\n'

ou += '\n'
ou += '\n'
ou += '\n'
ou += '-------------------------------------------------\n'
ou += 'glob2 values:\n'
ou += 'These are the global means for ats values.\n'
ou += 'n*:  n_valid\n'
ou += '-------------------------------------------------\n'
ou += '!table_2\n'
ou += 'name               ; units   ; n*  ;  mean\n'
ou += '-------------------------------------------------\n'
ou += glob2_mean_v_mag.ouline1()
ou += glob2_mean_speed.ouline1()
ou += glob2_v_align_mag.ouline1()
ou += glob2_wmean_curv.ouline1()
ou += '-------------------------------------------------\n'
ou += '\n'
fz = open(oudir+'/'+oufname2, 'w')
fz.write(ou)
fz.close()
#######################################################





##################################################################
### !graph #######################################################
# Graph 1 -- The layout with vectors.  g1
fig = plt.figure()

for i in range(n_culay):  culay[i].plot()

fpx = []
fpy = []
for i in range(n_fafov):  # convert m->mm
  fpx.append(fov_pos_x[i] * 1E3)
  fpy.append(fov_pos_y[i] * 1E3)
plt.plot(fpx, fpy,
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

# plt.title("scale:  mm")
plt.title( cul_name+'.  Scale, mm.')

plt.savefig(oudir+'/'+oufname_g1, bbox_inches='tight')



##################################################################
### !graph #######################################################
# Graph 1b -- The layout by itself.  g1b
if use_g1b:
  plt.clf()
  fig = plt.figure()
  #
  for i in range(n_culay):  culay[i].plot()
  #
  fpx = []
  fpy = []
  for i in range(n_fafov):  # convert m->mm
    fpx.append(fov_pos_x[i] * 1E3)
    fpy.append(fov_pos_y[i] * 1E3)
  plt.plot(fpx, fpy,
    linestyle='none',
    marker='s',
    markerfacecolor='none',
    markeredgecolor='#000000',
    markersize=12.0
    )
  #
  # for i in range(n_fafov):  fafov[i].plot_vecs_on_layout()
  #
  ca = fig.gca()
  # plt.xlim(-10, atrack[0].im_w+10 )
  # plt.ylim(-10, atrack[0].im_h+10 )
  plt.gca().set_aspect('equal', adjustable='box')
  #
  plt.title("scale:  mm")
  #
  plt.savefig(oudir+'/'+oufname_g1b, bbox_inches='tight')






##################################################################
### !graph #######################################################
# End of graphs.
##################################################################





