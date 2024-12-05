# Regexp finder

This script will search for regular expressions among all files under `PATH_DIR` and output the results
in a `PATH_DIR\out\` folder, storing the results for each file in a filename sharing the same name
preceded by `parsed_`.

For this script to work, please fill in the .env file:
```dotenv
# Please, use an absolute path, cur dir is inside the docker container
PATH_DIR="/src/scripts/regexp_finder/"
REG_EXP=^your_expression_[0-9a-f]{2}_example$
```