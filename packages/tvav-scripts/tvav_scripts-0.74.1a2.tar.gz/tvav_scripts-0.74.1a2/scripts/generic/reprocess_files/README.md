# reprocess_files

This is task can be used to reprocess files for both Celery and Kafka.

## How it works

Loads a list of file ids from a CSV file.

Fetches each file from DB and guesses whether it should go through Kafka or Celery for
re-processing.

Then iterates through every File id:

- Fetches it from DB.
- Triggers re-process for it using the guessed method.
- Waits for `BACKOFF_TIMER` seconds every `MAX_BATCH_SIZE` files re-processed.

## How to make it work

Duplicate the `.env.template`, name it as `.env` and fill the env variables for your use case.

Not all variables are used every time.
For example, if the guessed method is Celery, then we do not use Kafka username nor password
and viceversa.
