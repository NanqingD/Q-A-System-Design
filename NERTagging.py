#!/usr/bin/env python

from nltk.tag import StanfordNERTagger
from sets import Set


# rename question.txt from Part1 to question_dev.txt
# rename question.txt from Part2 to question_test.txt

# Global Variable
qType = [''] * 321
NER_mapping = {
'Who':['PERSON','ORGANIZATION'],
'Where':['LOCATION','ORGANIZATION'],
'When':['DATE','TIME']
}



def readQuestion(fileType):
	"""
	Scan the question and record the question type with corresponding position in a list.
	"""
	global qType
	f = open('question_%s.txt' %(fileType), 'r+')
	qNum = 0
	for line in f:
		if '<num>' in line:
			qNum = int(line.strip().split()[2])
		
		if 'Who' in line:
			qType[qNum] = 'Who'
		elif 'When' in line:
			qType[qNum] = 'When'
		elif 'Where' in line:
			qType[qNum] = 'Where'

	f.close()


def isEmpty(line):
	"""
	Determine whether to process certain line.
	"""
	if line.strip() == '':
		return True
	return False



def NERTaggering(filename):
	"""
	Call NER tagger from StanfordNERTagger.
	Scan the retrieval text for question and passage.
	Output the answers.
	"""
	global qType, NER_mapping
	st = StanfordNERTagger('/home/nanqing/Documents/stanford-ner-2015-04-20/classifiers/english.muc.7class.distsim.crf.ser.gz','/home/nanqing/Documents/stanford-ner-2015-04-20/stanford-ner.jar')
	print 'Tagger logged successfully!'
	
	f = open(filename, 'r+')
	print '%s opened successfully' %(filename)
	w1 = open('answer_test.txt','w+')
	w2 = open('answer_dev.txt','w+')

	question_id = 0
	rank_id = 0
	document_id = 0
	answers = []
	count = 6
	answerSet = Set()
	for line in f:
		if isEmpty(line):
			continue
		tokens = line.strip().split()
		if tokens[0] == 'Doc':
			cur_question_id = int(tokens[1])
			if cur_question_id != question_id:
				if count < 5:
					for j in range(5 - count):
						if question_id <= 88:
							w1.write('%s %s nil\n' %(question_id, j+1))
						else:
							w2.write('%s %s nil\n' %(question_id, j+1))
						print '%s %s nil' %(question_id, j+1)

				question_id = cur_question_id
				count = 0
				answerSet.clear()

		if tokens[0] == 'Rank':
			rank_id = int(tokens[1])

		if tokens[0] == 'No':
			document_id = int(tokens[1])

		if tokens[0] == 'Passage' and (count < 5):
			taggedTokens = st.tag(tokens[1:])
			for i in range(len(taggedTokens)):
				if taggedTokens[i][1] in NER_mapping[qType[question_id]]:
				    if taggedTokens[i][0] not in answerSet:
				   		answers.append(taggedTokens[i][0])
				   		answerSet.add(taggedTokens[i][0])

			num = len(answers)
			if num >0 and num <= 10:
				if question_id <= 88:
					w1.write('%s %s %s\n' %(question_id, document_id,' '.join(answers)))
				else:
					w2.write('%s %s %s\n' %(question_id, document_id,' '.join(answers)))
				print '%s %s %s' %(question_id, document_id,' '.join(answers))
				count += 1
			elif num > 10:
				if question_id <= 88:
					w1.write('%s %s %s\n' %(question_id, document_id,' '.join(answers[0:10])))
				else:
					w2.write('%s %s %s\n' %(question_id, document_id,' '.join(answers[0:10])))

				print '%s %s %s' %(question_id, document_id,' '.join(answers[0:10]))
				count += 1
			answers = []


	f.close()
	w1.close()
	w2.close()


def main():
	readQuestion('dev')
	readQuestion('test')
	sub = raw_input('Please type the in following format [passageNumber_wordNumber]: ')
	NERTaggering('ReplacedResult%s.txt' %(sub))


if __name__ == '__main__':
	main()












