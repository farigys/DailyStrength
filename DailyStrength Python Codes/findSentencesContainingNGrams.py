'''
Created on Dec 6, 2013

@author: bgyawali
'''


import os, sys, operator
import re
import nltk

     
def findSentencesWithTopEmotionWords(emotionWordsDict, filesDir, outputDir, ngramType):
    print "collecting the sentences with top emotion words"
    writeFile = open (outputDir + "/SentencesNPOSWithTopLIWCAffect" + ngramType + ".txt", "w")
    for emWord in emotionWordsDict:
        for textFile in os.listdir(filesDir):
            textFile = filesDir + "/" + textFile
            if(os.path.isfile(textFile)):
                openFile = open(textFile)
                sentences = openFile.readlines()
                for sen in sentences:
                    senLower = sen.strip("\n").strip().lower()
                    if(senLower != ''):
                        if(re.search(emWord, senLower)):
                            tokMerged = ""
                            tokens = sen.strip("\n").strip().split(" ")
                            for i in range(len(tokens)):
                                word = tokens[i].rsplit('_', 1)[0]
                                tokMerged += word + " "
                            writeFile.write(emWord + "\t" + emotionWordsDict[emWord] + "\t"  + tokMerged + "\n")

        
        
def getTopEmotionWords(posEmotionFile, negEmotionFile, emotToExclude, noOfEmotionWords, totalNGramCountFile):
    
    ## read total number of ngrams fro the file
    totNGramCount = 0
    if totalNGramCountFile != "":
        TotnGramCntFile = open(totalNGramCountFile)
        totNGramCount = int(TotnGramCntFile.readline().strip("\n").split("\t")[1])
    #print "cnt" + str(totNGramCount)
    
    ### read ngrams to exclude file and put them in dict
    nGramExcludeDict = {}
    if(emotToExclude != ""):
        emotExcludeFile = open(emotToExclude)
        sentences = emotExcludeFile.readlines()
        for sen in sentences:
            if sen.strip("\n")!="":
                nGramExcludeDict[sen.strip("\n")] = 0
    
    #for temp in nGramExcludeDict:
    #    print temp + "\t" + str(nGramExcludeDict[temp])            

    #print str(len(nGramExcludeDict)) + "\n\n"                
    ### read positive emotion ngrams and store in a dictionary             
    posFile = open(posEmotionFile)
    sentences = posFile.readlines()
    posNGrams = {}
    for sen in sentences:
        ngram = sen.strip("\n").split("\t")[0]
        count = int(sen.strip("\n").split("\t")[1])
        if ngram not in nGramExcludeDict:
            if totNGramCount != 0:
                posNGrams[ngram]= str(count/float(totNGramCount)) + "\tpositive"
            else:
                posNGrams[ngram]= str(count) +  "\tpositive"
            
            if(len(posNGrams)>=noOfEmotionWords):
                break
    
    ### read negative emotion ngrams and store in a dictionary    
    negFile = open(negEmotionFile)
    sentences = negFile.readlines()
    negNGrams = {}
    for sen in sentences:
        ngram = sen.strip("\n").split("\t")[0]
        count = int(sen.strip("\n").split("\t")[1])
        if ngram not in nGramExcludeDict:
            if totNGramCount != 0:
                negNGrams[ngram]= str(count/float(totNGramCount)) +  "\tnegative"
            else:
                negNGrams[ngram]= str(count) +  "\tnegative"
            if(len(negNGrams)>=noOfEmotionWords):
                break
    
    '''    
    print len(negNGrams), len(posNGrams)
    for temp in posNGrams:
        print temp + "\t" + posNGrams[temp]
    for temp in negNGrams:
        print temp + "\t" + negNGrams[temp]
    '''
                
    emotNGrams = dict(posNGrams.items()  + negNGrams.items())
    return emotNGrams
                

def get_user_params():
    user_params = {}
    # get user input params
    
    user_params['inputDir'] = raw_input('Input Directory [Back-Pain/Texts.parsed]: ')
    user_params['outputDir'] = raw_input('\nOutput Directory [Back-Pain]: ')
    user_params['ngrams'] = raw_input('\nN-gram to find [Unigrams/Bigrams/Trigrams]: ')
    user_params['posEmotFile'] = raw_input('\nPositive Ngram File [Back-Pain/PosEmotionNgramFrequency.txt]: ')
    user_params['negEmotFile'] = raw_input('\nNegative Ngram File [Back-Pain/NegEmotionNgramFrequency.txt]: ')
    user_params['nGramsToExcludeFile'] = raw_input('\nNgram to Exclude File[ExcludeNGram.txt]: ')
    user_params['emotionWordsCnt'] = raw_input('\nHow many top emotion Words to Include: ')
    user_params['ngramCountFile'] = raw_input('\nTotal Ngrams Count File[TotalUnigramCount.txt/TotalBigramCount.txt/TotalTrigramCount.txt]: ')


    '''
    user_params['inputDir'] = "Acne/Texts.parsed"
    user_params['outputDir'] = "Acne"
    user_params['ngrams'] = "Trigrams"
    user_params['posEmotFile'] = "Acne/PosEmotionTrigramsFrequency.txt"
    user_params['negEmotFile'] = "Acne/NegEmotionTrigramsFrequency.txt"
    user_params['nGramsToExcludeFile'] = "excludeTrigrams.txt"
    user_params['emotionWordsCnt'] = 100
    user_params['ngramCountFile'] = "Acne/TotalTrigramCount.txt"
    '''
    if user_params['inputDir'] == '' or user_params['outputDir'] == '' or user_params['ngrams'] == '' or user_params['posEmotFile'] == '' or user_params['negEmotFile'] == '':
        print "Invalid values. Try again"
        sys.exit()
    return user_params



def dump_user_params(user_params):
    # dump user params for confirmation
    print 'Input Directory:    ' + user_params['inputDir']
    print 'Output Directory:   ' + user_params['outputDir']
    print 'N-grams:   ' + user_params['ngrams']
    print 'Positive Emotion File:   ' + user_params['posEmotFile']
    print 'Negative Emotion File:   ' + user_params['negEmotFile']
    print 'N-grams to Exclude File:   ' + user_params['nGramsToExcludeFile']
    print 'Number of top Ngrams to include:   ' + str(user_params['emotionWordsCnt'])
    print 'Total Ngram Count File:   ' + user_params['ngramCountFile']
    return




        
def main():
    user_params = get_user_params()
    dump_user_params(user_params)

    
   
        
    
    #countEmotionWords(emotionWordsDict, filesDir, outputDir)
    topEmotionWords = getTopEmotionWords(user_params['posEmotFile'], user_params['negEmotFile'],user_params['nGramsToExcludeFile'], int(user_params['emotionWordsCnt']), user_params['ngramCountFile'])
    #for temp in topEmotionWords:
    #    print temp + "\t" +  topEmotionWords[temp]
    findSentencesWithTopEmotionWords(topEmotionWords, user_params['inputDir'], user_params['outputDir'], user_params['ngrams'])
        
            

if (__name__ == "__main__"):
    main()   
    