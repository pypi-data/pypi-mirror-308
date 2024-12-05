# deploy script

Selectively deploy customer branches for any repo living in Bitbucket.

## How to use

Duplicate the `.env.template` file to `.env` and fill all the variables to fit your needs.

```python
URL="https://api.bitbucket.org/"
APP_USERNAME="CHANGEME"
APP_PASSWORD="CHANGEME"
WORKSPACE="bmat-music"
PROJECT="TVAV"

EDITOR="vi"
```

- `URL, APP_USERNAME, APP_PASSWORD, WORKSPACE, PROJECT` are used to connect to Bitbucket API.

Install the requirements.txt dependencies and run the script.

It will ask you for the repository name you want to deploy.

Then, your preferred editor (or `vi` by default) will open with a file containing all existing customer branches
in said repo.

Edit the file to keep only the customers you want to deploy and close the editor. The script will attempt to
create and merge PRs from repo main branch to those left in the file.

After running the script a new file `stats.csv` will be created with some useful output about your deploy attempt.
