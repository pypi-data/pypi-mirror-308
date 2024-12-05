# Fix ASRUN codes for Eurosport 

This script is updating `epg_famille` and `epg_produit` and `epg_type` fields in Schedules with specified tag.

We need this script because ASRUN provider hasn’t yet stablized the ASRUN code generation and this has ripple effect in Eurosport Reportal and DIP4 generation.

More details here https://bmat-music.atlassian.net/browse/TVAV-9122


### Parameters

You can update the .env to execute the script with the parameters you want. 

Remember to set up the parameter ``MONGO_URI``.

Tag and new fields values can be specified in the .env file.
