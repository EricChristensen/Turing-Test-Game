import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import random
import tensorflow as tf
import tflearn
import numpy as np
import json
import pickle
import sys

# State variables:
# documents, words, classes, training_x, training_y, model
class BotModel:

    def __init__(self, name):
        self.name = name
        self.filepath = "./bots/" + self.name + "/" + self.name
        self.intents_path = self.filepath + "intents.json"
        print("build bot")

    def get_intents(self):
        with open(self.intents_path) as json_data:
            intents = json.load(json_data)
        return intents

    # Extracts the features from the json file
    # Features are word, classes, and documents
    # Only the words and classes are used for the actual bot
    # The documents are used for generating the training data
    def extract_features(self):
        self.words = []
        self.classes = []
        self.documents = []
        ignore_words = ['?']
        intents = self.get_intents()
        for intent in intents["intents"]:
            for pattern in intent["patterns"]:
                # tokenize the words in the sentence
                w = nltk.word_tokenize(pattern)
                # add the words to our words list
                self.words.extend(w)
                # add to our documents a tuple with the words and the tag
                self.documents.append((w,intent["tag"]))
                # add to our class list the tag if it isnt already there
                if intent["tag"] not in self.classes:
                    self.classes.append(intent["tag"])

        self.words = [stemmer.stem(w.lower()) for w in self.words if w not in ignore_words]
        self.words = sorted(list(set(self.words)))
        self.classes = sorted(list(set(self.classes)))

    # Sets the training_x and training_y values of the state
    # not sure what training_x and training_y really are
    def generate_training_data(self):
        training = []
        output = []
        output_empty = [0] * len(self.classes)

        # our training set is a bag of words for each sentence
        for doc in self.documents:
            # initialize empty bag of words for the particular document
            bag = []
            # list of tokenized words for the pattern
            pattern_words = doc[0]
            # stem each word
            pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
            # create our bag of words array
            for w in self.words:
                bag.append(1) if w in pattern_words else bag.append(0)

            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1

            training.append([bag, output_row])

        random.shuffle(training)
        training = np.array(training)

        self.training_x = list(training[:,0])
        self.training_y = list(training[:,1])

    def save_model(self):
        tf.reset_default_graph()
        # build the neural network, no idea how this works
        net = tflearn.input_data(shape=[None, len(self.training_x[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(self.training_y[0]), activation='softmax')
        net = tflearn.regression(net)

        # define model and set up tensor board
        model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
        model.fit(self.training_x, self.training_y, n_epoch=1000, batch_size=8, show_metric=True)
        model.save(self.filepath + 'model.tflearn')

    # Should save the various features and training data.
    # Features are the words and classes
    # Training data has x and y component and is training_x and training_y
    #
    def save_features(self):
        pickle.dump({'words':self.words, 'classes':self.classes, 'training_x':self.training_x, 'training_y':self.training_y }, open(self.filepath + "training_data", "wb"))

    def run(self):
        self.extract_features()
        self.generate_training_data()
        self.save_model()
        self.save_features()

if __name__ == "__main__":
    print("begin!")
    # sys.argv is the list of arguments passed to the python
    bot_model = BotModel(sys.argv[1])
    bot_model.run()
    print("the end!")
