#!/usr/bin/python3

# funb.py:  For string handling.


##################################################################
def oufloat(form, val, mult=1):
  # Handles the case when a float is None.
  # Example using from = '{0:8.3f}'
  mm = form.split(':')     # mm  = [ '{0', '8.3f}' ]
  mma = mm[1].split('.')   # mma = [ '8',  '3f}' ]
  length = int( mma[0] )   # length = 8
  ou = ''
  if val == None:   ou += '-'*length
  else:             ou += form.format( val*mult )
  return ou
##################################################################





