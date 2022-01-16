#!/usr/bin/python3

from modules import fun

import numpy as np
from matplotlib import pyplot as plt
import math


##################################################################
class c_fafov:
  #
  def __init__(self, vid):
    self.vid = vid
    self.vidname = 'v{0:03d}'.format( self.vid )
    # scale bar:
    #  sbar_len is it's length on graph.
    #  sbar_val is the value it stands for.
    self.sbar_len = None  # m (converted to mm on graph)
    # self.sbar_len_mm = None
    self.sbar_val = None  # m/s (converted to um/s on graph)
    self.sbar_x1 = None
    self.sbar_y1 = None
  #
  def read_sysB_basis(self, l):
    ll = l.split(';')
    #
    e1x = float(ll[0].strip())
    e1y = float(ll[1].strip())
    e2x = float(ll[2].strip())
    e2y = float(ll[3].strip())
    self.sysA_Be1 = np.array( [e1x, e1y] )
    self.sysA_Be2 = np.array( [e2x, e2y] )
    #
    e1 = [1, 0]
    e2 = [0, 1]
    self.mocBA = fun.MoC(e1, e2, self.sysA_Be1, self.sysA_Be2)
    #
  #
  def set_dir_traspe_1(self, dir):
    self.dir_traspe_1 = dir
  #
  def set_scale_fov_to_layout(self, scale):
    self.scale_fov_to_layout = scale
  #
  def set_vovg_scale(self, scale):
    self.vovg_scale = scale
  #
  def set_fov_pos(self, pos_x, pos_y):
    self.fov_pos = np.array( [pos_x, pos_y] )
  #
  def load_vecs(self):
    #
    fname = self.dir_traspe_1 + '/' + self.vidname + '.data'
    #
    ######################################
    # Input is in um/s, convert to SI base units.
    self.vela = []
    #
    f = open(fname)
    for l in f:
      if l.startswith('--- ---- '):  break
    for l in f:
      l = l.strip()
      lb = " ".join( l.split() )
      ll = lb.split(" ")
      vel = [ float(ll[2])/1E6, float(ll[3])/1E6 ]
      self.vela.append( np.array( vel ) )
    f.close()
    self.n_vela = len(self.vela)
  #
  def pro1(self):
    #
    self.vel_mag_max = 0.0
    #
    for i in range(self.n_vela):
      mag = np.linalg.norm( self.vela[i] )
      if mag > self.vel_mag_max:
        self.vel_mag_max = mag
    #
    self.vel_mean = np.mean( self.vela, axis=0 )
    #
    self.vel_mean_mag = np.linalg.norm( self.vel_mean )
    #
    # vel_mean_u is the unit vector for vel_mean.
    self.vel_mean_u = self.vel_mean / self.vel_mean_mag
    #
    ###############
    # Calculate the component of the unit vector in the
    # direction of the standard flow axis, Be1.
    # This is a measure of how well aligned the flow is
    # with the standard flow axis.
    # A "vu" is a vector calculated from unit vectors.
    # So it has no units but does not necessarily have
    # a magnitude of 1.
    ###############
    # dot product...
    self.sysB_vu_val = np.dot( self.vel_mean_u, self.sysA_Be1 )
    ###
    # sysB_vu_val:  It's the component of the mean direction
    # along the Be1.  It's how well the flow is aligned
    # ignoring speed.  It's range is [-1, +1].  Note that
    # an sysB_vu_val of -1 indicates perfectly aligned flow
    # in the direction opposite from the sy2_e1.
    #
    # Calculate the component of the velocity in the direction
    # of the Be1.
    # sysB_vel_mean is the mean_vel with components in sysB.
    self.sysB_vel_mean = self.mocBA * self.vel_mean
    self.sysB_vel_mean_mag = np.linalg.norm( self.sysB_vel_mean )
    # Note that sysB_vel_mean_mag will be positive even if the
    # sysB_vel_mean is in the opposite direction from the sysB_u
    # vector.
    #
    # gef:  globally effective flow.
    self.gef_mag = np.dot( self.vel_mean, self.sysA_Be1 )
    self.gef_vel = self.gef_mag * self.sysA_Be1
    #
    #
  #
  def set_sysC(self, direction ):
    # First make sure we take care of possible
    # getting a float close to 1 rather than an int.
    # Note we might even get 0 if there is not global
    # direction defined, in which case we just use
    # the same as sysB.
    if direction >= 0:  dir = int(1)   # use sysB
    else:               dir = int(-1)  # rotate by pi
    #
    self.sysA_Ce1 = dir * self.sysA_Be1
    self.sysA_Ce2 = dir * self.sysA_Be2
    #
  #
  #
  #
  def plot_vecs_on_layout(self):
    # fp:  fov pos for graphing (in mm)
    fp = 1E3 * self.fov_pos
    #
    # Plot the velocity vectors.
    # Convert vovg:  velocity to distance on graph.
    # Then convert 1E3:  SI base to mm for graphing.
    #
    grv = self.vela
    for i in range(self.n_vela):
      grv[i] *= 1E3 * self.vovg_scale
    x, y = fun.get_gr_from_vecarray_2( grv, pos=fp )
    #
    plt.plot(x, y, color='#888888')
    #
    ###############################################
    # Plot the scale bar for velocity on the distance
    # graph.
    # value m/s, for graphing will be um/s scale bar.
    # length m, for graphing will be mm.
    self.sbar_len = self.sbar_val * self.vovg_scale
    # Convert m to mm.
    len = self.sbar_len * 1E3
    x1 = self.sbar_x1 * 1E3
    y1 = self.sbar_y1 * 1E3
    #
    x = [ x1, x1+len ]
    y = [ y1, y1 ]
    plt.plot( x, y, color='#009900' )
    ###############################################
    #
    # Globally effective flow.
    v = self.gef_vel * self.vovg_scale * 1E3
    x, y = fun.get_gr_from_vec_2(v, pos=fp)
    plt.plot(x, y, color='#00cc00')
    #
    # Plot mean vectors.
    grv = self.vel_mean * self.vovg_scale * 1E3
    x, y = fun.get_gr_from_vec_2(grv, pos=fp)
    plt.plot(x, y, color='#ff0000')
    #
  #
  # class !end
##################################################################





