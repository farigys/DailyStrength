'''
Created on Oct 30, 2013

@author: bgyawali
'''


import os, sys
import shutil


#### parse all the files
def listFiles( srcDir, parseDir ):
    for fileName in os.listdir(srcDir):                            
        filePath = srcDir +'/'+ fileName
        #print filePath
        parsedFilePath = parseDir + '/' + fileName
        print "parsedfilepath" + parsedFilePath
        os.system("java -mx15000m -cp ""../StanfordParser/*:"" edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat ""wordsAndTags"" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz $* "+ filePath + ">"+parsedFilePath)




def get_user_params():
    user_params = {}
    # get user input params
    user_params['inputDir'] = raw_input('Input Directory [Back-Pain/Texts]: ')
    user_params['outputDir'] = raw_input('\nOutput Directory [Back-Pain/Texts.parsed]: ')


    if user_params['inputDir'] == '' or user_params['outputDir'] == '':
        print "Invalid input directory or Output directory. Try again"
        sys.exit()
    return user_params



def dump_user_params(user_params):
    # dump user params for confirmation
    print 'Input Directory:    ' + user_params['inputDir']
    print 'Output Directory:   ' + user_params['outputDir']
    return


def main():
    user_params = get_user_params()
    dump_user_params(user_params)
    ## parsing test data
    if os.path.exists(user_params['outputDir']):
        shutil.rmtree(user_params['outputDir'])
    os.mkdir(user_params['outputDir'])

    listFiles(user_params['inputDir'], user_params['outputDir'])




if __name__ == "__main__":
    main()
    