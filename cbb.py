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
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn



nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('tagsets')
nltk.download('wordnet')
  

wnl = WordNetLemmatizer()
ingredientset = set()

def makeIngredientsSet():
    ing_set = set()
    for recipe_file in os.listdir("recipes"):
        recipe = json.loads(open("recipes/" + recipe_file).read())
        for ingredient in recipe['ingredients'].keys():
            ing_set.add(ingredient)
    return ing_set


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
                bot.sendMessage(senderid, reply)

def greeting(tagged):
    return None

def identifyRecipeFromIngredients(ingredients):
    rec_list = []
    for recipe_file in os.listdir("recipes"):
        recipe = json.loads(open("recipes/" + recipe_file).read())
        for rec_ingredient in recipe['ingredients'].keys():
            if rec_ingredient in ingredients:
                if not recipe['name'] in rec_list:
                    rec_list.append(recipe['name'])
    return rec_list

def identifyRecipeFromTime(time):
    rec_list = []
    for recipe_file in os.listdir("recipes"):
        recipe = json.loads(open("recipes/" + recipe_file).read())
        if time >= recipe['time']:
                rec_list.append(recipe['name'])
    return rec_list

def identifyIngredientsInText(tagged):
    ingInText = set() #set of ingredients in  text
    for tup in tagged:
        if isIngredient(tup[0]):
            ingInText.add(tup[0])
    return ingInText

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

def isIngredient(word):
    reject_synsets = ['meal.n.01', 'meal.n.02', 'dish.n.02', 'vitamin.n.01']
    reject_synsets = set(wn.synset(w) for w in reject_synsets)
    accept_synsets = ['food.n.01', 'food.n.02']
    accept_synsets = set(wn.synset(w) for w in accept_synsets)
    for word_synset in wn.synsets(word, wn.NOUN):
        all_synsets = set(word_synset.closure(lambda s: s.hypernyms()))
        all_synsets.add(word_synset)
        for synset in reject_synsets:
            if synset in all_synsets:
                return False
        for synset in accept_synsets:
            if synset in all_synsets:
                return True

def intersectionWord(lst1, tagged):
    indices = set()
    for value in ing_set:
        for tup in tagged:
            if "NN" in tup[1] and tup[0].lower() in value and len(tup[0]) > 1:
                indices.add(tagged.index(tup))
    return indices

def handle(msg):
    print(msg)
    chat(msg)
    
def processText(text):
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    #entities = nltk.chunk.ne_chunk(tagged)
    return tagged

def respond(tagged):
    greet = greeting(tagged)
    if not greet == None:
        return greet
    time = identifyTimeInText(tagged)
    if not time == None:
        return time
        recipe = identifyRecipeFromTime(time)
        return recipe
    ingredients = identifyIngredientsInText(tagged)
    if not ingredients == None:
        return ingredients
        recipe = identifyRecipeFromIngredients(ingredients)
        return recipe


ing_set = makeIngredientsSet()    
food = wn.synset('food.n.02')
foodlist = list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))
print(respond( [('I', 'PRP'), ('want', 'VBP'), ('to', 'TO'), ('cook', 'VB'), (',', ','), ('but', 'CC'), ('I', 'PRP'), ('already', 'RB'), ('have', 'VBP'), ('celery', 'NN'), ('carrots', 'NN'), (',', ','), ('what', 'WP'), ('should', 'MD'), ('I', 'PRP'), ('make', 'VB'), ('?', '.')]))
print(ing_set)

#bot = telepot.Bot('735651281:AAFrwg_8Q2hQ2KKZxg81k0pEsHFPvzyhaW8')
#print(bot.getMe())
#print(ing_list)
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

