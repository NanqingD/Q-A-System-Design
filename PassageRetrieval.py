import functions as f
import subprocess

#generate index_parameters_file for each doc
f.generate_index_parameters("doc_test")
f.generate_index_parameters("doc_dev")

#build the Indri Index for each doc
f.Index_all_docs()

#generate all queries
dev_problems = f.Format_Problems("question")
test_problems = f.Format_Problems("question_test")

with open(f.File_path+"RetrievalResult.txt",'w') as t:
    for i in range(1,321): #do passage retrieval for each question
        if i<89:
            category = "doc_test"
            problem = test_problems[i]
        else:
            category = "doc_dev"
            problem = dev_problems[i]
            
        t.write("Doc: " + str(i) +"\n")
        t.write("\n")

        #Use Lemur to do the query (passage retrieval)
        query = "-query=#combine[passage200:200](" + problem + ")" 
        index_path = "-index=" + f.File_path + "indices/" + str(i)
        result = subprocess.check_output([f.Retrieval_path,query,"-count=20",index_path])

        result = result.decode("utf-8")

        #retrieve the table that can convert DOCNO to File No. for this question (doc)
        table = f.DOCNO_to_FileNO(category,i)

        ranks = result.split('\n')

        r = 1
        for rank in ranks: #format the results
            if(rank==''):
                continue
            
            fields = rank.split('\t')

            score = float(fields[0])
            DOCNO = fields[1] #which file (DOCNO) is the to be retrieved passage from
            start = int(fields[2]) #the starting token in the original file of this reuslt (passage)
            end = int(fields[3]) # the ending token in the original file of this result (passage)

            #get the File No.
            FileNO = table[DOCNO]

            #get the corresponding original content (text in the file) of this result
            passage = f.passage_retrieval(category,i,FileNO,start,end)

            t.write("Rank: " + str(r)+"\n")
            t.write("No.: " + str(FileNO) + "\n")
            t.write("Passage: " + passage + "\n")
            t.write("\n")
            r=r+1

        t.write("\n\n\n")
