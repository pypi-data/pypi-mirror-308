# get_sigpool_list_for_vericast_customer


Use this script to get a JSON file with a list of sigpools for the Vericast customer name provided.


## How it works

Queries Vericast API to get the `customer_id` and then the sigpool list.

Saves the results in a JSON file.

## How to use

Duplicate `.env.template` into `.env` and fill the `CUSTOMER_NAME` env variable with your Vericast customer name.
