#!/usr/bin/env python

import re
import string

def removeTags(inputfile,outputfile):
	"""
	Remove Tags <> [] {} from passage.
	Remove punctuation from passage.
	"""
	f = open(inputfile, 'r')

	text = f.read()
	text = re.sub(r'[\<\(\{\[].*[\>\)\}\]]','',text)
	replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
	text = text.translate(replace_punctuation)
	print 'No punctuation!'

	w = open(outputfile, 'w+')
	w.write(text)

	f.close()
	w.close()

if __name__ == '__main__':
	sub = raw_input('Please type the in following format [passageNumber_wordNumber]: ')
	removeTags('RetrievalResult%s.txt' %(sub),'ReplacedResult%s.txt' %(sub))