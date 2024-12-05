# Bitbucket script

Perform project wide operations using Bitbucket API.

## How to use

Duplicate the `.env.template` file to `.env` and fill all the variables to fit your needs.

- `URL, APP_USERNAME, APP_PASSWORD, WORKSPACE, PROJECT` are used to connect to Bitbucket API.
- `REPOS_TO_CHECK_TXT` is used to filter the repos. Should be a plain text file in this directory with 1 repo name per line.
- `UPDATE_FN_NAME` is used to update every repo. Should be a string with the name of one method in `update_methods.py`.

After running the script a new file `stats.csv` will be created with some useful messages about your update attempt.

## Can I add more update methods?

Of course!

Just ensure all functions follow `UpdateFn` protocol.

```python
URL="https://api.bitbucket.org/"
APP_USERNAME="CHANGEME"
APP_PASSWORD="CHANGEME"
WORKSPACE="bmat-music"
PROJECT="TVAV"

# this needs to be a method present in `update_methods.py`
UPDATE_FN_NAME="add_main_branch_restrictions"

# optional
REPOS_TO_CHECK_TXT="repositories.txt"
```
