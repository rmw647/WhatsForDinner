#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 08:51:56 2017

@author: rebeccaward

Backend functionality of web app.

Programmatically calls out to several recipe services and randomly generates
dinner suggestions.
"""

from bs4 import BeautifulSoup
import random
import requests


#### Simply recipes parsing ####

simply_recipes = 'http://www.simplyrecipes.com/index/'
resp = requests.get(simply_recipes).text
soup = BeautifulSoup(resp, 'html.parser')
# get a list of the main ingredients in the index
ingredients = soup.find(id="taxonomy-main-ingredient")
ingredients = ingredients.find_all('a')
main_ingredients = []
for ingredient in ingredients:
    main_ingredients.append(ingredient.get_text())

# pick the main ingredients you want
###### THIS SHOULD BE DONE IN GUI! ######
my_ingredient = 'no response'
print("\nWhat protein do you want to eat tonight?\n")
print('\n'.join(main_ingredients))
my_ingredient = input("Please enter the main ingredient you want in your tummy!\n"
                      "(Press Enter if you want me to pick for you!)\n").capitalize()
if my_ingredient == '':
    my_ingredient = random.choice(main_ingredients)
elif not my_ingredient in main_ingredients:
    print("\nDude!!!! You need to pick one of the ingredients in the list!")
    my_ingredient = input("Enter an ingredient FROM THE LIST:\n").capitalize()
    if not my_ingredient in main_ingredients:
        print("\nThis is why we can't have nice things. {} is not on the list.\n"
              "I'll pick for you.\n".format(my_ingredient.capitalize()))
        my_ingredient = random.choice(main_ingredients)
if my_ingredient == 'Vegetables':
    print("Ok, it's your life, but I think you're going to be hungry.\n")

first_url = 'http://www.simplyrecipes.com/recipes/ingredient/' + my_ingredient

resp = requests.get(first_url).text
                   
soup = BeautifulSoup(resp, 'html.parser')

all_recipes = soup.find_all('li', itemtype="http://schema.org/Recipe")

recipe_list = []

for recipe in all_recipes:
    info = {}
    info['name'] = recipe.h2.get_text()
    info['description'] = recipe.find(itemprop="description").get_text().strip()
    info['link'] = recipe.a["href"]
    recipe_list.append(info)
    
my_dinner = random.choice(recipe_list)
print("\nCongrats! You're making {} for dinner!\n".format(my_dinner["name"]))
print("You're gonna love it! How do I describe it? It's like... {}\n".format(
        my_dinner["description"]))
print("You can get all the deets here: {}".format(my_dinner["link"]))