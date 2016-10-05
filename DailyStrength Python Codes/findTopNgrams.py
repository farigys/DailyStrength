'''
Created on Dec 6, 2013

@author: bgyawali


this program reads the parsed texts and finds the top unigrams, bigrams and trigrams of the positive and negative emotions

'''

import os, sys, operator
import re
from nltk import bigrams, trigrams


def getTopEmotionNGrams(emotionWordsDict, filesDir, outputDir):
    print "finding top emotion words"
    posEmotionOnegramDict = {}
    negEmotionOnegramDict = {}
    posEmotionBigramDict = {}
    negEmotionBigramDict = {}
    posEmotionTrigramDict = {}
    negEmotionTrigramDict = {}
    fileCnt = 0
    
    ### these will be used to count the total number of unigrams, bigrams, or trigrams on all the files of a given condition. for example: total tokens in back pain condition 
    unigramCount = 0
    bigramCount = 0
    trigramCount = 0
    for textFile in os.listdir(filesDir):
        textFile = filesDir + "/" + textFile
        print "processing file " + textFile + ": " + str(fileCnt)
        if(os.path.isfile(textFile)):           
            openFile = open(textFile)
            sentences = openFile.readlines()
            for sen in sentences:
                if(sen.strip("\n").strip() != ''):
                    tokens = sen.strip("\n").strip().lower().split(" ")   ### unigram tokens
                    ml_bigram = bigrams(tokens)  ## bigrams
                    ml_trigram = trigrams(tokens)  ### trigrams
                    unigramCount += len(tokens)
                    bigramCount += len(ml_bigram)
                    trigramCount += len(ml_trigram)
                    for words in emotionWordsDict:  ### loop for each emotion words present in the LIWC dictionary
                        if(re.search('\*$', words)): ### if the emotijon word ends with *, then it means, there can be multiple words that match this expression. 
                            ### so go for a different appraoch 
                            wordsPattern = words[0:len(words)-1]
                            ## script to find one gram
                            for onegram in tokens:
                                if(re.match(wordsPattern,onegram)):
                                    if(emotionWordsDict[words] == 'positive'):
                                        posEmotionOnegramDict[onegram] = posEmotionOnegramDict.get(onegram, 0) + 1
                                    else:
                                        negEmotionOnegramDict[onegram] = negEmotionOnegramDict.get(onegram, 0) + 1
                            ## script to find bigrams
                            for bigram in ml_bigram:
                                if(re.match(wordsPattern,bigram[0]) or re.match(wordsPattern, bigram[1])):
                                    realBigram = bigram[0] + " " + bigram[1]
                                    if(emotionWordsDict[words] == 'positive'):
                                        posEmotionBigramDict[realBigram] = posEmotionBigramDict.get(realBigram, 0) + 1
                                    else:
                                        negEmotionBigramDict[realBigram] = negEmotionBigramDict.get(realBigram, 0) + 1
                            ## script to find trigrams
                            for trigram in ml_trigram:
                                if(re.match(wordsPattern,trigram[0]) or re.match(wordsPattern, trigram[1]) or re.match(wordsPattern, trigram[2])):
                                    realBigram = trigram[0] + " " + trigram[1] + " " + trigram[2]
                                    if(emotionWordsDict[words] == 'positive'):
                                        posEmotionTrigramDict[realBigram] = posEmotionTrigramDict.get(realBigram, 0) + 1
                                    else:
                                        negEmotionTrigramDict[realBigram] = negEmotionTrigramDict.get(realBigram, 0) + 1
                                        
                        else: ### this means the emotion word doesn't end with *. so this is a single regular emotion word. so do direct comparison. :)
                            wordsPattern = words
                            ## script to find one grams
                            for onegram in tokens:
                                    oneGramWord = onegram.rsplit('_', 1)[0]
                                    if(oneGramWord == wordsPattern):
                                        realBigram = bigram[0] + " " + bigram[1]
                                        if(emotionWordsDict[words] == 'positive'):
                                            posEmotionOnegramDict[onegram] = posEmotionOnegramDict.get(onegram, 0) + 1
                                        else:
                                            negEmotionOnegramDict[onegram] = negEmotionOnegramDict.get(onegram, 0) + 1
                            ## script to find bigrams
                            for bigram in ml_bigram:
                                    bigram0 = bigram[0].rsplit('_', 1)[0]
                                    bigram1 = bigram[1].rsplit('_', 1)[0]
                                    #print bigram0, bigram1
                                    if(bigram0 == wordsPattern or bigram1 == wordsPattern):
                                        realBigram = bigram[0] + " " + bigram[1]
                                        if(emotionWordsDict[words] == 'positive'):
                                            posEmotionBigramDict[realBigram] = posEmotionBigramDict.get(realBigram, 0) + 1
                                        else:
                                            negEmotionBigramDict[realBigram] = negEmotionBigramDict.get(realBigram, 0) + 1
                            ## script to find trigrams
                            for trigram in ml_trigram:
                                trigram0 = trigram[0].rsplit('_', 1)[0]
                                trigram1 = trigram[1].rsplit('_', 1)[0]
                                trigram2 = trigram[2].rsplit('_', 1)[0]
                                if(wordsPattern == trigram0 or wordsPattern == trigram1 or wordsPattern == trigram2):
                                    realBigram = trigram[0] + " " + trigram[1] + " " + trigram[2]
                                    if(emotionWordsDict[words] == 'positive'):
                                        posEmotionTrigramDict[realBigram] = posEmotionTrigramDict.get(realBigram, 0) + 1
                                    else:
                                        negEmotionTrigramDict[realBigram] = negEmotionTrigramDict.get(realBigram, 0) + 1
        fileCnt+=1
        
    ### sort positive and negative unigrams, bigrams, and trigrams in descendign order    
    sortedPosOnegramDict = sorted(posEmotionOnegramDict.items(), key=operator.itemgetter(1,0), reverse=True)
    sortedNegOnegramDict = sorted(negEmotionOnegramDict.items(), key=operator.itemgetter(1,0), reverse=True)
    sortedPosBigramDict = sorted(posEmotionBigramDict.items(), key=operator.itemgetter(1,0), reverse=True)
    sortedNegBigramDict = sorted(negEmotionBigramDict.items(), key=operator.itemgetter(1,0), reverse=True)
    sortedPosTrigramDict = sorted(posEmotionTrigramDict.items(), key=operator.itemgetter(1,0), reverse=True)
    sortedNegTrigramDict = sorted(negEmotionTrigramDict.items(), key=operator.itemgetter(1,0), reverse=True)
    
    
    ### write them in files
    emotionWordsFile = open(outputDir + "/PosEmotionUnigramsFrequency.txt", "w")
    for i in range(len(sortedPosOnegramDict)):
        emotionWordsFile.write(sortedPosOnegramDict[i][0] + "\t" + str(sortedPosOnegramDict[i][1]) + "\n")
        
    emotionWordsFile = open(outputDir + "/NegEmotionUnigramsFrequency.txt", "w")
    for i in range(len(sortedNegOnegramDict)):
        emotionWordsFile.write(sortedNegOnegramDict[i][0] + "\t" + str(sortedNegOnegramDict[i][1]) + "\n")
        
    emotionWordsFile = open(outputDir + "/PosEmotionBigramsFrequency.txt", "w")
    for i in range(len(sortedPosBigramDict)):
        emotionWordsFile.write(sortedPosBigramDict[i][0] + "\t" + str(sortedPosBigramDict[i][1]) + "\n")
        
    emotionWordsFile = open(outputDir + "/NegEmotionBigramsFrequency.txt", "w")
    for i in range(len(sortedNegBigramDict)):
        emotionWordsFile.write(sortedNegBigramDict[i][0] + "\t" + str(sortedNegBigramDict[i][1]) + "\n")
        
    emotionWordsFile = open(outputDir + "/PosEmotionTrigramsFrequency.txt", "w")
    for i in range(len(sortedPosTrigramDict)):
        emotionWordsFile.write(sortedPosTrigramDict[i][0] + "\t" + str(sortedPosTrigramDict[i][1]) + "\n")
        
    emotionWordsFile = open(outputDir + "/NegEmotionTrigramsFrequency.txt", "w")
    for i in range(len(sortedNegTrigramDict)):
        emotionWordsFile.write(sortedNegTrigramDict[i][0] + "\t" + str(sortedNegTrigramDict[i][1]) + "\n")        
 
 
    ## writing total number of tokens in a file       
    tokensFile = open(outputDir + "/TotalUnigramCount.txt","w")
    tokensFile.write("Unigrams count:\t" + str(unigramCount))  
    tokensFile = open(outputDir + "/TotalBigramCount.txt","w")
    tokensFile.write("Bigrams count:\t" + str(bigramCount))  
    tokensFile = open(outputDir + "/TotalTrigramCount.txt","w")
    tokensFile.write("Trigrams count:\t" + str(trigramCount))  
      


