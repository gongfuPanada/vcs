#!/usr/bin/env python
# (c) Scott Cagno, 2013 All rights reserved
# License: https://sites.google.com/site/bsdc3license

# imports
from state import state
from recognizer import recognizer
import scopes, os, subprocess


# word parsing engine
class parser(object):

	# constructor
	def __init__(self):
		self.scope=dict(scopes.base.items()+scopes.common.items())
		self.recog=recognizer('corpus')
		self.recog.connect('finished', self.parse)
		self.state=state()

	# scope parser
	def parse(self, asr, hyp):
		hyp=hyp.split(' ')
		if "DICTATE" in hyp:
			self.dictate()
		elif "V-C-S" in hyp:
			self.vcs(0)
		elif "EDITOR" in hyp:
			self.editor(2)
		elif "SHELL" in hyp:
			self.shell(1)
		elif "STOP-V-C-S" in hyp:
			os.system("./stop.sh")
		else:
			for cmd in hyp:
				if cmd in self.scope.keys():
					if self.scope[cmd] != None:
						method, action=self.scope[cmd][0]
						self.xdo(method, action)

	# switch vcs
	def vcs(self, window):
		self.state.set_win(window)
		self.scope=dict(scopes.base.items()+scopes.common.items())

	# switch editor
	def editor(self, window):
		self.state.set_win(window)
		self.scope=dict(scopes.base.items()+scopes.vim.items())

	# switch shell
	def shell(self, window):
		self.state.set_win(window)
		self.scope=dict(scopes.base.items()+scopes.shell.items())

	# dictation helper
	def dictate(self):
		self.recog.pause()
		os.system("notify-send 'Dictation Mode' 'Listening...'")
		try:
			text=subprocess.check_output('./dictate.py')
		except subprocess.CalledProcessError:
			pass
		os.system("killall notify-osd")
		self.xdo('type', text.strip('\n'))
		self.recog.listen()

	# xdotool helper
	def xdo(self, method, action):
		subprocess.call("xdotool %s '%s'" % (method, action), shell=True)

if __name__ == '__main__':
	parser().recog.run()