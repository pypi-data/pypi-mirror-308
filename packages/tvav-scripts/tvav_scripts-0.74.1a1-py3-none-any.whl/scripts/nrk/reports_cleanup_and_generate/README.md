# General

Remember to create your env file based on the example: `cp .env.example .env`

# Reports cleanup

This script is used to clean the digital usages, avworks and schedules reported.

It will set the reported for all the ones selected as ``False``. Also, it will clean extras ``reported_by`` and ``reported_daily``.

It will set also the extra field ``cleaned_reported``, so it is easy to query for these entries in the database.

### Parameters

You can update the .env to execute the script with the parameters you want. 

Remember to set up the parameter ``MONGO_URI`` and ``CLEANUP_TYPE`` to one of the valids. And depending on that parameter you must set up others.

* If you are running it by ``date`` remember to update ``START_TIME`` and ``END_TIME``.

* If you are running it by ``filename`` remember to update ``REPORT_REGEX``.

* If you are running it by ``ids`` remember to update ``REPORT_IDS``.

If you want to keep the reported schedules and digital usages but still clean the avworks ones, you can set the parameter ``CLEAN_LOGS_FROM_DAY``, if not, it is better if you keep it as not defined in the env file. 

# Generate reports

This script is used to generate reports for all Schedules, AvWorks and DigitalUsages due the parameter ``REPORT_TYPE``

Remember to set up the parameters ``START_TIME`` and ``END_TIME``. So, that parameters will be the ones to filter which objects report.

### Parameters

You can update the .env to execute the script with the parameters you want. 

The mandatory ones are as said ``START_TIME`` and ``END_TIME``. Also ``REPORT_TYPE``, as it will show the report to create.

It is also mandatory to update the ``MONGO_URI``, ``CELERY_BROKER`` and ``REPORTS_QUEUE``.
