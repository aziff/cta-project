* ---------------------------------------------------------------------------- *
* Code to clean june2015 bus data to be used in python
* Takes in: 		dirty .csv of bus data
* Exports: 			clean .csv 
* Original version:	January 16, 2016
* Current version: 	January 16, 2016
* ---------------------------------------------------------------------------- *

cd ~/Desktop/fun/cta-project

import delim using "june2015", clear delim("|")

* ---------------------------------------------------------------------------- *

split v3, parse(" ")

gen date = date(v31, "YMD")
format date %d

split v32, parse(":")
destring v321 v322, replace
gen time = v321 * 60 + v322

local vars_to_drop v3 v31 v32 v321 v322
drop `vars_to_drop'

rename routes171and172busstoparrivaltim route
rename v2 bus
rename v4 stopID

* ---------------------------------------------------------------------------- *

export delim using "cleaned-june2015", replace delim(",")
