







#----
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
#
#
from goodest._essence import retrieve_essence, build_essence
#from .check_key import check_key
#
#----

def hype_technicians_inventory_recipes (packet):
	blue_print = packet ["blue_print"]	
	
	@blue_print.route ("/Recipes/insert_1")
	@openapi.parameter ("opener", str, "header")
	@openapi.description ("""
		
		Crafting Zone :: Unfinished
	
	""")
	async def addresses_staff_goodest_inventory_recipes_insert_1 (request):
		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status
	
		essence = retrieve_essence ()

		#lock_status = check_key (request)
		#if (lock_status != "unlocked"):
		#	return lock_status

		#return sanic.json (essence)
	
	
