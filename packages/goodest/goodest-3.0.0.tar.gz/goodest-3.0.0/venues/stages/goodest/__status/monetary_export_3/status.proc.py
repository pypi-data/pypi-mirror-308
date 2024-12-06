



'''
	mongo connection strings
		
		DB: goodest
			
			collection: 
				cautionary_ingredients
				essential_nutrients
'''

'''
	goodest_1 adventures monetary saves export --version 3
'''


import pathlib
from os.path import dirname, join, normpath
import sys
def add_paths_to_system (paths):
	this_directory = pathlib.Path (__file__).parent.resolve ()	
	for path in paths:
		sys.path.insert (0, normpath (join (this_directory, path)))
	

add_paths_to_system ([
	'../../../../stages'
])


#/
#
#
from goodest._essence import build_essence
#
#
import biotech
#
#
import rich
#
#
import json
import pathlib
from os.path import dirname, join, normpath
import os
import sys
import subprocess
#
#\

#----
#
name = "goodest"
this_directory = pathlib.Path (__file__).parent.resolve ()
venues = str (normpath (join (this_directory, "../../../../../venues")))
this_stage = str (normpath (join (venues, f"stages/{ name }")))


monitors = str (normpath (join (this_directory, f"monitors")))

if (len (sys.argv) >= 2):
	glob_string = monitors + '/' + sys.argv [1]
	db_directory = False
else:
	glob_string = monitors + '/**/money_status_*.py'
	db_directory = normpath (join (this_directory, "DB"))

print ("glob string:", glob_string)
#
#----

# os.system ("goodest_1 adventures monetary saves import --version 3 --drop")
os.system ("goodest_1 adventures monetary saves-G2 extract --version status_1")

bio = biotech.on ({
	"glob_string": glob_string,
	
	"simultaneous": True,
	"simultaneous_capacity": 50,

	"time_limit": 60,

	"module_paths": [
		normpath (join (venues, "stages"))
	],

	"relative_path": monitors,
	
	"db_directory": db_directory,
	
	"aggregation_format": 2
})


bio ["off"] ()


def turn_off ():
	goodest_binary_path = str (normpath (join (this_directory, "../../__dictionary/goodest_1")))
	subprocess.Popen (
		[ f"{ goodest_binary_path }",  "off" ],
		cwd = this_directory
	)


import time
time.sleep (2)

rich.print_json (data = bio ["proceeds"] ["alarms"])
rich.print_json (data = bio ["proceeds"] ["stats"])



