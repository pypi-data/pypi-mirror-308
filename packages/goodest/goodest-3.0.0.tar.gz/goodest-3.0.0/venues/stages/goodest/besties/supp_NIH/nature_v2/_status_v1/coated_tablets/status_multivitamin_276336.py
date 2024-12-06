

'''
	python3 status.proc.py besties/supp_NIH/nature/_status/coated_tablets/status_multivitamin_276336.py
'''

#----
#
import goodest.besties.supp_NIH.nature_v2 as supp_NIH_nature_v2
import goodest.besties.supp_NIH.examples as NIH_examples
from goodest.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts
#
import json
import rich
#
#----

def check_1 ():	
	supp_1 = supp_NIH_nature_v2.create (
		NIH_examples.retrieve ("coated tablets/multivitamin_276336.JSON")
	)
	
	print (json.dumps (supp_1, indent = 4))
	
	def add (path, data):
		import pathlib
		from os.path import dirname, join, normpath
		this_directory = pathlib.Path (__file__).parent.resolve ()
		example_path = normpath (join (this_directory, path))
		FP = open (example_path, "w")
		FP.write (data)
		FP.close ()
		
	add ("status_multivitamin_276336_nature.JSON", json.dumps (supp_1, indent = 4))
	
	
	vitamin_A = seek_name_or_accepts (
		grove = supp_1 ["essential nutrients"] ["grove"],
		name_or_accepts = "vitamin A"
	)
	
	rich.print_json (data = vitamin_A) 
	
	assert (
		vitamin_A ["natures"] [0] ["measures"] ["mass + mass equivalents"] ["per form"] ["grams"] ["fraction string"] ==
		"3/2000"
	)
	assert (
		vitamin_A ["natures"] [0] ["measures"] ["mass + mass equivalents"] ["per package"] ["grams"] ["fraction string"] ==
		"27/200"
	)
	
	
	#
	#	https://dsld.od.nih.gov/label/276336
	#
	#	Vitamin A: 
	#		per form:		1500				mcg RAE 
	#			3/2000
	#
	#		per package:	1500 * 90 = 135000
	#			27/200
	#
	#
	
	
	return;
	
checks = {
	"check 1": check_1
}