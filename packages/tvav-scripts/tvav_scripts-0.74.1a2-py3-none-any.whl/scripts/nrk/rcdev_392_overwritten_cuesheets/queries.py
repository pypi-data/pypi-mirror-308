from typing import NamedTuple


# last reported vs production
SQL_REPORT_LAST_REPORTED_VS_PRODUCTION = """
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
        id,
        rank() over (
            partition by
                reported_program_row_id
            order by
                mw_id, id
        ) AS cue_position,
        reported_program_row_id,
        mw_id,
        mw_title,
        cue_duration,
        mw_source
    from
        reported_mw_info
),
ranked_mwi_b as (
    select
        id,
        rank() over (
            partition by
                production_program_row_id
            order by
                mw_id, id
        ) as cue_position,
        program_id,
        production_program_row_id,
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
    a.program_id as program_id,
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
    on a.program_id = b.program_id
left join
    reported_cuesheet a_cuesheet on a_cuesheet.reported_program_row_id = a.id
left join
    production_cuesheet b_cuesheet on b_cuesheet.production_program_row_id = b.id
cross join
    series
left join
    ranked_mwi_a mwi_a on (
        mwi_a.reported_program_row_id = a.id and
        mwi_a.cue_position = series.value
    )
left join
    ranked_mwi_b mwi_b on (
        mwi_b.production_program_row_id = b.id and
        mwi_b.cue_position = series.value
    )
where (
    (
        (mwi_b.id is null and mwi_a.id is not null) or
        (mwi_b.id is not null and mwi_a.id is null) or
        (mwi_a.cue_position = mwi_b.cue_position)
    ) and exists (
        select 1
        from
            last_reported_version lrv
        where
            lrv.program_id = a.program_id and
            lrv.id = a.id and
            lrv.report_date = a.report_date
    ) and (
        mwi_a.cue_position is not null or
        mwi_b.cue_position is not null
    ) and coalesce(a_cuesheet.data, '') <> coalesce(b_cuesheet.data, '') and
    a.program_id is not null and
    a.program_id != ''
)
order by
    a.report_date, a.program_id
"""

# first reported vs other reported
SQL_REPORT_FIRST_REPORTED_VS_OTHER_REPORTED  = """
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


class Report(NamedTuple):
    report_filename: str
    columns: tuple[str, ...]
    query: str


DIFF_REPORT_SQL_QUERIES: list[Report] = [
    Report(
        "last_reported_vs_prod.csv",
        (
            "program_id",
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
            "production_music_source",
            "production_last_edited_at",
            "production_last_populated_at",
        ),
        SQL_REPORT_LAST_REPORTED_VS_PRODUCTION,
    ),
]
