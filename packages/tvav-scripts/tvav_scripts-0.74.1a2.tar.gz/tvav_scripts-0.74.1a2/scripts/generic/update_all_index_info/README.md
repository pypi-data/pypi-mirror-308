# Update all index info

This script updates all `index_info.last_updated` for every MongoDB to a specific timestamp provided in the configuration.

For this script to work, please fill in the .env file:
```dotenv
MONGO__CREDS=changeme:changeme
# needed for the config, but will modify every DB
MONGO__DB_NAME=tv-av-prod

TIMESTAMP="2024-06-02 09:00:00"
```
