
import heapq, random
from collections import Counter
import re
from prettytable import PrettyTable

def replaceLeastWordsWithUNK(text,word1,word2,word3):
    replacements={
        word1 : 'UNK',
        word2 : 'UNK',
        word3 : 'UNK',
    }
    newText = (' '.join(map(lambda w: replacements.get(w, w), text)))
    createSmoothingBigram(newText)

def createSmoothingBigram(data):
    listOfSmoothedBigrams = []
    smoothedBigramCounts = {}
    smoothedUnigramCounts = {}

    words = re.findall(r"[\w']+|[.!?]", data)

    for i in range(len(words)):
        if i < len(words) - 1:

            listOfSmoothedBigrams.append((words[i], words[i + 1]))

            if (words[i], words[i + 1]) in smoothedBigramCounts:
                smoothedBigramCounts[(words[i], words[i + 1])] += 1
            else:
                smoothedBigramCounts[(words[i], words[i + 1])] = 1

        if words[i] in smoothedUnigramCounts:
            smoothedUnigramCounts[words[i]] += 1
        else:
            smoothedUnigramCounts[words[i]] = 1

    calcSmoothingProb(data, listOfSmoothedBigrams, smoothedUnigramCounts, smoothedBigramCounts)
    return  listOfSmoothedBigrams, smoothedUnigramCounts, smoothedBigramCounts

def calcSmoothingProb(data,listOfSmoothedBigrams, smoothedUnigramCounts, smoothedBigramCounts):
    listOfProbSmoothedBigram = {}
    smoothedValue= 0.5
    vValue = 10

    for bigram in listOfSmoothedBigrams:
        word1 = bigram[0]
        word2 = bigram[1]

        listOfProbSmoothedBigram[bigram] = (smoothedBigramCounts.get(bigram)+smoothedValue) / (smoothedUnigramCounts.get(word1)+smoothedValue*vValue)

    print(' ')
    maxSmoothedBigram(data,listOfProbSmoothedBigram,listOfSmoothedBigrams,smoothedUnigramCounts)
    print(' ')

    return listOfProbSmoothedBigram

def maxSmoothedBigram(data,listOfProbSmoothedBigram, listOfSmoothedBigrams,smoothedUnigramCounts):
    bigramsAndAmounts = {}
    listOfMostUsedValues = []

    BigramCounter = Counter(listOfSmoothedBigrams)


    for key, value in BigramCounter.items():
        if value not in bigramsAndAmounts:
            bigramsAndAmounts[value] = [key]
        else:
            bigramsAndAmounts[value].append(key)

    listOfMostUsedValues.append(heapq.nlargest(10, bigramsAndAmounts.keys()))
    counter = 0
    print('The Most Used Smoothed Bigrams and Smoothed Probabilities: ')
    t = PrettyTable(['Bigram:', 'Amount', 'Probability'])
    for i in listOfMostUsedValues:
        for j in i:
            a = list(bigramsAndAmounts.values())[list(bigramsAndAmounts.keys()).index(j)]
            for k in a:
                if (k[0] == '.' and k[1] == '.'):
                    counter -= 1
                else:
                    b = list(listOfProbSmoothedBigram.values())[list(listOfProbSmoothedBigram.keys()).index(k)]
                    if(j>1):
                      t.add_row([k, j, b])
            counter += len(a)
            if (counter >= 10):
                break
    print(t)
    findSmoothedProbabilityOfSentence(data,listOfProbSmoothedBigram, listOfSmoothedBigrams,smoothedUnigramCounts)

def compareAndReplaceUnkWord(sentence,text):
    splittedSentence = re.findall(r"[\w']+|[.!?]", sentence)
    splittedText=re.findall(r"[\w']+|[.!?]", text)
    wordsChangeToBe =[]
    for i in range(len(splittedSentence)):
        d= splittedSentence[i]
        counter = 0
        for j in range(len(splittedText)):
            e= splittedText[j]
            if (splittedSentence[i]==splittedText[j]):
                counter +=1
        if(counter==0):
            if splittedSentence[i] not in wordsChangeToBe:
               wordsChangeToBe.append(splittedSentence[i])
    return replaceWords(wordsChangeToBe, splittedSentence)

def replaceWords(wordsChangeToBe, sentence):
    for i in range(len(wordsChangeToBe)):
        for j in range(len(sentence)):
            if (wordsChangeToBe[i] == sentence[j]):
                sentence[j]= 'UNK'
    return sentence

def findSmoothedProbabilityOfSentence(text, listOfProbSmoothedBigram,listOfSmoothedBigrams,smoothedUnigramCounts):
    probability= 1
    smoothedProbabilityOfZeroBigrams =0
    smoothedValue = 0.5
    vValue = 10
    sentence = input('Enter a sentence')
    modifySentence = compareAndReplaceUnkWord(sentence, text)
    listOfSmoothedBigramsofSentence = []
    for i in range(len(modifySentence)):
        if i < len(modifySentence) - 1:
            listOfSmoothedBigramsofSentence.append((modifySentence[i], modifySentence[i + 1]))

    for i in listOfSmoothedBigramsofSentence:
        try:
           a= list(listOfProbSmoothedBigram.values())[list(listOfProbSmoothedBigram.keys()).index(i)]
           probability = probability*a
        except:
             smoothedProbability = (smoothedProbabilityOfZeroBigrams + smoothedValue) / (
             smoothedUnigramCounts.get(i[0]) + smoothedValue * vValue)
             probability= probability*smoothedProbability
    print('')
    print('Probability of the sentence : ' , probability)
    enterAgain(text, listOfProbSmoothedBigram, listOfSmoothedBigrams, smoothedUnigramCounts)

def enterAgain(text, listOfProbSmoothedBigram,listOfSmoothedBigrams,smoothedUnigramCounts):
    return findSmoothedProbabilityOfSentence(text, listOfProbSmoothedBigram,listOfSmoothedBigrams,smoothedUnigramCounts)




