


import goodest.measures._interpret.unit_kind as unit_kind
import goodest.measures.energy.swap as energy_swap
import goodest.measures.mass.swap as mass_swap
import goodest.measures.number.decimal.reduce as reduce_decimal
import goodest.measures.number.sci_note_2 as sci_note_2


from goodest.mixes.show.variable import show_variable


from fractions import Fraction

def calc_mass (
	amount_per_package__from_portion,
	unit_name,		
			
	USDA_food_nutrient,
	mass_and_volume,
	
	records = 1
):

	mass_plus_mass_eq_per_package__from_portion = amount_per_package__from_portion
	
	if (records >= 1):
		show_variable ({
			"mass_plus_mass_eq_per_package__from_portion": {
				"var": mass_plus_mass_eq_per_package__from_portion,
				"float": float (mass_plus_mass_eq_per_package__from_portion)
			}
		}, mode = "pprint")				
	
	
	mass_plus_mass_eq_per_package_in_grams = Fraction (mass_swap.start ([ 
		mass_plus_mass_eq_per_package__from_portion, 
		unit_name 
	], "grams"))
	
	return {
		"mass + mass equivalents": {
			"per package": {
				"listed": [ 
					reduce_decimal.start (
						mass_plus_mass_eq_per_package__from_portion, 
						partial_size = 3
					), 
					unit_name 
				],
				"grams": {
					"scinote string": sci_note_2.produce (mass_plus_mass_eq_per_package_in_grams),
					"decimal string": reduce_decimal.start (
						mass_plus_mass_eq_per_package_in_grams, 
						partial_size = 3
					),
					"fraction string": str (mass_plus_mass_eq_per_package_in_grams)
				}
			}
		}
	}