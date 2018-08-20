import pickle
import tflearn
import json
import nltk
import random
import numpy as np
from nltk.stem.lancaster import LancasterStemmer
import tensorflow as tf
from botutil import BotUtil

class ChatBot:
    def __init__(self, name):
        self.name = name
        self.filepath = "./bots/" + self.name + "/" + self.name
        self.intents_path = self.filepath + 'intents.json'
        self.stemmer = LancasterStemmer()
        self.load_features()
        self.load_model()

    # hmm this is interesting... the bot has features? the bot is aware of the features...
    # it is the part of its brain that figures out how it classifies things. It is its memory
    # and its meaning. Should this stay within the bot? Yes for now...But this might not
    # be specific just to bots. This might be
    def load_features(self):
        data = pickle.load(open(self.filepath + "training_data", "rb"))
        self.words = data['words']
        self.classes = data['classes']
        self.training_x = data['training_x']
        self.training_y = data['training_y']

    # this should stay because the bot has a model. what model does the bot have?
    # well the bot has this model...
    def load_model(self):
        tf.reset_default_graph()
        #nueral net stuff
        net = tflearn.input_data(shape=[None, len(self.training_x[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(self.training_y[0]), activation='softmax')
        net = tflearn.regression(net)

        # Define model and setup tensorboard
        self.model = tflearn.DNN(net, tensorboard_dir=self.filepath + 'tflearn_logs')
        model_path = self.filepath + 'model.tflearn'
        self.model.load(model_path)

    def get_intents(self):
        with open(self.intents_path) as json_data:
            intents = json.load(json_data)
        return intents

    # this needs the model so it is unlikely it should be refactored out into a helper
    # the bot classifies. The bot responds. The bot shouldn't know about bag of words though...
    # the bot has a model
    def classify(self, sentence):
        ERROR_THRESHOLD = 0.25
        # generate probabilities from the model
        # results = self.model.predict([self.bow(sentence, self.words)])[0]
        results = self.model.predict([BotUtil.bow(sentence, self.words)])[0]
        # filter out predictions below a threshold
        results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append((self.classes[r[0]], r[1]))
        # return tuple of intent and probability
        return return_list

    def response(self, sentence, userID='123', show_details=False):
        results = self.classify(sentence)
        # if we have a classification then find the matching intent tag
        if results:
            intents = self.get_intents()
            # loop as long as there are matches to process
            while results:
                for i in intents['intents']:
                    # find a tag matching the first result
                    if i['tag'] == results[0][0]:
                        # a random response from the intent
                        return random.choice(i['responses'])

                results.pop(0)
