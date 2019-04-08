# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 01:32:41 2019

@author: Lenovo
"""



try:
    import argparse
    import os
    from gtts import gTTS
    import speech_recognition as sr
    from pygame import mixer
    import pyaudio
    import time
    import pickle
    import datetime
except ImportError as e:
    print(e)
    print("Check wether the package {} is properly installed...".format(e))


class Chatbot_Predict():
    
    def __init__(self):
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-m", "--model", required=True,
        	help="path to output trained model")
        self.ap.add_argument("-a", "--audiofile", required=True,
        	help="path to save audio file.")
        self.args = vars(self.ap.parse_args())
        self.speech_reg_obj = sr.Recognizer()
        self.microphone_source = 0
        self.audio = None
        self.date_and_time = datetime.datetime.now()
    
    def select_microphone_source(self):
        count = 0
        for micro_phone in sr.Microphone.list_microphone_names():
            print(str(count)+'.'+micro_phone)
            count += 1
        self.microphone_source = int(input("Please enter the number of " \
                                       "microphone which you like to use = "))
        return self.microphone_source
    
    def listen_audio(self, microphone_source):
        with sr.Microphone(device_index=microphone_source) as source:
            print("Say something!")
            self.speech_reg_obj.adjust_for_ambient_noise(source)
            self.audio = self.speech_reg_obj.listen(source)
        return self.audio
    
    def convert_speech_to_text(self, audio):
        try:
         print("Google Speech Recognition thinks you said --> " \
               + self.speech_reg_obj.recognize_google(self.audio))
         return self.get_reponse(audio)
        except sr.UnknownValueError as e:
            print(e)
            print("Google Speech Recognition could not understand audio." \
                  "Please say something to continue or say 'Bye' to end this" \
                  "conversation")
            self.listen_audio()
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition" \
                  "service; {0}. Please repeat  or say 'Bye' to end this." \
                  "conversation".format(e))
            self.listen_audio()
    
    def get_reponse(self, audio):
        if audio is not None:
            input_message = str(self.speech_reg_obj.recognize_google(audio))
            if input_message.strip().lower() not in ['bye', 'quit', 'stop', 
                                  'end', 'abort', 'shutdown']:    
                model = pickle.load(self.args['model'])
                reply = model.get_response(input_message)
                response_reply = str(reply)
                print(response_reply)
                return ['proceed', input_message, response_reply]
            else:
                print("Bye...")
                return ['abort']
    
    def get_text_to_speech(self, response_text):
        language = 'en'
        gtts_obj = gTTS(text=response_text, lang=language, slow=False)
        self.date_and_time = datetime.datetime.now().replace(' ', '_')
        gtts_obj.save(self.args['audiofile']+str(self.date_and_time)+".mp3")
        
    def play_response(self, reply):
        mixer.init()
        mixer.music.load(self.args['audiofile']+str(self.date_and_time)+'.mp3')
        mixer.music.play()        
        print('Darling: ', reply)


if __name__ == "__main__":
    response_text = None
    cb_test = Chatbot_Predict()
    while response_text is not 'abort':
        audio_source = cb_test.select_microphone_source()
        input_audio = cb_test.listen_audio(audio_source)
        reponse_in_text = cb_test.convert_speech_to_text(input_audio)
        response_text = reponse_in_text[0]
        if response_text is not 'abort':
            cb_test.get_text_to_speech(reponse_in_text[2])
            cb_test.play_response(reponse_in_text[2])
        
    