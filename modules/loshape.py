#!/usr/bin/python3

from modules import fun

import numpy as np
import sys
import math

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

# loshape:  layout shapes.


##################################################################
class c_loshape_canvas:
  #
  def __init__(self):
    self.w = None
    self.h = None
  #
  def set(self, line):
    # print("Checking: <"+line+">")
    l = line.strip()
    lb = " ".join(l.split())
    ll = lb.split(' ')
    # print("Checking ll: ", ll)
    if ll[0] != 'canvas':
      print("Error.  Strange initial word in loshape_canvas.")
      print('  Expected "canvas".')
      print("  Found:  ["+ll[0]+"]")
      print("  Full line: ", l)
      sys.exit(1)
    self.w = float(ll[1])
    self.h = float(ll[2])
    self.border_color = ll[3]
  #
  def plot(self):
    wr = self.w/2
    hr = self.h/2
    x = [-wr,  wr, wr, -wr, -wr]
    y = [-hr, -hr, hr,  hr, -hr]
    plt.plot(x,y, color=self.border_color)
  #
  # class !end
##################################################################



##################################################################
class c_loshape_line:
  #
  def __init__(self, line=None):
    if line != None:  self.set(line)
  #
  def set(self, line):
    l = line.strip()
    lb = " ".join(l.split())
    ll = lb.split(' ')
    if ll[0] != 'line':
      print("Error.  Strange initial word in loshape_line.")
      print('  Expected "line".')
      print("  Full line: ", l)
      sys.exit(1)
    self.x1 = float(ll[1])
    self.y1 = float(ll[2])
    self.x2 = float(ll[3])
    self.y2 = float(ll[4])
    self.color = ll[5]
  #
  def plot(self):
    x = [self.x1, self.x2]
    y = [self.y1, self.y2]
    plt.plot(x,y, color=self.color)
  #
  # class !end
##################################################################


##################################################################
class c_loshape_circle:
  #
  def __init__(self):
    self.a = None
  #
  def set(self, line):
    l = line.strip()
    lb = " ".join(l.split())
    ll = lb.split(' ')
    if ll[0] != 'circle':
      print("Error.  Strange initial word in loshape_circle.")
      print('  Expected "circle".')
      print("  Full line: ", l)
      sys.exit(1)
    self.n_seg = int(ll[1])
    self.r     = float(ll[2])
    self.color = ll[3]
  #
  def plot(self):
    #
    x, y = fun.get_gr_circle(self.r, n_seg=self.n_seg )
    #
    plt.plot(x,y, color=self.color)
  #
  # class !end
##################################################################




