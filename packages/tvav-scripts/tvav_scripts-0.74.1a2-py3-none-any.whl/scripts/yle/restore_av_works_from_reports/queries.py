# last reported vs production
SQL_REPORT_1 = """
with RECURSIVE generate_series(value) as (
    select 1 union all select value + 1
    from
        generate_series
    where
        value < {}
),
series as (
    select value from generate_series
),
ranked_mwi_a AS (
    select
        rank() over (
            partition by
                reported_program_id
            order by
                mw_id, id
        ) AS cue_position,
        reported_program_id,
        mw_id,
        mw_title,
        cue_duration,
        mw_source
    from
        mw_info
),
ranked_mwi_b as (
    select
        id,
        rank() over (
            partition by
                yle_numerical_id
            order by
                mw_id, id
        ) as cue_position,
        yle_numerical_id,
        program_title,
        mw_id,
        mw_title,
        cue_duration,
        mw_source,
        last_edited_at,
        last_populated_at
    from
        production_mw_info
)
select
    a.yle_numerical_id as yle_numerical_id,
    a.program_title as last_reported_program_title,
    a.id as last_reported_id,
    a.report_date as last_reported_date,
    a.report_filename as last_reported_filename,
    mwi_a.mw_id as last_reported_cue_id,
    mwi_a.mw_title as last_reported_cue_title,
    mwi_a.cue_duration as last_reported_cue_duration,
    mwi_a.mw_source as last_reported_music_source,
    b.program_title as production_program_title,
    mwi_b.mw_id as production_cue_id,
    mwi_b.mw_title as production_cue_title,
    mwi_b.cue_duration as production_cue_duration,
    mwi_b.mw_source as production_music_source,
    b.last_edited_at as production_last_edited_at,
    b.last_populated_at as production_last_populated_at
from
    reported_program a
join production_program b
    on a.yle_numerical_id = b.yle_numerical_id
    and a.is_filler = b.is_filler
left join
    cuesheet a_cuesheet on a_cuesheet.reported_program_id = a.id
left join
    production_cuesheet b_cuesheet on b_cuesheet.yle_numerical_id = a.yle_numerical_id
    and b_cuesheet.production_program_id = b.id
cross join
    series
left join
    ranked_mwi_a mwi_a on (
        mwi_a.reported_program_id = a.id and
        mwi_a.cue_position = series.value
    )
left join
    ranked_mwi_b mwi_b on (
        mwi_b.yle_numerical_id = a.yle_numerical_id and
        mwi_b.cue_position = series.value
    )
where a.is_filler = 0 and (
    (
        (mwi_b.id is null and mwi_a.reported_program_id is not null) or
        (mwi_b.id is not null and mwi_a.reported_program_id is null) or
        (mwi_a.cue_position = mwi_b.cue_position)
    ) and exists (
        select 1
        from
            last_reported_version lrv
        where
            lrv.yle_numerical_id = a.yle_numerical_id and
            lrv.id = a.id and
            lrv.report_date = a.report_date
    ) and not exists (
        select 1
        from
            report_3 r3
        where
            r3.yle_numerical_id = a.yle_numerical_id
    ) and (
        mwi_a.cue_position is not null or
        mwi_b.cue_position is not null
    ) and coalesce(a_cuesheet.data, '') <> coalesce(b_cuesheet.data, '') and
    a.yle_numerical_id is not null and
    a.yle_numerical_id != ''
)
order by
    a.report_date, a.yle_numerical_id
"""

