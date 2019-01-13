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
import time as t
import random 
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from word2number import w2n



nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('tagsets')
nltk.download('wordnet')
  

wnl = WordNetLemmatizer()

def chat(dic):
    if 'from' in dic.keys():
        sender = dic['from']
        if 'id' in sender.keys():
            senderid = sender['id']
            if 'text' in dic.keys():
                tagged = processText(dic['text'])
                respond(senderid, tagged)
 
def checkIngredients(i1, i2):
    tokens1 = nltk.word_tokenize(i1)
    tokens2 = nltk.word_tokenize(i2)
    for t1 in tokens1:
        for t2 in tokens2:
            if wnl.lemmatize(t1) == wnl.lemmatize(t2):
                return True
    return False

def handle(msg):
    print(msg)
    chat(msg)
               
def identifyRecipeFromName(tagged):
    rec = None
    sentence = stringOutOfTagged(tagged)
    for recipe_file in os.listdir("recipes"):
        recipe = json.loads(open("recipes/" + recipe_file).read())
        name = recipe['name']
        if name.lower() in sentence.lower():
            return recipe        
    return rec

def identifyRecipeFromID(tagged):
    rec = None
    recid = -1
    for ta in tagged:
        if ta[1] == 'CD':
            recid = ta[0]
    for recipe_file in os.listdir("recipes"):
        recipe = json.loads(open("recipes/" + recipe_file).read())
        rid = recipe['id']
        try:
            if int(recid) == rid:
                return recipe
        except:
            recid = w2n.word_to_num(recid)
            if int(recid) == rid:
                return recipe
    return rec

def identifyRecipeFromIngredients(ingredients):
    rec_arr = []
    for recipe_file in os.listdir("recipes"):
        recipe = json.loads(open("recipes/" + recipe_file).read())
        for rec_ingredient in recipe['ingredients'].keys(): 
            for i in ingredients:
                if checkIngredients(rec_ingredient, i):
                    rec_arr.append(recipe['name'] + " (" + str(recipe['id']) + ")")
    if len(ingredients) > 1:
        rec_arr = onlyMultipleInArray(rec_arr)
        return rec_arr
    return set(rec_arr)

def identifyRecipeFromTime(time):
    rec_list = []
    for recipe_file in os.listdir("recipes"):
        recipe = json.loads(open("recipes/" + recipe_file).read())
        if int(time) >= int(recipe['time']):
                rec_list.append(recipe['name'] + " (" + str(recipe['id']) + ")")
    return rec_list

def identifyIngredientsInText(tagged):
    ingInText = set() #set of ingredients in  text
    for tup in tagged:
        if isIngredient(tup[0]):
            ingInText.add(wnl.lemmatize(tup[0].lower()))
    return ingInText

def identifyTimeInText(tagged):
    time_m = ["minutes", "mins", "min"]
    time_h = ["h", "hour", "hours", "hrs"]
    intersect_m = intersectionSimple(time_m, tagged)
    intersect_h = intersectionSimple(time_h, tagged)
    if intersect_m == -1 and intersect_h == -1:
        return None
    elif not intersect_m == -1:
        for i in range(0,intersect_m):
            if tagged[i][1] == "CD":
                try:
                    time_val = int(tagged[i][0])
                except:
                    time_val = w2n.word_to_num(tagged[i][0])
                return time_val
    elif not intersect_h == -1:
        for i in range(0,intersect_h):
            if tagged[i][1] == "CD":
                try:
                    time_val = int(tagged[i][0])
                except:
                    time_val = w2n.word_to_num(tagged[i][0])
                return time_val*60
    return None

def identifyBye(tagged):
    if not intersectionComplex(["bye"], tagged) == -1:
        return True
    return False

def identifyThanks(tagged):
    if not intersectionComplex(["thank", "thx"], tagged) == -1:
        return True
    return False

def identifyYesNo(tagged):
    if 'yes' in tagged[0][0].lower() or 'okay' in tagged[0][0].lower() or 'yeah' in tagged[0][0].lower() or 'sure' in tagged[0][0].lower():
        return True
    return False

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

def intersectionSimple(lst1, tagged):
    for value in lst1:
        for tup in tagged:
            if value == tup[0].lower():
                return tagged.index(tup)
    return -1

def intersectionComplex(lst1, tagged):
    for value in lst1:
        for tup in tagged:
            if value in tup[0].lower():
                return tagged.index(tup)
    return -1

def listToString(l):
    string = ""
    for ll in l:
        string = string + str(ll) + """
"""
    return string
    

def makeIngredientsSet():
    ing_set = set()
    for recipe_file in os.listdir("recipes"):
        recipe = json.loads(open("recipes/" + recipe_file).read())
        for ingredient in recipe['ingredients'].keys():
            ing_set.add(ingredient)
    return ing_set    

def onlyMultipleInArray(array):
    unique = set()
    multi = set()
    for a in array:
        if a in unique:
            unique.remove(a)
            multi.add(a)
        else:
            unique.add(a)
    return multi

