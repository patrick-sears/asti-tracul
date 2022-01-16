#!/usr/bin/python3


##################################################################
# This module file was originally created in 20220 ipro 0115v10a.
##################################################################


import numpy as np
import math


##################################################################
def MoC( Ae1, Ae2, Be1, Be2 ):
  # - For conversion of vector components from system A
  #   to system B.
  # - Ae1 and Ae2 are system A basis vectors.
  # - Be1 and Be2 are system B basis vectors.
  # - All these components must be must be in the same
  #   system.
  #   - For example, if all components are in system A,
  #     then Ae1=<1,0> and Ae2=<0,1>.
  #
  # For a vector v with components in system A (vA), to
  # get the components in system B (vB), do this:
  #    vB = mBA vA
  #
  c11 = np.dot( Be1, Ae1 )
  c12 = np.dot( Be1, Ae2 )
  c21 = np.dot( Be2, Ae1 )
  c22 = np.dot( Be2, Ae2 )
  #
  mBA = np.array( [
      [ c11, c12 ],
      [ c21, c22 ]
    ] )
  #
  return mBA
##################################################################


##################################################################
def get_gr_from_vec( v, x0=0, y0=0 ):
  gx = [x0, x0+v[0]]
  gy = [y0, y0+v[1]]
  return gx, gy
##################################################################



##################################################################
def get_gr_from_vecarray( v, x0=0, y0=0 ):
  gx = []
  gy = []
  #
  for i in range(len(v)):
    gx.append(x0)
    gx.append(x0+v[i][0])
    gx.append(None)
    gy.append(y0)
    gy.append(y0+v[i][1])
    gy.append(None)
  #
  return gx, gy
  #
##################################################################


##################################################################
def rotate_vec(v, ang):
  c = math.cos(ang)
  s = math.sin(ang)
  x = c * v[0] - s * v[1]
  y = s * v[0] + c * v[1]
  return np.array( [x, y] )
##################################################################



##################################################################
def get_matrix_inverse(m):
  if np.linalg.det(m) == 0:  return None
  return np.linalg.inv(m)
##################################################################


##################################################################
def get_gr_wedge_from_vec( v, wid=math.pi/20, x0=0, y0=0 ):
  # Note I want the default wid to be in radians because
  # it will often be called by other functions rather than
  # by humans.
  half_dang = (wid/2)
  v1 = rotate_vec(v, -half_dang)
  v2 = rotate_vec(v,  half_dang)
  gx = [x0, x0+v1[0], x0+v2[0], x0]
  gy = [y0, y0+v1[1], y0+v2[1], y0]
  return gx, gy
##################################################################






##################################################################
def get_gr_circle(r, x0=0, y0=0, n_seg=40):
  x = []
  y = []
  n_pnt = n_seg + 1
  #
  dang = math.pi * 2 / n_seg
  for i in range(n_pnt):
    ang = i * dang
    x.append( x0 + r * math.cos(ang) )
    y.append( y0 + r * math.sin(ang) )
  #
  return x, y
##################################################################



##################################################################
def get_gr_multi_circle(r_array, x0=0, y0=0, n_seg=40):
  x = []
  y = []
  n_pnt = n_seg + 1
  #
  dang = math.pi * 2 / n_seg
  for r in r_array:
    #
    for i in range(n_pnt):
      ang = i * dang
      x.append( x0 + r * math.cos(ang) )
      y.append( y0 + r * math.sin(ang) )
    #
    x.append(None)
    y.append(None)
    #
  #
  return x, y
##################################################################



