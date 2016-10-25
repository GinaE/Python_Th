

import random

all_questions = {
    "strong": "Do ye like yer drinks strong?",
    "salty": "Do ye like it with a salty tang?",
    "bitter": "Are ye a lubber who likes it bitter?",
    "sweet": "Would ye like a bit of sweetness with yer poison?",
    "fruity": "Are ye one for a fruity finish?"
}

ingredients = {
    "strong": ["glug of rum", "slug of whiskey", "splash of gin"],
    "salty": ["olive on a stick", "salt-dusted rim", "rasher of bcaon"],
    "bitter": ["shake of bitters", "splash of tonic", "twist of lemon peel"],
    "sweet": ["sugar cube", "spoonful of honey", "splash of cola"],
    "fruity": ["slice of orange", "dash of cassis", "cherry on top"]
}

# Ask all the questions about tastes



def Get_Preferences():
    preference = {}  # a dictionary. Will have the preferences, each flavor mapped to a boolean value.
    for question in all_questions:
        preference[question] = raw_input(all_questions[question])
        if preference[question] == 'yes':
            preference[question] = True
        else:
            preference[question] = False
    return preference

def Give_ingredients(preference):
    ing = []
    for question in all_questions:
        if preference[question] == True:
            ing.append(random.choice(ingredients[question]))
    return ing
	
preference = Get_Preferences()  # parenthesis, or preference will become another name for Get_preferences
a = Give_ingredients(preference)

for i in a:
    print "add: ", i

	
    
#    preference = raw_input(ingredients[question])

