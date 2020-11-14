import heapq, random
import re
from collections import Counter

from prettytable import PrettyTable


import smoothedNgram


def __init__():
    pass


def createBigram(data):
    listOfBigrams = []
    bigramCounts = {}
    unigramCounts = {}
    text = data.lower()
    words= re.findall(r'\b[a-zA-Z]+|[.!?]', text)

    for i in range(len(words)):
        if i < len(words) - 1:

          listOfBigrams.append((words[i], words[i + 1]))

          if (words[i], words[i + 1]) in bigramCounts:
              bigramCounts[(words[i], words[i + 1])] += 1
          else:
              bigramCounts[(words[i], words[i + 1])] = 1

        if words[i] in unigramCounts:
            unigramCounts[words[i]] += 1
        else:
            unigramCounts[words[i]] = 1


    return words,listOfBigrams, unigramCounts, bigramCounts


def calcBigramProb(words,listOfBigrams, unigramCounts, bigramCounts):
    listOfProbBigram = {}
    listOfProbUnigram = {}

    for bigram in listOfBigrams:
        word1 = bigram[0]
        word2 = bigram[1]
        listOfProbBigram[bigram] = (bigramCounts.get(bigram)) / (unigramCounts.get(word1))

    for unigram in words:
        word = unigram
        listOfProbUnigram[unigram]=(unigramCounts.get(word)) / len(words)

    print(' ')

    return listOfProbBigram, listOfBigrams,listOfProbUnigram,words

def maxUnigram(listOfProbBigram,listOfBigrams,listOfProbUnigram, words):
    listOfHighestValues = []
    flipped = {}
    counter = 0
    for key, value in listOfProbUnigram.items():
        if key == '.':
            print('')
        elif value not in flipped:
            flipped[value] = [key]
        else:
            flipped[value].append(key)
    listOfHighestValues.append(heapq.nlargest(10, flipped.keys()))
    totalUnigram =Counter(words)
    print('The Most Used 10 Unigrams and Probabilities: ')
    t = PrettyTable(['Unigram:', 'Amount', 'Probability'])
    for i in listOfHighestValues:
        for j in i:
            a = list(flipped.values())[list(flipped.keys()).index(j)]
            b= totalUnigram[a[0]]
            counter += 1
            t.add_row([a,b,j])
    print(t)
    maxBigram(listOfProbBigram, listOfBigrams)

    return words, flipped


def findLeastValues(words,flipped):
    min_value = min(flipped.keys())
    z = list(flipped.values())[list(flipped.keys()).index(min_value)]
    word1 = z[0]
    word2=z[1]
    word3=z[2]
    a=words
    smoothedNgram.replaceLeastWordsWithUNK(words, word1, word2, word3)

def maxBigram(listOfProbBigram, listOfBigrams):
    bigramsAndAmounts = {}
    listOfMostUsedValues= []

    BigramCounter = Counter(listOfBigrams)

    for key, value in BigramCounter.items():
        if value not in bigramsAndAmounts:
            bigramsAndAmounts[value] = [key]
        else:
            bigramsAndAmounts[value].append(key)

    listOfMostUsedValues.append(heapq.nlargest(10, bigramsAndAmounts.keys()))
    counter=0
    print('The Most Used Bigrams and Probabilities: ')
    t = PrettyTable(['Bigram:', 'Amount', 'Probability'])
    for i in listOfMostUsedValues:
        for j in i:
            a= list(bigramsAndAmounts.values())[list(bigramsAndAmounts.keys()).index(j)]
            for k in a:
                if(k[0]=='.' and k[1]=='.'):
                    counter -=1
                else:
                  b = list(listOfProbBigram.values())[list(listOfProbBigram.keys()).index(k)]
                  if(j>1):
                    t.add_row([k, j, b])
            counter += len(a)
            if(j>1 and counter>=10):
                break
    print(t)

