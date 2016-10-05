import os
import shutil
import sys
import operator


### read all files and tokenize
def convertToUniversalPoSTags(homeDir, destDir, UniversalPOSMapFile):

## read universal pos tags
    universalPOSMap = {}
    universalPOSFile = open(UniversalPOSMapFile, "r")
    univLines = universalPOSFile.readlines()
    for line in univLines:
        line = line.strip("\n")
        lineParts = line.split("\t")
        universalPOSMap[lineParts[0]]=lineParts[1]
    
    

    print("number of maps" + str(len(universalPOSMap)))
    ## looping through each file of each native language dir
    for fileName in os.listdir(homeDir):
        readFilePath = homeDir + "/" + fileName
        readFile = open(readFilePath, "r")
        writeFile = open(destDir + "/" + fileName, "w")
        #print "fileName: " + readFilePath
        
        allLines = readFile.readlines()   ### this reads whole file and writes everything in a string
        readFile.close()
        
        ## looping through each lines of the file
        for line in allLines:                        
            stripLine = line.strip('\n')
            newUniversalLine=''                        
            if stripLine != '':
                lineParts = stripLine.split(' ')
                for partcnt in range(0, len(lineParts)):
                    #print str(partcnt) + " " + lineParts[partcnt]
                    wordPOS=lineParts[partcnt].rsplit('/',1)
                    newUniversalLine = newUniversalLine + wordPOS[0]+ '/' + universalPOSMap[wordPOS[1]] +' '
            newUniversalLine+="\n"        
            writeFile.write(newUniversalLine)
        
        writeFile.close()
            
## end of function posNGram




def get_user_params():
    user_params = {}
    # get user input params
    user_params['inputDir'] = raw_input('Input Directory [Back-Pain/Texts.parsed]: ')
    user_params['outputDir'] = raw_input('\nOutput Directory [Back-Pain/Texts.universal]: ')


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
    UniversalPOSMapFile = 'en-ptb.map'
    if os.path.exists(user_params['outputDir']):
        shutil.rmtree(user_params['outputDir'])
    os.mkdir(user_params['outputDir'])
    convertToUniversalPoSTags(user_params['inputDir'], user_params['outputDir'], UniversalPOSMapFile)

                    
                
if __name__ == "__main__":
    main()
    