# first reported vs backup
SQL_REPORT_2 = """
with RECURSIVE generate_series(value) as (
    select 1 union all select value + 1
    from
        generate_series
    where
        value < {}
),
series as (
    select value from generate_series
),
ranked_mwi_a AS (
    select
        rank() over (
            partition by
                reported_program_id
            order by
                mw_id, id
        ) AS cue_position,
        reported_program_id,
        mw_id,
        mw_title,
        cue_duration,
        mw_source
    from
        mw_info
),
ranked_mwi_b as (
    select
        id,
        rank() over (
            partition by
                yle_numerical_id
            order by
                mw_id, id
        ) as cue_position,
        yle_numerical_id,
        program_title,
        mw_id,
        mw_title,
        cue_duration,
        mw_source,
        approved
    from
        backup_mw_info
)
select
    a.yle_numerical_id as yle_numerical_id,
    a.program_title as first_reported_program_title,
    a.id as first_reported_id,
    a.report_date as first_reported_date,
    a.report_filename as first_reported_filename,
    mwi_a.mw_id as first_reported_cue_id,
    mwi_a.mw_title as first_reported_cue_title,
    mwi_a.cue_duration as first_reported_cue_duration,
    mwi_a.mw_source as first_reported_music_source,
    mwi_b.program_title as backup_program_title,
    mwi_b.mw_id as backup_reported_cue_id,
    mwi_b.mw_title as backup_cue_title,
    mwi_b.cue_duration as backup_cue_duration,
    mwi_b.mw_source as backup_music_source,
    prod_mwi.last_edited_at as production_last_edited_at,
    prod_mwi.last_populated_at as production_last_populated_at
from
    reported_program a
join backup_program b
    on a.yle_numerical_id = b.yle_numerical_id
    and a.is_filler = b.is_filler
left join
    cuesheet a_cuesheet on a_cuesheet.reported_program_id = a.id
left join
    backup_cuesheet b_cuesheet on b_cuesheet.yle_numerical_id = a.yle_numerical_id
    and b_cuesheet.backup_program_id = b.id
cross join
    series
left join
    ranked_mwi_a mwi_a on (
        mwi_a.reported_program_id = a.id and
        mwi_a.cue_position = series.value
    )
left join
    ranked_mwi_b mwi_b on (
        mwi_b.yle_numerical_id = a.yle_numerical_id and
        mwi_b.cue_position = series.value
    )
left join
    production_program prod_mwi on (
        prod_mwi.yle_numerical_id = a.yle_numerical_id
    )
where a.is_filler = 0 and (
    b.approved = 1 and (
        (mwi_b.id is null and mwi_a.reported_program_id is not null) or
        (mwi_b.id is not null and mwi_a.reported_program_id is null) or
        (mwi_a.cue_position = mwi_b.cue_position)
    ) and (
        mwi_a.cue_position is not null or
        mwi_b.cue_position is not null
    ) and exists (
        select 1
        from
            first_reported_version frv
        where
            frv.report_date > '2023-08-31' and
            frv.yle_numerical_id = a.yle_numerical_id and
            frv.id = a.id and
            frv.report_date = a.report_date
    ) and coalesce(a_cuesheet.data, '') <> coalesce(b_cuesheet.data, '') and
    a.yle_numerical_id is not null and
    a.yle_numerical_id != ''
)
order by
    a.report_date, a.yle_numerical_id
"""