def prettyIngredientList(ingdict):
    pretty = ""
    for key in ingdict.keys():
        measurements = str(ingdict[key][0])
        if(not str(ingdict[key][1]) == ""):
            measurements =  measurements + """ """ + str(ingdict[key][1])
        pretty = pretty + measurements + """ """ +  key + """
"""
    return pretty

def processText(text):
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    #entities = nltk.chunk.ne_chunk(tagged)
    return tagged

def respond(senderid, tagged):
    global status
    global current_recipe
    skip = False
    found = False
    thx = identifyThanks(tagged)
    bye = identifyBye(tagged)
    recipes = {}
    if thx:
        sendResponse(senderid, str("You're welcome!"))
        skip = True
    if bye:
        sendResponse(senderid, str("Good Bye!"))
        status = 0
        skip = True
    if status == 0 and not skip:
        current_recipe = None
        sendResponse(senderid, str("Hi!"))
        status = 1
    if status == 1:
        #checks if recipe name is mentioned
        recipe = identifyRecipeFromName(tagged)
        if not recipe == None:
            #get ingredient list of recipe
            current_recipe = recipe
            sendFoundRecipe(senderid, recipe)
            status = 2
            skip = True
        #checks if recipe ID is mentioned
        recipe = identifyRecipeFromID(tagged)
        if not recipe == None:
            #get ingredient list of recipe
            current_recipe = recipe
            sendFoundRecipe(senderid, recipe)
            status = 2
            skip = True
        #checks if time is mentioned
        if not skip:
            time = identifyTimeInText(tagged)
            if not time == None:
                skip = True
                recipes = identifyRecipeFromTime(time)
                if len(recipes) > 0:
                    found = True
            #checks if ingredients are mentioned  
            ingredients = identifyIngredientsInText(tagged)
            if (not ingredients == None) and len(ingredients) > 0:
                skip = True
                if not found:
                    recipes = identifyRecipeFromIngredients(ingredients)
                    found = True
                else:
                    rec2 = identifyRecipeFromIngredients(ingredients)
                    if len(rec2) > 0:
                        print(set(recipes))
                        print(rec2)
                        recipes = set(recipes).intersection(rec2)
            if found:
                sendFoundRecipes(senderid, recipes)
            elif skip: 
                sendResponse(senderid, "Sorry, I did not find any recipes meeting your requirements.")
            else:
                sendResponse(senderid, "How can I help you today?")
    if not skip and (status == 2 or status == 3):
        word = identifyYesNo(tagged)
        if not word and status == 2: 
            sendResponse(senderid, "Do you still want to continue with this recipe?")
            status = 3
        elif not word and status == 3:
            sendResponse(senderid, "K bye!")
            status = 0
        elif word:
            sendResponse(senderid, str(current_recipe["procedure"]))
            sendBonAppetit(senderid)
            status = 0

def sendBonAppetit(senderid):
    array = ["Bon Appétit", "Guten Appetit", "Eet Smakelijk", " Enjoy your meal", "Buon appetito", "Vel bekomme", "Bom apetite", "¡Buen apetito", "Smaklig måltid"]
    r = random.randint(0, len(array))
    sendResponse(senderid, array[r] + "!")
    
def sendFoundRecipe(senderid, recipe):
    sendResponse(senderid, prettyIngredientList(recipe["ingredients"]))
    sendResponse(senderid, "This recipe is for " + str(current_recipe["portions"]) + " portions.")
    sendResponse(senderid, "Do you have all the ingredients for this recipe?")
            
def sendFoundRecipes(senderid, recipes):
    recString = listToString(recipes)
    sendResponse(senderid, "I have found the following recipes: " + recString)
    sendResponse(senderid, " Which one would you like to make? (please answer by using the name or the ID of the recipe)")

def sendResponse(senderid, message):
    t.sleep(1)
    bot.sendMessage(senderid, str(message))

def stringOutOfTagged(tagged):
    string = ""
    for ta in tagged:
        string = string + " " + ta[0]
    return string
       
    
#ing_set = makeIngredientsSet()    
food = wn.synset('food.n.02')
foodlist = list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))
#print(respond( [('I', 'PRP'), ('want', 'VBP'), ('to', 'TO'), ('cook', 'VB'), (',', ','), ('but', 'CC'), ('I', 'PRP'), ('already', 'RB'), ('have', 'VBP'), ('celery', 'NN'), ('carrots', 'NN'), (',', ','), ('what', 'WP'), ('should', 'MD'), ('I', 'PRP'), ('make', 'VB'), ('?', '.')]))
#print(ing_set)
status = 0
current_recipe = None
reply_keyboard = [['Yes', 'No']]
bot = telepot.Bot('735651281:AAFrwg_8Q2hQ2KKZxg81k0pEsHFPvzyhaW8')
print(bot.getMe())
#print(ing_set)
MessageLoop(bot, handle).run_as_thread()

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

