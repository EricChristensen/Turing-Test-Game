import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np

class BotUtil:

    #what does nltk's word_tokenize do on a sentence?
    #what does nltk's stem do to a word?
    @staticmethod
    def clean_up_sentence(sentence):
        #this should not be part of this method. either there needs to be a
        #constructor or maybe these methods really are just for bot_model
        #and dont need to be in their own helper class
        stemmer = LancasterStemmer()
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
        return sentence_words

    # what are the words?
    # what is the 'sentence'
    @staticmethod
    def bow(sentence, words, show_details=False):
        sentence_words = BotUtil.clean_up_sentence(sentence)
        # bag of words
        bag = [0]*len(words)
        for s in sentence_words:
            for i,w in enumerate(words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)
        return (np.array(bag))
