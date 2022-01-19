#!/usr/bin/python3





##################################################################
class c_meaner:
  #
  def __init__(self):
    self.x = []
    self.n_valid = 0
    self.mean = None
  #
  def add(self, x):
    self.x.append(x)
  #
  def pro1(self):
    self.mean = 0
    for v in self.x:
      if v == None:  continue
      self.mean += v
      self.n_valid += 1
    if self.n_valid == 0:
      self.mean = None
    else:
      self.mean /= self.n_valid
  #
  def set_name(self, name, ou_units, ou_units_mult):
    self.name = name
    self.ou_units = ou_units
    self.ou_units_mult = ou_units_mult
  #
  def set_form(self, delim, form1, form2, form3, form4):
    self.delim = delim
    self.form1 = form1  # name
    self.form2 = form2  # ou units
    self.form3 = form3  # n_valid
    self.form4 = form4  # mean
    #
    # Example using from = '{0:8.3f}'
    mm = form4.split(':')     # mm  = [ '{0', '8.3f}' ]
    mma = mm[1].split('.')   # mma = [ '8',  '3f}' ]
    length = int( mma[0] )   # length = 8
    self.ou_for_none = '-' * length
  #
  def ouline1(self):
    ou = ''
    ou += self.form1.format(self.name)
    ou += self.delim
    ou += self.form2.format(self.ou_units)
    ou += self.delim
    ou += self.form3.format(self.n_valid)
    ou += self.delim
    if self.mean == None:  ou += self.ou_for_none
    else:
      ou_mean = self.mean * self.ou_units_mult
      ou += self.form4.format(ou_mean)
    ou += '\n'
    return ou
  #
##################################################################





