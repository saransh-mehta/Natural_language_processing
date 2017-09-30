import os
import nltk
import numpy as np
import string
from difflib import SequenceMatcher
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import random
import pandas as pd


translator = str.maketrans('','', string.punctuation)

def readCorpus(fileName, x, y, z):

    df = pd.read_csv(fileName)

    for question in df['questions']:
        
        question = question.translate(translator)
        x.append(question.lower())

    for classes in df['class']:

        y.append(classes)

    for subClass in df['sub_class']:

        z.append(subClass)

    return x, y, z
'''
def correctAbreviations(inp, dicti):
    
    tokens = str.split(inp, ' ')
    for word in tokens:
        if word in dicti.keys():
            inp = inp.replace(word, dicti[word])
    
    return inp
'''
def inpPart2(inp, listId):
    
    stemmer = LancasterStemmer()
    
    keywords = []
    prekeywords = nltk.word_tokenize(inp)
    
    for word in prekeywords:
        if word not in stopwords.words('english'):
            
            #stemmed = stemmer.stem(word)
            keywords.append(word)
            
    #print(keywords)
    maxRatio = 1
    maxScore = keywords.__len__() + maxRatio
    
    scoreList = []
    
    for tuple in listId:
        
        score = tuple[0]
    
        for word in keywords:
            
            #print(x[tuple[1]])
            findRes = x[tuple[1]].find(word)
            #findRes = re.findall(word, x[tuple[1]])
            #print(findRes)
            
            if findRes != -1:
                
                score = score + 1
                
        scoreList.append((score, tuple[1]))
    #print(scoreList)
    return scoreList

def EmptyList(inp):
    
    keywords = []
    prekeywords = nltk.word_tokenize(inp)
    
    for word in prekeywords:
        if word not in stopwords.words('english'):
            keywords.append(word)
    
    #score = 0
    possibleQuestions = []
    
    for word in keywords:
        
        for i in range(x.__len__()):
            
            findRes = x[i].find(word)
            #findRes = re.findall(word, x[i])
            #print(findRes)
            
            if findRes != -1:
                
                possibleQuestions.append(y[i])
                
    if len(possibleQuestions) >3:
        
        del possibleQuestions[3:]
                
    if possibleQuestions != []:
        
        print('possible classes')
        for classes in possibleQuestions:
            print(classes)
            
    else:
        
        print("couldn't classify !")

def Response(scoreList):
    
    responseScore = max(tuple[0] for tuple in scoreList)
    #print(responseScore)
    
    responseIdList = []
    for tuple in scoreList:
        
        # this is made to handle if responsescore is same, it will return the last one.
        
        if tuple[0] == responseScore:
            responseIdList.append(tuple[1])
         
    #print(responseIdList)
    responseId = random.choice(responseIdList)
    #print(responseId)

    return y[responseId], z[responseId]

def inpPart1(inp):
    
    ratioList = []
    for i in range(x.__len__()):
        a = SequenceMatcher(None, inp, x[i]).ratio()
        if a >= 0.7:
            ratioList.append( (a, i) )
    #listId = [(r, ratioList.index(r)) for r in ratioList if r >= 0.7]
    #print(ratioList)
    return ratioList

def keywordsReturn(inp):

    tokenKeywords = []
    tokens = nltk.word_tokenize(inp)
    posTagged = nltk.pos_tag(tokens)

    for posPair in posTagged:

        if posPair[0] not in stopwords.words('english'):
            tokenKeywords.append(posPair)
    return tokenKeywords

x = []
y = []
z = []

csvFilePayzello = 'intent_payzello_bot_nlp.csv'

x, y, z = readCorpus(csvFilePayzello, x, y, z)
while True:
    inp = input("enter message : ")
    inp = inp.lower()
    
    #inp = correctAbreviations(inp, dictionary)
    
    listId = inpPart1(inp)
    
    if listId != []:
        
        scoreList = inpPart2(inp, listId)
        responseClass, responseSubClass = Response(scoreList)
        keywordsToSend = keywordsReturn(inp)

        print('class : {} '.format(responseClass))
        print('subclass : {}'.format(responseSubClass))
        print('Keyword to Ashis: {}'.format(keywordsToSend))
    else:
        
        EmptyList(inp)
        print('Keyword to Ashis: {}'.format(keywordsToSend))