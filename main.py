import re
import ngram
import smoothedNgram

def split_into_sentences(text):
   text = text.lower()
   sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
   getSentences(sentences,text)
   return sentences

def getTextWithoutSpaces(text):
    withoutLineBreaks = text.replace("\n", "")
    withoutSpaces = re.sub(' +', ' ', withoutLineBreaks)
    return withoutSpaces

def getSentences(sentences,text):
    data = re.findall(r'\b[a-zA-Z]+|[.!?]', text)
    unique_words = set(data)
    sentenceCounter=0
    wordCounter=0
    for i in sentences:
        sentenceCounter += 1
        i = i.lower()
        words = i.split()
        wordCounter += len(words)
    print('Total sentence in the text : ' + str(sentenceCounter-1))
    print('Total word in the text : ' + str(wordCounter))
    print('Unique word number : ' + str(len(unique_words)-1))


def getText():
    file = open("hw01_FireFairies.txt")
    data = file.read()
    return data


def listResults():
    print('')
    split_into_sentences(getText())
    print('')
    words,listOfBigrams, unigramCounts, bigramCounts = ngram.createBigram(getTextWithoutSpaces(getText()))
    listOfProbBigram, listOfBigrams, listOfProbUnigram, words = ngram.calcBigramProb(words, listOfBigrams, unigramCounts, bigramCounts)
    words, flipped = ngram.maxUnigram(listOfProbBigram, listOfBigrams, listOfProbUnigram, words)
    ngram.findLeastValues(words, flipped)


if __name__ == '__main__':
   listResults()
