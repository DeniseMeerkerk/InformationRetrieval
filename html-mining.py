#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:21:46 2019

@author: denise
"""

import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
#%% get links to recipes from home site.
def getLinks():
    local_filename, headers = urllib.request.urlretrieve('https://www.ah.nl/allerhande/recepten-zoeken?Nrpp=18226')
    html = open(local_filename)
    soup = BeautifulSoup(html, 'html.parser')
    links = ['hoi']
    for link in soup.find_all('a'):
        temp = link.get('href')
        if temp is not None:
            if re.match(r'^/allerhande/recept/', temp) and not re.match(links[-1], temp):
                links.append(temp)
    del(links[0])
    html.close()
    return links
#%% get recipe: safe link, title, ingredients and preperation
def getTitle(soup):
    title = soup.title.string[:-37]
    return title

def getIngredients(soup):
    temp = str(soup.head.script.next_sibling.next_sibling).split('\n')
    ingredientlist = []
    for ind, ingredient in enumerate(temp):
        if '"ingredients" : [ {' in temp[ind]:
            ind += 1
            while not  '} ],' in temp[ind]:
                if 'name' in temp[ind]:
                    ingredientlist.append(temp[ind][10:-1])
                ind +=1
            break
    return ' '.join(ingredientlist)

def getPreparation(soup):
    bereiding = str(soup.body.find('ol')).replace('<ol>','').replace('</ol>','').replace('<li>','').replace('</li>','')[1:-1]
    if bereiding == 'on':
        bereiding = str(soup.find("section", {"class": "preparation"}).findAll('p'))
        bereiding = bereiding.split('<p>')[-1]
        bereiding = bereiding.replace('</p>','')
    return bereiding

def main():
    recipes = []
    links = getLinks()
    for link in links:
        local_filename, headers = urllib.request.urlretrieve('https://www.ah.nl' + link)
        html = open(local_filename)
        soup = BeautifulSoup(html, 'html.parser')
        
        title = getTitle(soup)
        ingredients = getIngredients(soup)
        bereiding = getPreparation(soup)    
        
        recipes.append([link, title, ingredients, bereiding])
        html.close()
    return pd.DataFrame(recipes)
#%%
recipes = main()

export_csv = recipes.to_csv (r'/home/denise/Documents/Vakken/IR/export_recipes600-25-11.csv', index = None, header=False)

#%%
recipes5 = pd.read_csv (r'/home/denise/Documents/Vakken/IR/export_recipes600-24-11.csv', header=None)#zondag
#zaterdag
#vrijdag
#donderdag
recipes4 = pd.read_csv (r'/home/denise/Documents/Vakken/IR/export_recipes600-20-11.csv', header=None)#woensdag
recipes3 = pd.read_csv (r'/home/denise/Documents/Vakken/IR/export_recipes600-19-11.csv', header=None)#dinsdag
recipes2 = pd.read_csv (r'/home/denise/Documents/Vakken/IR/export_recipes600-18-11.csv', header=None)#maandag
#%%
frames = [recipes2, recipes3, recipes4, recipes5]

recipestotal = pd.concat(frames).sort_values(0)
dubbelen = recipestotal[recipestotal.duplicated(3,keep=False)]
sum(recipestotal.duplicated(0,keep=False))
#%% cleaning

recipestotal.dropna(inplace = True) #drop all lines with nan value
sub ='prijs per persoon'
sub2 = 'Je kunt dit gerecht helemaal maken met biologische ingrediënten.'
recipestotal["Indexes"]= recipestotal[3].str.find(sub) 
recipestotal = recipestotal[recipestotal.Indexes < 0]
recipestotal = recipestotal.drop('Indexes', axis=1)
recipestotal["Indexes"]= recipestotal[3].str.find(sub2)
recipestotal = recipestotal[recipestotal.Indexes < 0]
recipestotal = recipestotal.drop('Indexes', axis=1)

#%%
export_csv = recipestotal.to_csv (r'/home/denise/Documents/Vakken/IR/export_recipes2376-25-11.csv', index = None, header=False)
