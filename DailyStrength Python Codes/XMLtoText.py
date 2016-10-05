'''
by binod gyawali

this program divides a XML into multiple texts. 
Eg: a XML file has problem at first and replies.
So, it will create one file with problem_XML file name
and for each replies: it will create files replies_xmlFileName_replyNo
if the number of replies is 5, then replyNo gies from 1 to 5. 
'''

from BeautifulSoup import *
import os, shutil

def parseFile(xmlFile, fileId, outputDir):
	print xmlFile + " processing started"	
	xmlFile = open(xmlFile, "r")
	content = xmlFile.readlines()
	# create beautiful soup object
	soup = BeautifulSoup(''.join(content))
	
	### lists all problem Tags, reads the contents and puts them into text
	problem = soup.findAll("problem")
	for p in problem:
		problemContent = ""
		if(len(p.contents)>=3):
			contents = p.contents[3].contents
			for i in range(len(contents)):
				#print i, contents[i]
				if (isinstance(contents[i], Tag) and len(contents[i].contents)>0):			
					problemContent = problemContent + " " +  contents[i].contents[0] 
	problemFile = open(outputDir + "/Problem_"+fileId+".txt", "w")
	problemFile.write(problemContent.strip());
	problemFile.close()

	### finds all replies and for each reply, it will read the contents and create multiple reply files				
	replies = soup.findAll("reply")
	for reply in replies:
		attrDict = dict(reply.attrs)		
		#print fileId, attrDict['id']
		replyContent = ""
		contents = reply.contents[5].contents
		for i in range(len(contents)):
			#print i, contents[i]
			if(isinstance(contents[i],Tag) and len(contents[i].contents)>0):
				replyContent = replyContent + " " + contents[i].contents[0]
		replyFile = open(outputDir + "/Reply_" + fileId + "_"+ attrDict['id']+ ".txt", "w")
		replyFile.write(replyContent.strip().encode('utf-8').decode('ascii', 'ignore'))
		replyFile.close()
		#print 



def get_user_params():
	user_params = {}
	# get user input params
	user_params['xmlDir'] = raw_input('XML Input Directory [Back-Pain/XML]: ')
	user_params['outputDir'] = raw_input('\nOutput Directory [Back-Pain]: ')


	if user_params['xmlDir'] == '' or user_params['outputDir'] == '':
		print "Invalid xml directory or Output directory. Try again"
		sys.exit()
	return user_params



def dump_user_params(user_params):
	# dump user params for confirmation
	print 'XML Input Directory:    ' + user_params['xmlDir']
	print 'Output Directory:   ' + user_params['outputDir']
	return




def main():	
	user_params = get_user_params()
	dump_user_params(user_params)
	outputDir = user_params['outputDir']+"/Texts"
	if os.path.exists(outputDir):
		shutil.rmtree(outputDir)
	os.makedirs(outputDir)
	for files in os.listdir(user_params['xmlDir']):
		#print os.path.realpath(files)
		files = user_params['xmlDir'] + "/" + files
		if os.path.isfile(files):
			print files
			fileName = files.split("/")[2]
			fileMatch = re.search('([0-9]+)',fileName)
			fileId = fileMatch.group(1)
			parseFile(files, fileId, outputDir)
			
	

if __name__== '__main__':
	#xmlDir = 'Acne/XML'
	#outputDir = 'Acne/Texts'	
	
	main()
	
