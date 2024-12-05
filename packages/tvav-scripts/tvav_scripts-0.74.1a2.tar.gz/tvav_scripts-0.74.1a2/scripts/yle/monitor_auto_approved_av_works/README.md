# monitor_auto_approved_av_works

The purpose of this script is to monitor the DB in a cronjob inside av-fabric-stg
to ensure no auto approved AvWorks appear.

If 1 or more auto approved AvWorks are found, it will notify in the Slack channel
set by the env variables.

## How to use

Just define the env variables from .env.templates in your env or in a .env file with the
right values and run the script.