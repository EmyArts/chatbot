# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 12:50:17 2018

@author: Emy Arts & Sophia Zell
"""
from telepot.loop import MessageLoop
import telepot
import nltk
import json
import os

nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('tagsets')

#bot = telepot.Bot('735651281:AAFrwg_8Q2hQ2KKZxg81k0pEsHFPvzyhaW8')
#print(bot.getMe())
ing_list = makeIngredientsList()

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
    ing_list = []
    for recipe_file in os.listdir("recipes"):
        recipe = json.loads(open("recipes/" + recipe_file).read())
        for ingredient in recipe['ingredients'].keys():
            ing_list.append(ingredient)
    return ing_list

def identifyRecipeFromIngredients(ingredients):
    return 2

def identifyRecipeFromTime(time):
    return 7

def identifyIngredientsInText(tagged):
    indices = intersectionNoun(ing_list, tagged)
    if len(indices) == 0:
        return None
    else:
        ingredients = []
        for i in indices:
            ingredients.append(tagged[i][0])
        return ingredients

def identifyTimeInText(tagged):
    time = ["minutes", "mins", "min", "h", "hour", "hours", "hrs" ]
    intersect = intersectionSimple(time, tagged)
    if intersect == -1:
        return None
    else:
        for i in range(0,intersect):
            if tagged[i][1] == "CD":
                return tagged[i][0] 
    return None

def intersectionSimple(lst1, tagged):
    for value in lst1:
        for tup in tagged:
            if value == tup[0].lower():
                return tagged.index(tup)
    return -1

def intersectionNoun(lst1, tagged):
    indices = set()
    for value in ing_list:
        for tup in tagged:
            if value == tup[0].lower() or "NN" in tup[1] and tup[0].lower() in value:
                indices.add(tagged.index(tup))
    return indices

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
        recipe = identifyRecipeFromIngredients(ingredients)
        return recipe
    return "HII"
  
print(respond( [('I', 'PRP'), ('want', 'VBP'), ('to', 'TO'), ('cook', 'VB'), (',', ','), ('but', 'CC'), ('I', 'PRP'), ('already', 'RB'), ('have', 'VBP'), ('celery', 'NN'), ('carrots', 'NN'), (',', ','), ('what', 'WP'), ('should', 'MD'), ('I', 'PRP'), ('make', 'VB'), ('?', '.')]))
#MessageLoop(bot, handle).run_as_thread()

"""Messages look like this: 
 {'message_id': 25, 
 'from': {'id': 271994095, 'is_bot': False, 'first_name': 'Posh', 'language_code': 'de'}, 
 'chat': {'id': 271994095, 'first_name': 'Posh', 'type': 'private'}, 
 'date': 1543493333, 
<<<<<<< HEAD
 'text': 'hiii'}
 
 tagged looks like this: 
 [('I', 'PRP'), ('want', 'VBP'), ('to', 'TO'), ('cook', 'VB'), (',', ','), ('but', 'CC'), ('I', 'PRP'), ('already', 'RB'), ('have', 'VBP'), ('celery', 'NN'), (',', ','), ('what', 'WP'), ('should', 'MD'), ('I', 'PRP'), ('make', 'VB'), ('?', '.')]
 
 """