# first reported vs other reported
SQL_REPORT_3 = """
with RECURSIVE generate_series(value) as (
    select 1 union all select value + 1
    from
        generate_series
    where
        value < {}
),
series as (
    select value from generate_series
),
ranked_mwi_a as (
    select
        rank() over (
            partition by
                reported_program_id
            order by
                mw_id, id
        ) as cue_position,
        reported_program_id,
        mw_id,
        mw_title,
        cue_duration,
        mw_source
    from
        mw_info
),
ranked_mwi_b as (
    select
        rank() over (
            partition by
                reported_program_id
            order by
                mw_id, id
        ) as cue_position,
        reported_program_id,
        mw_id,
        mw_title,
        cue_duration,
        mw_source
    from
        mw_info
),
program_last_edited_at as (
    select distinct
        yle_numerical_id,
        last_edited_at,
        last_populated_at
    from
        production_mw_info
)
select
    a.yle_numerical_id as yle_numerical_id,
    a.program_title as first_reported_program_title,
    a.id as first_reported_id,
    a.report_date as first_reported_date,
    a.report_filename as first_reported_filename,
    mwi_a.mw_id as first_reported_cue_id,
    mwi_a.mw_title as first_reported_cue_title,
    mwi_a.cue_duration as first_reported_cue_duration,
    mwi_a.mw_source as first_reported_music_source,
    b.program_title as other_reported_program_title,
    b.id as other_reported_id,
    b.report_date as other_reported_date,
    b.report_filename as other_reported_filename,
    mwi_b.mw_id as other_reported_cue_id,
    mwi_b.mw_title as other_reported_cue_title,
    mwi_b.cue_duration as other_reported_cue_duration,
    mwi_b.mw_source as other_reported_music_source,
    prod_mwi.last_edited_at as production_last_edited_at,
    prod_mwi.last_populated_at as production_last_populated_at
from
    reported_program a
join
    reported_program b on (
        a.yle_numerical_id = b.yle_numerical_id and
        a.is_filler = b.is_filler and
        a.id <> b.id
    )
left join
    cuesheet a_cuesheet on (
        a_cuesheet.reported_program_id = a.id
    )
left join
    cuesheet b_cuesheet on (
        b_cuesheet.reported_program_id = b.id
    )
cross join
    series
left join ranked_mwi_a mwi_a on (
    mwi_a.reported_program_id = a.id and
    mwi_a.cue_position = series.value
)
left join ranked_mwi_b mwi_b on (
  mwi_b.reported_program_id = b.id and
  mwi_b.cue_position = series.value
)
left join program_last_edited_at prod_mwi on (
    a.yle_numerical_id = prod_mwi.yle_numerical_id
)
where a.is_filler = 0 and (
    (
        (
          mwi_a.reported_program_id is null and
          mwi_b.reported_program_id is not null
        ) or (
          mwi_b.reported_program_id is null and
          mwi_a.reported_program_id is not null
        ) or mwi_a.cue_position = mwi_b.cue_position
  ) and (
    mwi_a.cue_position is not null or
    mwi_b.cue_position is not null
  ) and exists (
        select 1
        from
            first_reported_version frv
        where
            frv.yle_numerical_id = a.yle_numerical_id and
            frv.id = a.id and
            frv.report_date = a.report_date
  ) and
  coalesce(a_cuesheet.data, '') <> coalesce(b_cuesheet.data, '') and
  a.yle_numerical_id is not null and
  a.yle_numerical_id != ''
)
order by
    a.report_date, a.yle_numerical_id, b.report_date
"""

SQL_SIMPLIFIED_REPORT_3 = "select * from report_3"


REPORTS = [
    {
        # 1 --> Overwrite happened after last report
        # last reported - 3rd report vs production
        "report_filename": "1_overwrite_happened_after_last_report.csv",
        "sql": SQL_REPORT_1,
        "fields": [
            "yle_numerical_id",
            "last_reported_program_title",
            "last_reported_id",
            "last_reported_date",
            "last_reported_filename",
            "last_reported_cue_id",
            "last_reported_cue_title",
            "last_reported_cue_duration",
            "last_reported_music_source",
            "production_program_title",
            "production_cue_id",
            "production_cue_title",
            "production_cue_duration",
            "production_mw_source",
            "production_last_edited_at",
            "production_last_populated_at",
        ],
    },
    {
        # 2 --> Overwrite happened before 1 report
        # first reported vs Backup DB
        "report_filename": "2_overwrite_happened_before_1_report.csv",
        "sql": SQL_REPORT_2,
        "fields": [
            "yle_numerical_id",
            "first_reported_program_title",
            "first_reported_id",
            "first_reported_date",
            "first_reported_filename",
            "first_reported_cue_id",
            "first_reported_cue_title",
            "first_reported_cue_duration",
            "first_reported_music_source",
            "backup_program_title",
            "backup_cue_id",
            "backup_cue_title",
            "backup_cue_duration",
            "backup_music_source",
            "production_last_edited_at",
            "production_last_populated_at",
        ],
    },
    {
        # 3 --> Overwrite happened in between reports
        # reported vs reported
        "report_filename": "3_overwrite_happened_in_between_reports.csv",
        "sql": SQL_SIMPLIFIED_REPORT_3,
        "fields": [
            "yle_numerical_id",
            "first_reported_program_title",
            "first_reported_id",
            "first_reported_date",
            "first_reported_filename",
            "first_reported_cue_id",
            "first_reported_cue_title",
            "first_reported_cue_duration",
            "first_reported_music_source",
            "other_reported_program_title",
            "other_reported_id",
            "other_reported_date",
            "other_reported_filename",
            "other_reported_cue_id",
            "other_reported_cue_title",
            "other_reported_cue_duration",
            "other_reported_music_source",
            "production_last_edited_at",
            "production_last_populated_at",
        ],
    },
]
