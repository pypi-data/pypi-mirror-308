

'''
	python3 insurance.py "besties/food_USDA/interpret/packageWeight/interpret/status_1.py"
'''

'''
	Sometimes when multiple values, one of the values is rounded.
		prefer grams or prefer ounces?
'''

import json

from goodest.besties.food_USDA.nature_v2._interpret.packageWeight.interpret import interpret_amount

from goodest.mixes.show.variable import show_variable

def check_1 ():	
	proceeds = interpret_amount ("12 fl oz/355 mL")
	calculated = proceeds.calculated;
	listed = proceeds.listed;

	assert (calculated ['liters'] == '71/200')
	assert (calculated ['fluid ounces'] == '19984723346456576/1664840044750517')

def check_2 ():	
	proceeds = interpret_amount ("355 mL")
	calculated = proceeds.calculated;
	listed = proceeds.listed;

	show_variable ({
		"calculated": calculated
	})

	assert (calculated ['liters'] == '71/200')
	assert (calculated ['fluid ounces'] == '19984723346456576/1664840044750517')

		
	
checks = {
	"check 1": check_1,
	"check 2": check_2	
}