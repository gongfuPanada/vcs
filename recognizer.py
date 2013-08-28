#!/usr/bin/env python
# (c) Scott Cagno, 2013 All rights reserved
# License: https://sites.google.com/site/bsdc3license

# imports
import gst, gobject, sys

# speech recognition class
class recognizer(gobject.GObject):
	
	# setup
	__gsignals__ = {
		'finished' : (
			gobject.SIGNAL_RUN_LAST, 
			gobject.TYPE_NONE, 
			(gobject.TYPE_STRING,)
		)
	}
	
	# constructor
	def __init__(self, corpus):
		# init
		gobject.threads_init()
		gobject.GObject.__init__(self)
		pipe = [
			'autoaudiosrc',
			'audioconvert',
			'audioresample',
			'vader name=vad',
			'pocketsphinx name=asr',
			'appsink sync=false'
		]

		# assemble audio pipeline
		self.pipeline = gst.parse_launch(' ! '.join(pipe))

		# audio speech recognition, aka pocketsphinx libs
		asr = self.pipeline.get_by_name('asr')
		asr.set_property('lm', corpus + '/lm')
		asr.set_property('dict', corpus + '/dic')
		asr.set_property('configured', True)
		asr.connect('result', self.result)

		# voice activity dector
		self.vad = self.pipeline.get_by_name('vad')
		self.vad.set_property('auto-threshold', True)

	# set state to listen
	def listen(self):
		self.pipeline.set_state(gst.STATE_PLAYING)

	# set state to pause
	def pause(self):
		self.vad.set_property('silent', True)
		self.pipeline.set_state(gst.STATE_PAUSED)

	# emit result
	def result(self, asr, hyp, uttid):
		self.emit('finished', hyp)

	# run the speech recognizer
	def run(self):
		self.listen()
		main_loop = gobject.MainLoop()
		try:
			main_loop.run()
		except:
			main_loop.quit()
			sys.exit("\nGoodbye!")