def get_user_params():
    user_params = {}
    # get user input params
    user_params['inputDir'] = raw_input('Input Directory [Back-Pain/Texts.parsed]: ')
    user_params['outputDir'] = raw_input('\nOutput Directory [Back-Pain]: ')
    user_params['affecWordsFile'] = raw_input('Affect Words File [AffectWords.txt]: ')


    if user_params['inputDir'] == '' or user_params['outputDir'] == '' or user_params['affecWordsFile'] == '':
        print "Invalid input directory or Output directory or affect words file. Try again"
        sys.exit()
    return user_params



def dump_user_params(user_params):
    # dump user params for confirmation
    print 'Input Directory:    ' + user_params['inputDir']
    print 'Output Directory:   ' + user_params['outputDir']
    print 'Affect words file:   ' + user_params['affecWordsFile']
    return




        
def main():
    user_params = get_user_params()
    dump_user_params(user_params)
    emotionWords = [line.strip() for line in open(user_params['affecWordsFile'])]
    emotionWordsDict = {}
    for temp in emotionWords:
        word, wordClass = temp.split("\t")
        emotionWordsDict[word]=wordClass
        
    #print len(emotionWordsDict)
   
        
    
    #countEmotionWords(emotionWordsDict, filesDir, outputDir)
    getTopEmotionNGrams(emotionWordsDict, user_params['inputDir'], user_params['outputDir'])
        
            

if (__name__ == "__main__"):
    main()   
    
 