# generate_reports


Needed for YLE-1816.

This script is called from Jenkins to trigger report generation on YLE PROD / STG.

Final reports will be delivered to **REPORT_SUBMIT_NAMESPACE**

##  Instructions

Just replace the .env file with your needed values.

```dotenv
MONGO_URI=mongodb+srv://{}@bmat-tvav-prod.yq6o5.mongodb.net/{}?retryWrites=true&w=majority
MONGO_USER=CHANGEME:CHANGEME
MONGO_DB=CHANGEME
CELERY_BROKER=amqp://CHANGEME:CHANGEME@fast-rabbit.rmq.cloudamqp.com/file-processor?ssl=true
CELERY_QUEUE=CHANGEME

USER="bmat_processor"
START_TIME="2022-01-25 00:00:00"
END_TIME="2023-06-15 23:59:59"
REPORT_FORMAT="CHANGEME"
REPORT_SUBMIT_NAMESPACE="CHANGEME"
```