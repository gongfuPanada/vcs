#!/usr/bin/env python
import os, urllib2, json

def dictate():
	os.system('sox -q -r 16000 -b 16 -c 1 -d a.flac silence 1 0.3 1% 1 0.5 1% 2>/dev/null')
	audio=open('a.flac', 'rb').read()
	apiurl='http://www.google.com/speech-api/v1/recognize?client=chromium&lang=en-us'
	header={'Content-Type': 'audio/x-flac; rate=16000'}
	request=urllib2.Request(apiurl, audio, header)
	response=urllib2.urlopen(request)
	os.remove('a.flac')
	return json.loads(response.read())['hypotheses'][0]['utterance']

if __name__ == '__main__':
	print(dictate())