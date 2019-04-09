# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 00:15:13 2019

@author: Vino
"""

try:
    import argparse
    from chatterbot.trainers import ListTrainer
    from chatterbot import ChatBot
    import os
    import pickle
except ImportError as e:
    print(e)
    print("Check wether the package {} is properly installed...".format(e))


class Chatbot_Trainer():

    def __init__(self):
        # construct the argument parser and parse the arguments
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-d", "--dataset", required=True,
                             help="path to input dataset")
        self.ap.add_argument("-m", "--model", required=False,
                             help="path to output trained model")
        self.args = vars(self.ap.parse_args())
        self.cb_obj = ChatBot('Bot')

    def train_model(self):
        trained_data = []
        self.cb_obj.set_trainer(ListTrainer)
        for files in os.listdir(self.args['dataset']):
            data = open(self.args['dataset'] + files, 'r').readlines()
            trained_data.append(self.cb_obj.train(data))
        return trained_data

    def save_model(self, trained_data):
        pickle.dump(trained_data, open(self.args['model'], 'wb'))


if __name__ == "__main__":
    cb_training_obj = Chatbot_Trainer()
    trained_data = cb_training_obj.train_model()
    cb_training_obj.save_model(trained_data)


