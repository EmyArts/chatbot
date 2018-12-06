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
nltk.download('tagsets')

#bot = telepot.Bot('735651281:AAFrwg_8Q2hQ2KKZxg81k0pEsHFPvzyhaW8')
#print(bot.getMe())

def chat(dic):
    if 'from' in dic.keys():
        sender = dic['from']
        if 'id' in sender.keys():
            senderid = sender['id']
            print(senderid)
            if 'text' in dic.keys():
                tagged = processText(dic['text'])
                reply = respond(tagged)
                print(reply)
                #bot.sendMessage(senderid, reply)

def greeting(tagged):
    return None

def makeIngredientsList():
    return 5

def checkForIngredients(ingredients):
    return 4

def identifyRecipeFromIngredients(ingredients):
    return 2

def identifyRecipeFromTime(time):
    return 7

def identifyIngredientsInText(tagged):
    return "HI"

def identifyTimeInText(tagged):
    time = ["minutes", "mins", "min", "h", "hour", "hours", "hrs" ]
    #print(tagged[0][0])
    intersect = intersection(time, tagged)
    if intersect == -1:
        return None
    else:
        for i in range(0,intersect):
            if tagged[i][1] == "CD":
                return tagged[i][0] 
    return None

def intersection(lst1, lst2): 
    lst1 = [x.lower() for x in lst1]
    for value in lst1:
        for tup in lst2:
            if value == tup[0].lower():
                return lst2.index(tup)
    return -1         
    #lst3 = [value for value in lst1 if value in lst2] 
    #return lst3 

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
    return tokens

def respond(tagged):
    greet = greeting(tagged)
    if not greet == None:
        return greet
    time = identifyTimeInText(tagged)
    if not time == None:
        recipe = identifyRecipeFromTime(time)
        return recipe
    ingredients = identifyIngredientsInText(tagged)
    if not ingredients == None:
        return ingredients
    return "HII"
  
print(respond([('Hi', 'NNP'), (',', ','), ('I', 'PRP'), ('want', 'VBP'), ('to', 'TO'), ('cook', 'VB'), ('and', 'CC'), ('only', 'RB'), ('have', 'VBP'), ('20', 'CD'), ('Minutes', 'NNPS'), (',', ','), ('what', 'WP'), ('should', 'MD'), ('I', 'PRP'), ('make', 'VB'), ('?', '.')]))
#MessageLoop(bot, handle).run_as_thread()

"""Messages look like this: 
 {'message_id': 25, 
 'from': {'id': 271994095, 'is_bot': False, 'first_name': 'Posh', 'language_code': 'de'}, 
 'chat': {'id': 271994095, 'first_name': 'Posh', 'type': 'private'}, 
 'date': 1543493333, 
 'text': 'hiii'}
 
 tagged looks like this: 
 [('I', 'PRP'), ('want', 'VBP'), ('to', 'TO'), ('cook', 'VB'), (',', ','), ('but', 'CC'), ('I', 'PRP'), ('already', 'RB'), ('have', 'VBP'), ('celery', 'NN'), (',', ','), ('what', 'WP'), ('should', 'MD'), ('I', 'PRP'), ('make', 'VB'), ('?', '.')]
 
 """