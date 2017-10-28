# DB data predictive analytics for car2go

## insights into data

Total 12 columns in the data, namely:
ZUGEREIGNIS_ZUGGATTUNG;ZUGEREIGNIS_ZUGNUMMER;ZUGEREIGNIS_DS100;ZUGEREIGNIS_TYP;ZUGEREIGNIS_SOLLZEIT;ZUGEREIGNIS_ISTZEIT;QUELLE_SENDER;EINGANGSZEIT;SERVICE_ID;NAME;LAENGE;BREITE;geo

### ZUGEREIGNIS_ZUGNUMMER
- Total 897 unique train number
	- we can use this param to cluster trains

### ZUGEREIGNIS_SOLLZEIT
- Total 15 days of data
	- starting from 1 sep 2017 to 15 sep 2017
		- total 454828 trip by the entire s-bahn fleet in stuttgart (including all kinds of trains and routes within the city)

### ZUGEREIGNIS_ISTZEIT
- same as above

### delay
- I basically tried to see the distribution of the delay for the fleet
	- I found
		- min delay = 0
		- max delay = 1144 mins
		- avg delay = 1.09155 mins
		- median of delay = 0 min ()
	- detailed histogram stored in the folder
