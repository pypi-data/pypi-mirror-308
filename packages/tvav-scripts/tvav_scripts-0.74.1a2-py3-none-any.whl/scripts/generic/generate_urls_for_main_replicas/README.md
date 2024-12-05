# Generic - Generate Reportal URLs for Main Replicas

This script will connect to the MongoDB instance specified by `MONGO_URI`, fetch schedules that match the defined pipeline, 
generate Reportal APP URLs for each schedule and write them to a file called `reportal_urls.csv`.

## Setup and Execution:

1. Copy this repository to your local machine.
2. Make sure you have the required Python libraries installed. You may wish to create a virtual environment for this project. You can install the libraries using pip:

```shell
pip install -r requirements.txt
```

3. Create a file called `.env` located at the script root and define your environment variables in it. Include at least `MONGO_URI`, `START_DATE`, `END_DATE` following the `DATETIME_FORMAT -> %Y-%m-%d %H:%M:%S` and `REPORTAL_DOMAIN_NAME`.
4. To run the script, ensure you're in the same directory as the project and use the command:
```shell
python generate_urls_for_main_replicas.py
```

5. The generated URL file (_`reportal_urls.csv`_) can be found in the scripts's root directory. Each line in the CSV file corresponds to a unique Reportal URL.
