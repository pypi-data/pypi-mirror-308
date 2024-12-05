# Improvements

## About customers already synced with master

- In the file (or maybe between 2 files), should split customers into:
    - customers that do not contain last commit in master
        - if not deleted by the user, create and merge PR
    - customers that do contain last commit in master
        - if not deleted by the user, push an empty commit to the branch to trigger CI
