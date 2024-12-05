# Copy backup

This script will copy all documents matching a certain query from a collection from a source MongoDB
server into a target MongoDB server. This is useful if you want to create a quick backup of some docs
in production or move them between Backup Cluster and Prod Cluster or your local MongoDB instances.

For this script to work, please fill in the .env file:
```dotenv
ORIGIN_URI=mongodb+srv://{}@bmat-tvav-prod-backup.yq6o5.mongodb.net/{}?retryWrites=true&w=majority
TARGET_URI=mongodb+srv://{}@bmat-tvav-prod.yq6o5.mongodb.net/{}?retryWrites=true&w=majority
MONGO_USER=CHANGEME:CHANGEME
MONGO_DB='the db you want to copy'
MONGO_COL='the collection you want to copy'
MY_NAME='your name'
MAX_BATCH_SIZE=10000
QUERY={}
```
**Notice how the origin and target URI have 2x `{}`** this is because the script will try to run ''.format()
on both URIs with your MONGO_USER, but you can ignore it.