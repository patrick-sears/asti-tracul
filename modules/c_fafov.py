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
    # self.sfa_on_mag = None
    self.sbar_len = None  # um/s
    self.sbar_len_mm = None
    self.sbar_x1 = None
    self.sbar_y1 = None
  #
  def read_standard_flow_axis(self, l):
    ll = l.split(' ')
    # sfa:  standard flow axis
    self.sfa_ux = float(ll[0])
    self.sfa_uy = float(ll[1])
  #
  def set_dir_traspe_1(self, dir):
    self.dir_traspe_1 = dir
  #
  def set_scale_fov_to_layout(self, scale):
    self.scale_fov_to_layout = scale
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
    # direction of the standard flow axis.
    # This is a measure of how well aligned the flow is
    # with the standard flow axis.
    # A "vu" is a vector calculated from unit vectors.
    # So it has no units but does not necessarily have
    # a magnitude of 1.
    # dot product...
    vu_x = self.mean_ux * self.sfa_ux
    vu_y = self.mean_uy * self.sfa_uy
    self.sfa_vu_val = vu_x + vu_y
    # sfa_vu_val:  It's the component of the mean direction
    # along the sfa.  It's how well the flow is aligned
    # ignoring speed.  It's range is [-1, +1].  Note that
    # an sfa_vu_val of -1 indicates perfectly aligned flow
    # in the direction opposite from the sfa.
    #
    # Calculate the component of the velocity in the direction
    # of the sfa.
    self.sfa_v_x = self.vec_mean_dx_um * self.sfa_ux
    self.sfa_v_y = self.vec_mean_dy_um * self.sfa_uy
    self.sfa_v_mag = math.hypot(self.sfa_v_x, self.sfa_v_y)
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
    # "/1000" because in um/s.
    ### madx = self.sfa_ux * (self.sfa_mag_on_graph/1000) * self.scale_fov_to_layout
    ### mady = self.sfa_uy * (self.sfa_mag_on_graph/1000) * self.scale_fov_to_layout
    ### max = [ self.fov_pos_x, self.fov_pos_x+madx ]
    ### may = [ self.fov_pos_y, self.fov_pos_y+mady ]
    ### plt.plot(max, may, color='#008800')
    #
    # um/s scale bar.
    self.sbar_len_mm = self.sbar_len * self.scale_fov_to_layout / 1000.0
    sbar_x2 = self.sbar_x1 + self.sbar_len_mm
    sbar_y2 = self.sbar_y1
    sbar_x = [ self.sbar_x1, sbar_x2 ]
    sbar_y = [ self.sbar_y1, sbar_y2 ]
    plt.plot( sbar_x, sbar_y, color='#009900' )
    #
    #
    mdx = self.vec_mean_dx_mm * self.scale_fov_to_layout
    mdy = self.vec_mean_dy_mm * self.scale_fov_to_layout
    mx = [ self.fov_pos_x, self.fov_pos_x+mdx ]
    my = [ self.fov_pos_y, self.fov_pos_y+mdy ]
    plt.plot(mx, my, color='#ff0000')
  #
  # class !end
##################################################################

    self.vec_mean_dy_mm = np.mean( self.vec_dy_mm )




