





# goodest


## Rules
This is a mix because it has a frontend build.  
The frontend licenses seem unrestrictive and can be found at:  
```
goodest/frontend_licenses.csv
goodest/frontend_licenses_summary.csv
```

Original bits in the PyPI module are subject to the rules that can be found at:
```
goodest/[Rules]/Rules.E.HTML
```

	
## Obtain
```
[prompt] apt install git python3-pip curl -y
[prompt] pip install goodest
[prompt] goodest adventures squishy build
```

## (optional) obtain mongo
https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/   


---	

## Tutorial
This opens an HTML quay.
```
[prompt] goodest tutorial
```

---	

## Essence
This needs to be somewhere closer to "/" than
where the goodest process is started.


```
[file] goodest_essence.py
```
```
import json
fp = open ("/online/ridges/goodest/ridges.JSON", "r")
ridges = json.loads (fp.read ())
fp.close ()

def crate (the_path):
	from os.path import dirname, join, normpath
	import sys
	import pathlib
	this_directory = pathlib.Path (__file__).parent.resolve ()
	
	return str (normpath (join (this_directory, the_path)))



essence = {
	"mode": "business",
	"alert_level": "caution",
	
	"ventures": {
		"path": crate (
			"[records]/ventures_map.JSON"
		)
	},
	
	"monetary": {
		"URL": "mongodb://0.0.0.0:39000/",
					
		"saves": {
			"path": crate ("monetary/_saves")
		}
	},
	"sanique": {
		"protected_address_key": "1234"
	},
	"USDA": {
		"food": ridges ["USDA"] ["food"]
	},
	"NIH": {
		"supp": ridges ["NIH"] ["supp"]
	}
}
```

## optional, build local HAProxy HTTPS Certificates
```
goodest adventures demux_hap build_unverified_certificates
```

---	

## on
The ventures are "Sanic", "HAProxy", and "Mongo"
```
goodest ventures on
```

---

## import the database data
```
goodest_1 adventures monetary saves import --version 10 --drop
```

---

## URLs
```
0.0.0.0:8000/docs/swagger
```

---



## contacts
Graceful.Bryonics@Proton.me





