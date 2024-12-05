# moat - Mother of all Tasks

This script is able to run Reportal Celery tasks.

## Running the script

Duplicate [.env.template](.env.template) to a file named .env and
fill all ENV vars for your needs:

```dotenv
# it will pause if total queued messages is greater than this
MAX_QUEUE_LOAD=500
# the frequency for checking the queue count
TRIGGER_QUEUE_COUNT=100
# Time in seconds between 2 consecutive tasks
BACKOFF_TIMER=1

MONGO_URI="mongodb+srv://{}@bmat-tvav-prod.yq6o5.mongodb.net/{}?retryWrites=true&w=majority"
MONGO_CREDENTIALS=CHANGEME:CHANGEME
MONGO_DB=CHANGEME

# User with permissions to send tasks to file-processor
CELERY_URI="amqp://{}@fast-rabbit.rmq.cloudamqp.com/file-processor"
CELERY_CREDENTIALS=CHANGEME:CHANGEME
CELERY_QUEUE=CHANGEME

# Output report
REPORTAL_URL=https://CHANGEME.bmat.com
# File with 1 ObjectID per line as str
INPUT_FILE_WITH_OBJECT_IDS=input.csv

# Uncomment the task and params of your choice
CHOSEN_TASK=CHANGEME
[...]  # Task params, uncomment the one you need
```

## Explaining the script

This script will:
1. Read the config passed by parameter or in the ENV
2. Connect to MongoDB + RabbitMQ
3. Read your `INPUT_FILE_WITH_OBJECT_IDS` line by line
4. Send 1 Celery task per MongoDocument using the lines in the previous steps as ObjectIds
5. Generate 2 reports:
    1. Error report with all issues found.
    2. Output report with ObjectIds + reportal url.

All of this while checking the number of messages in the queue every `TRIGGER_QUEUE_COUNT` iterations to never go
above `MAX_QUEUE_LOAD`.
