#!/usr/bin/env python
# (c) Scott Cagno, 2013 All rights reserved
# License: https://sites.google.com/site/bsdc3license

# import
import os

# state machine
class state(object):

	# constructor
	def __init__(self):
		self.set_win(0)

	# set and change window
	def set_win(self, window):
		os.system('xdotool key ctrl+a key %d' % (window))
		self.win=window