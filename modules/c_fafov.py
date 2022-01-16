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
  def read_sys2_basis(self, l):
    ll = l.split(';')
    self.sys2_e1x = float(ll[0].strip())
    self.sys2_e1y = float(ll[1].strip())
    self.sys2_e2x = float(ll[2].strip())
    self.sys2_e2y = float(ll[3].strip())
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
    self.fov_pos_x = pos_x
    self.fov_pos_y = pos_y
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
    self.vec_mag_max = 0.0
    #
    for i in range(self.n_vela):
      mag = np.linalg.norm( self.vela[i] )
      if mag > self.vec_mag_max:
        self.vec_mag_max = mag
    #
    self.vel_mean = np.mean( self.vela, axis=0 )
    #
    self.vel_mean_mag = np.linalg.norm( self.vel_mean )
    #
    self.mean_ux = self.vel_mean[0] / self.vel_mean_mag
    self.mean_uy = self.vel_mean[1] / self.vel_mean_mag
    #
    # Calculate the component of the unit vector in the
    # direction of the standard flow axis, sys2_e1.
    # This is a measure of how well aligned the flow is
    # with the standard flow axis.
    # A "vu" is a vector calculated from unit vectors.
    # So it has no units but does not necessarily have
    # a magnitude of 1.
    # dot product...
    sys2_vu_x = self.mean_ux * self.sys2_e1x
    sys2_vu_y = self.mean_uy * self.sys2_e1y
    self.sys2_vu_val = sys2_vu_x + sys2_vu_y
    # sys2_vu_val:  It's the component of the mean direction
    # along the sys2_e1.  It's how well the flow is aligned
    # ignoring speed.  It's range is [-1, +1].  Note that
    # an sy2_vu_val of -1 indicates perfectly aligned flow
    # in the direction opposite from the sy2_e1.
    #
    # Calculate the component of the velocity in the direction
    # of the sys2_e1.
    self.sys2_v_x = self.vel_mean[0] * self.sys2_e1x
    self.sys2_v_y = self.vel_mean[1] * self.sys2_e1y
    self.sys2_v_mag = math.hypot(self.sys2_v_x, self.sys2_v_y)
    # Note that sys2_v_mag will be positive even if the sys2_v
    # is in the opposite direction from the sys2_u vector.
    #
  #
  def set_sys3(self, direction ):
    # First make sure we take care of possible
    # getting a float close to 1 rather than an int.
    # Note we might even get 0 if there is not global
    # direction defined, in which case we just use
    # the same as sys2.
    if direction >= 0:  dir = int(1)   # use sys2
    else:               dir = int(-1)  # rotate by pi
    #
    self.sys3_e1x = dir * self.sys2_e1x
    self.sys3_e1y = dir * self.sys2_e1y
    self.sys3_e2x = dir * self.sys2_e2x
    self.sys3_e2y = dir * self.sys2_e2y
    #
  #
  #
  #
  def plot_vecs_on_layout(self):
    # fp:  fov pos for graphing (in mm)
    fp = np.array( [self.fov_pos_x, self.fov_pos_y] )
    fp *= 1E3 # convert from SI base to mm
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
    # Plot mean vectors.
    #
    grv = self.vel_mean * self.vovg_scale * 1E3
    x, y = fun.get_gr_from_vec_2(grv, pos=fp)
    plt.plot(x, y, color='#ff0000')
  #
  # class !end
##################################################################





