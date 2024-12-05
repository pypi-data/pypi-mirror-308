# V1 Reimport Reindex Script

## Description
This script was ported from [this snippet](https://bitbucket.org/bmat-music/workspace/snippets/LMq7Kb), 
and it is intended to automate the process of reimporting matches and resetting the elasticsearch index.

## How it works
This script uses a class `V1ReimportReindexScript` which has several methods to execute the reimport and reindex process. 
The significant steps are as follows:
- Read all necessary configurations from `.env` file. (check `.env.template`)
- Making connections to MongoDB and Celery.
- Fetching all the broadcasts. 
- Based on certain conditions, creating a chain of tasks and executing them to reimport matches and/or reset the index.

## Quickstart guide
### Prerequisites
- Python `<3.7`
- Install all dependencies from `requirement.txt`:
  - `pip install -r requirements.txt`
- To run the tests, also install dependencies from `test-requirements.txt`:
  - `pip install -r test-requirements.txt`
- Make sure to fill all the variables in `.env` file, the script relly on that.

### Running the script
In the `v1_reimport_reindex.py` file, change the flags of `populate_broadcasts` and `reset_index` based on your needs:
```python
...
if __name__ == "__main__":
    config = models.Config()  # Will load varibles from .env automatically
    script = V1ReimportReindexScript(config)
    script.run(populate_broadcasts=True, reset_index=True)  # flags to change
```
In this example, both `populate_broadcasts` and `reset_index` are set to `True`, which will result in making tasks for both reimporting matches and resetting index.

After that, run the script:
```shell
python v1_reimport_index.py
```

## Verifying the status
To verify whether the tasks ran successfully, do the following:
- Check the queues in RabbitMQ.
- Check the processor pod logs for `reset_index` tasks.
- Check the populate pod logs for `populate_broadcasts` tasks.
