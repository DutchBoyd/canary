# implementation of sentiment analysis based on:
# http://nealcaren.web.unc.edu/an-introduction-to-text-analysis-with-python-part-3/
#
# Canary 2018
###############################################################################
from __future__ import print_function
import os.path
import urllib
import json

from string import punctuation

class TextAnalyzer():
    positive_words = []
    negative_words = []

    def __init__(self):
        files=['negative.txt','positive.txt']
        path='http://www.unc.edu/~ncaren/haphazard/'
        for file_name in files:
            if not os.path.isfile(file_name):
                urllib.urlretrieve(path+file_name,file_name)
        self.positive_words = open("positive.txt").read().split('\n')
        self.negative_words = open("negative.txt").read().split('\n')

    def analyzeText(self, originalText):
        positive_counter = 0.0
        negative_counter = 0.0
        text=originalText.lower()
        for p in list(punctuation):
            text=text.replace(p,'')

        words=text.split(' ')

        for word in words:
            if word in self.positive_words:
                positive_counter += 1
            elif word in self.negative_words:
                negative_counter += 1
        return {
                "text":originalText,
                "positive":positive_counter/len(words),
                "negative":negative_counter/len(words)
            }

    def analyzeListOfText(self, listOfText):
        results = []
        for text in listOfText:
            results.append(self.analyzeText(text))
        return results

if __name__ == "__main__":

    file_name='obama_tweets.txt'
    if not os.path.isfile(file_name):
        path='http://www.unc.edu/~ncaren/haphazard/'
        urllib.urlretrieve(path+file_name,file_name)

    tweets = open("obama_tweets.txt").read().split('\n')
    analyzer = TextAnalyzer()
    results = analyzer.analyzeListOfText(tweets)
    counter = 1
    for result in results:
        print (str(counter)+' '+json.dumps(result))
        counter += 1
