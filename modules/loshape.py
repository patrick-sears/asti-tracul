#!/usr/bin/python3

import sys

# loshape:  layout shapes.


##################################################################
class c_loshape_canvas:
  def __init__(self):
    self.a = None
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
##################################################################



##################################################################
class c_loshape_line:
  def __init__(self):
    self.a = None
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
##################################################################


##################################################################
class c_loshape_circle:
  def __init__(self):
    self.a = None
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
##################################################################




