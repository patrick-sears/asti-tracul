#!/usr/bin/python3


from matplotlib import pyplot as plt


##################################################################
class c_fafov:
  #
  def __init__(self, vid):
    self.vid = vid
    self.vidname = 'v{0:03d}'.format( self.vid )
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
    for i in range(self.n_vec):
      self.vec_dx_mm.append( self.vec_dx_um[i] / 1000.0 )
      self.vec_dy_mm.append( self.vec_dy_um[i] / 1000.0 )
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
  #
  # class !end
##################################################################





