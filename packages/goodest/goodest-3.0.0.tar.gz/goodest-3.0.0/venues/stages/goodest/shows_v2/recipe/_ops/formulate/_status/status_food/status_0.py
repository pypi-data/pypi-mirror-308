
'''
	python3 status.proc.py shows_v2/recipe/_status/status_food/status_0.py
'''

#----
#
import goodest.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import goodest.besties.food_USDA.examples as USDA_examples	
import goodest.besties.food_USDA.nature_v2 as food_USDA_nature_v2
import goodest.mixes.insure.equality as equality
#
from goodest.shows_v2.recipe._ops.formulate import formulate_recipe
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts	
#
#
from copy import deepcopy
from fractions import Fraction
import json
#
#----


def check_1 ():
	walnuts_1882785 = food_USDA_nature_v2.create (
		USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	)
	
	'''
		recipe_1: {
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						#
						#	424.0762244 grams
						#						
						"fraction string": "47746738154613173415299/112589990684262400000"
					}
				}
			},
			"energy": {
				"per recipe": {
					"food calories": {
						#
						#	3082.66 food calories
						#
						"fraction string": "154133/50"
					}
				}
			}
		}
	'''	
	recipe_1 = formulate_recipe ({
		"natures_with_amounts": [
			[ walnuts_1882785, 1 ]
		]
	})
	
	assert ("cautionary ingredients" in recipe_1)
	assert ("natures" in recipe_1 ["cautionary ingredients"])
	
	assert (
		recipe_1 ["essential nutrients"] ["measures"] ==
		walnuts_1882785 ["essential nutrients"] [ "measures" ]
	), [
		recipe_1 ["essential nutrients"] ["measures"],
		walnuts_1882785 ["essential nutrients"] [ "measures" ]
	]
	

	recipe_2 = formulate_recipe ({
		"natures_with_amounts": [
			[ walnuts_1882785, 2 ]
		]
	})
	assert (
		recipe_2 ["essential nutrients"] ["measures"] ==
		{
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						#
						#	424.0762244 grams	
						#		-> 848.1524488 = 47746738154613173415299/56294995342131200000
						#						
						"fraction string": "47746738154613173415299/56294995342131200000",
						'scinote string': '8.4815e+2'
					}
				}
			},
			"energy": {
				"per recipe": {
					"food calories": {
						#
						#	3082.66 food calories
						#		-> 6165.32 = 154133/25
						#
						"fraction string": "154133/25",
						'scinote string': '6.1653e+3'
					}
				}
			}
		}
	), recipe_2 ["essential nutrients"] ["measures"]
	
	
	
checks = {
	"check 1": check_1
}