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
                reply = processText(dic['text'])
                bot.sendMessage(senderid, reply)

def handle(msg):
    print(msg)
    chat(msg)
    
def processText(text):
    tokens = nltk.word_tokenize(text)
    print(tokens)
    tagged = nltk.pos_tag(tokens)
    print(tagged)
    entities = nltk.chunk.ne_chunk(tagged)
    print(entities)
    
    if text == 'hi':
        return 'Hello, how can I help you?'
    else:
        return 'Yooo'
    
MessageLoop(bot, handle).run_as_thread()

"""Messages look like this: 
 {'message_id': 25, 
 'from': {'id': 271994095, 'is_bot': False, 'first_name': 'Posh', 'language_code': 'de'}, 
 'chat': {'id': 271994095, 'first_name': 'Posh', 'type': 'private'}, 
 'date': 1543493333, 
 'text': 'hiii'}"""