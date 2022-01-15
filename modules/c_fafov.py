#!/usr/bin/python3

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
    self.vec_dx_um = []
    self.vec_dy_um = []
    f = open(fname)
    for l in f:
      if l.startswith('--- ---- '):  break
    for l in f:
      l = l.strip()
      lb = " ".join( l.split() )
      ll = lb.split(" ")
      self.vec_dx_um.append( float(ll[2]) )
      self.vec_dy_um.append( float(ll[3]) )
    f.close()
    self.n_vec = len(self.vec_dx_um)
    #
  #
  def pro1(self):
    #
    self.vec_dx_mm = []
    self.vec_dy_mm = []
    #
    self.vec_mag_max_um = 0.0
    #
    for i in range(self.n_vec):
      self.vec_dx_mm.append( self.vec_dx_um[i] / 1000.0 )
      self.vec_dy_mm.append( self.vec_dy_um[i] / 1000.0 )
      #
      mag_um = math.hypot(self.vec_dx_um[i], self.vec_dy_um[i])
      if mag_um > self.vec_mag_max_um:
        self.vec_mag_max_um = mag_um
    #
    self.vec_mag_max_mm = self.vec_mag_max_um / 1000.0
    #
    self.vec_mean_dx_mm = np.mean( self.vec_dx_mm )
    self.vec_mean_dy_mm = np.mean( self.vec_dy_mm )
    #
    self.vec_mean_dx_um = np.mean( self.vec_dx_um )
    self.vec_mean_dy_um = np.mean( self.vec_dy_um )
    self.vec_mean_mag_um = math.hypot( self.vec_mean_dx_um, self.vec_mean_dy_um )
    #
    self.mean_ux = self.vec_mean_dx_um / self.vec_mean_mag_um
    self.mean_uy = self.vec_mean_dy_um / self.vec_mean_mag_um
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
    self.sys2_v_x = self.vec_mean_dx_um * self.sys2_e1x
    self.sys2_v_y = self.vec_mean_dy_um * self.sys2_e1y
    self.sys2_v_mag = math.hypot(self.sys2_v_x, self.sys2_v_y)
    # Note that sys2_v_mag will be positive even if the sys2_v
    # is in the opposite direction from the sys2_u vector.
    #
  #
  def plot_vecs_on_layout(self):
    dx = []
    dy = []
    for i in range(self.n_vec):
      dx.append( self.vec_dx_mm[i] * self.scale_fov_to_layout )
      dy.append( self.vec_dy_mm[i] * self.scale_fov_to_layout )
    x = []
    y = []
    for i in range(self.n_vec):
      x.append( self.fov_pos_x )
      x.append( self.fov_pos_x + dx[i] )
      x.append( None )
      y.append( self.fov_pos_y )
      y.append( self.fov_pos_y + dy[i] )
      y.append( None )
    plt.plot(x, y, color='#888888')
    #
    ###############################################
    # value m/s, for graphing will be um/s scale bar.
    # length m, for graphing will be mm.
    #############
    # temporary kluge
    # scale in [mm]/[um/s]
    # SI:  [m]/[m/s]
    ftl_SI = self.scale_fov_to_layout * 1E6 / 1E3
    # self.sbar_len = self.sbar_val * self.scale_fov_to_layout
    # self.sbar_len = self.sbar_val * ftl_SI
    self.sbar_len = self.sbar_val * self.vovg_scale
    #############
    len = self.sbar_len * 1000  # convert m to mm.
    print("sbar_val (um/s): ", self.sbar_val*1E6)
    print("len: ", len)
    x1 = self.sbar_x1 * 1000  # Convert m -> mm
    y1 = self.sbar_y1 * 1000  # Convert m -> mm
    x = [ x1, x1+len ]
    y = [ y1, y1 ]
    plt.plot( x, y, color='#009900' )
    ###############################################
    #
    # vec_mean_dx_mm is in mm/s
    mdx = self.vec_mean_dx_mm * self.scale_fov_to_layout
    mdy = self.vec_mean_dy_mm * self.scale_fov_to_layout
    mx = [ self.fov_pos_x, self.fov_pos_x+mdx ]
    my = [ self.fov_pos_y, self.fov_pos_y+mdy ]
    plt.plot(mx, my, color='#ff0000')
  #
  # class !end
##################################################################





