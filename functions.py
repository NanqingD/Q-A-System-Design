################################################################################
#This file contains all the help functions that are used for passage retrieval #
################################################################################
import subprocess
import string
import glob
from nltk.tokenize import WhitespaceTokenizer as wpt
from nltk import word_tokenize as wt
################################################################################
########################## All paths we need to define #########################
#The path where our files exist
File_path = '/Users/JerryKuo/Desktop/NLP/Project 3/'

#The path to call IndriBuildIndex to do indexing
Indexing_path = '/usr/local/bin/IndriBuildIndex'

#The path to call IndriRunQuery to do retrieval
Retrieval_path = '/usr/local/bin/IndriRunQuery'
################################################################################
################################## Help Functions ##############################

#This function generates the indexing_parameters_file for each doc
#input@category: indicate "doc_dev" or"doc_test"
def generate_index_parameters(category):
    #get all docs
    docs = glob.glob(File_path + category + '/*')

    #iterate all docs and generate the corresponding indexing parameters file
    for doc in docs:
        #we first get the No. of this doc
        iteration = -1
        while(doc[iteration]!='/'):
            iteration  = iteration - 1
        Number = doc[iteration+1:len(doc)]

        #Generate the indexing parameters file
        with open(File_path+'parameters/' + Number,'w') as f:
            f.write('<parameters>\n')
            f.write('  <index>../indices/' + Number + '</index>\n')
            f.write('  <memory>1G</memory>\n')
            f.write('  <corpus>\n    <path>../'+ category +'/' + Number + '/</path>\n    <class>trectext</class>\n  </corpus>\n')
            f.write('  <stemmer><name>krovetz</name></stemmer>\n')
            #f.write('  <field>\n    <name>text</name>\n  </field>\n')
            f.write('</parameters>')



#This function is used to build the index for each doc
def Index_all_docs():
    #get all parameters_files
    parameters_files = glob.glob(File_path + 'parameters/*')

    #Build the index for each doc with the corresponding parameters_file
    for file in parameters_files:
        subprocess.call([Indexing_path,file])
        


#This function extracts the question for each doc
#and format the corresponding query for Lemur
#input@category: indicate "question" or "question_test"
#output@problems: a dictionary where key is the question No. while value is the query
def Format_Problems(category):
    problems = {}

    #Something we want to delete in the question, in order to do query in Lemur
    Punc = set(string.punctuation)
    Aux_Art = {'is','was','are','were','did','does','do','the','a'}

    if category == "question":
        key = 88 #initialize problem No.
    else:
        key = 0 #initialize problem No.
    
    flag = 0 #indicate if this line is the content of this question
    with open(File_path+ category +'.txt','r') as f:
        for row in f.readlines():
            if row.find('<num>') != -1:
                key = key + 1
            elif row.find('<desc>') != -1:
                flag = 1
            elif flag == 1: #extract the content of the problem
                #delete all punctuations
                content = ''.join(ch for ch in row[0:len(row)-2].replace("'",' ') if ch not in Punc)

                #delete the words we don't wanna include in the query
                question = ''
                for part in wt(content):
                    if part not in Aux_Art:
                        question = question + part + ' '
                
                problems[key] = question[0:len(question)-1] 
                flag = 0

                
    return problems



#This function constructs a dictionary between DOCNO and the File No. for each doc
#input@category: indicate "doc_dev" or "doc_test"
#input@doc: build the dictionary for which doc
#output@result: the dictionary where key is the DOCNO while value is the corresponding File No.
def DOCNO_to_FileNO(category,doc):
    #get all files in this doc
    files = glob.glob(File_path + category + '/'+str(doc)+'/*')
    result = {}

    for file in files: #iterate all files, and read the content of each one
        with open(file,'r',errors='ignore') as f:
            content = f.read()

        #find the indices of the beginning and end of the DOCNO tag
        begin = content.find('<DOCNO>')
        end = content.find('</DOCNO>')

        #get the DOCNO
        DOCNO = content[begin+7:end].strip()

        #get the File No.
        iteration = -1
        while(file[iteration]!='/'):
            iteration = iteration - 1
        FileNO = int(file[iteration+1:len(file)])

        #put the result into the dictionary
        result[DOCNO] = FileNO

    return result



#This function is used to do passage retrieval
#input@category: indicate "doc_dev" or "doc_test"
#input@doc: which doc is the to be retrieved passage in
#input@file: which file No. is the to be retrieved passage from
#input@start: the index of the token that the passage starts in the TEXT of the file
#input@end: the index of the token that the passage ends in the TEXT of the file
#output@result: the string of the passage 
def passage_retrieval(category,doc,file,start,end):
    result = ''
    this_path = File_path + category + '/'+ str(doc) + '/' + str(file)

    #read the target file
    with open(this_path,'r',errors='ignore') as f:
        content = f.read()
    
    #tokenize the TEXT part
    tokens = wpt().tokenize(content)

    if len(tokens) < end:
        for i in range(len(tokens)-200,len(tokens)):
            result = result + tokens[i] + ' '
        return result[0:len(result)-1]

    #based on the start & end index, do retrieval
    for i in range(start,end):
        result = result + tokens[i] + ' '

    return result[0:len(result)-1]
