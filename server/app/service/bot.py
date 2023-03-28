import logging
import numpy as np
import spacy
from sklearn.neural_network import MLPClassifier
from joblib import load

class Chatbot():
    
    path_classifier = 'app/service/classifier.model'
    path_responses = 'app/service/responses.data'
    path_tags = 'app/service/tags.data'
    path_word_list = 'app/service/word_list.data'
    
    classifier = None
    responses = None
    tags = None
    
     
    def __init__(self, threshold = 0.2, fallback = 'fallback', greeting = 'greeting'):

        self.nlp = spacy.load("en_core_web_sm")

        self.classifier = load(self.path_classifier)
        self.responses = load(self.path_responses)
        self.tags = load(self.path_tags)
        self.word_list = load(self.path_word_list)
        
        self.threshold = threshold #when below threshold chatbot returns a fallback answer because of the lacking confidence
        self.fallback = fallback #name of fallback tag
        self.greeting = greeting
    
    def lemmatizer(self, text):
        doc = self.nlp(text)
        return [d.lemma_ for d in doc]
        
    def get_tag_from_prediction(self, result, threshold):
        max_proba = np.max(result)
        if max_proba < threshold:
            return self.fallback
        predicted_tag = self.tags[np.argmax(result)]
        return predicted_tag
        
    def log_predictions(self, input_text, prediction_tag, probability, prediction_tag_if_not_fallback, response):
        logging.basicConfig(filename='app/service/logs/chatbot_predictions.log', encoding='utf-8', level=logging.DEBUG)
        s = f'{input_text}, {prediction_tag}, {probability}, {prediction_tag_if_not_fallback}, {response}'
        logging.debug(s)
    
    def bag_of_words(self, sentence):
        bog = np.zeros(len(self.word_list), dtype=np.float32)
        for idx, word in enumerate(self.word_list):
            if word in sentence:
                bog[idx] = 1
        return bog
    
    def pipe_new_input(self, text):
        if text == '': #otherwise error
            logging.info('Empty input')
            text = ' '
        text = self.lemmatizer(text)
        bog = self.bag_of_words(text)
        x = bog.reshape(1, bog.shape[0])
        return x
    
    def get_random_response_from_tag(self, tag):
        
        return np.random.choice(self.responses[tag])
    
    def predict(self, input_text, log_status = True):
        x = self.pipe_new_input(input_text)
        
        result = self.classifier.predict_proba(x)
        max_proba = np.max(result)
        
        predicted_tag = self.get_tag_from_prediction(result, self.threshold)
        predicted_tag_except_fallback = self.get_tag_from_prediction(result, 0.0)
        
        response = self.get_random_response_from_tag(predicted_tag)
        
        if log_status:
            self.log_predictions(input_text,
                                    predicted_tag,
                                    max_proba,
                                    predicted_tag_except_fallback,
                                    response)
        return response
    
    def get_greeting(self):
        return self.get_random_response_from_tag(self.greeting)