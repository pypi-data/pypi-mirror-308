


'''
	import goodest.besties.food_USDA.examples as USDA_examples
	walnuts_1882785 = USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	walnuts_1882785 = USDA_examples.retrieve ("branded/impossible_2468423.JSON")
	walnuts_1882785 = USDA_examples.retrieve ("branded/beet_juice_2642759.JSON")	
'''

import pathlib
from os.path import dirname, join, normpath
import json

def retrieve (path):
	this_directory = pathlib.Path (__file__).parent.resolve ()
	example_path = normpath (join (this_directory, path))
	
	with open (example_path) as FP:
		data = json.load (FP)

	return data
	

'''
	import goodest.besties.food_USDA.examples as USDA_examples
	USDA_examples.add ("branded/goodest_pizza_2672996.JSON", json.dumps ({}, indent = 4))
'''
def add (path, data):
	this_directory = pathlib.Path (__file__).parent.resolve ()
	example_path = normpath (join (this_directory, path))

	FP = open (example_path, "w")
	FP.write (data)
	FP.close ()
	

