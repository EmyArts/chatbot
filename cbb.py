# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 12:50:17 2018

@author: Emy Arts & Sophia Zell
"""
from telepot.loop import MessageLoop
import telepot
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

bot = telepot.Bot('735651281:AAFrwg_8Q2hQ2KKZxg81k0pEsHFPvzyhaW8')
print(bot.getMe())

def chat(dic):
    if 'from' in dic.keys():
        sender = dic['from']
        if 'id' in sender.keys():
            senderid = sender['id']
            print(senderid)
            if 'text' in dic.keys():
                tagged = processText(dic['text'])
                reply = respond(tagged)
                bot.sendMessage(senderid, reply)

def greeting(tagged):
    return "HI"

def makeIngredientsList():
    return 5

def checkForIngredients(ingredients):
    return 4

def identifyRecipeFromIngredients(ingredients):
    return 2

def identifyRecipeFromTime():
    return 7

def identifyIngredientsInText(tagged):
    return "HI"

def identifyTimeInText(tagged):
    return "HI"

def handle(msg):
    print(msg)
    chat(msg)
    
def processText(text):
    tokens = nltk.word_tokenize(text)
    print(tokens)
    tagged = nltk.pos_tag(tokens)
    print(tagged)
    #entities = nltk.chunk.ne_chunk(tagged)
    #print(entities)
    return tagged

def respond(tagged):
    greet = greeting(tagged)
    if not greet == None:
        return greet
    time = identifyTimeInText(tagged)
    if not time == None:
        return time
    ingredients = identifyIngredientsInText(tagged)
    if not ingredients == None:
        return ingredients
    return "HII"
    
MessageLoop(bot, handle).run_as_thread()

"""Messages look like this: 
 {'message_id': 25, 
 'from': {'id': 271994095, 'is_bot': False, 'first_name': 'Posh', 'language_code': 'de'}, 
 'chat': {'id': 271994095, 'first_name': 'Posh', 'type': 'private'}, 
 'date': 1543493333, 
 'text': 'hiii'}"""