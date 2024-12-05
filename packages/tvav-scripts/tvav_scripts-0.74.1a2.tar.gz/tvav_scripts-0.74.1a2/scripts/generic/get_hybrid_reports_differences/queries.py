from dataclasses import dataclass
from typing import Iterator


# TODO: rethink this
LINES_EXISTING_IN_BOTH_REPORTS_BUT_DIFF_DURATION = """
with common as (
  select 
    r.id as r_id,
    v.id as v_id,
    v."Channel",
    r."EPG Title" as r_epg_title,
    v."EPG Title" as v_epg_title,
    r."EPG Type" as r_epg_type,
    v."EPG Type" as v_epg_type,
    r."Link" as r_link,
    v."Link" as v_link,
    r."Track" as r_track,
    v."Track" as v_track,
    r."Artist" as r_artist,
    v."Artist" as v_artist,
    r."Label" as r_label,
    v."Label" as v_label,
    r."ISRC" as r_isrc,
    v."ISRC" as v_isrc,
    r."ISWC" as r_iswc,
    v."ISWC" as v_iswc,
    r."BmatId" as r_bmat_id,
    v."BmatId" as v_bmat_id,
    r."Album" as r_album,
    v."Album" as v_album,
    r."UTC Start Time" as r_utc_start_time,
    v."UTC Start Time" as v_utc_start_time,
    r."UTC End Time" as r_utc_end_time,
    v."UTC End Time" as v_utc_end_time,
    r."UTC Duration (s)" as r_duration,
    v."UTC Duration (s)" as v_duration
  from reportal_reports_{report_month} r
  left join vericast_reports_{report_month} v on (
    (r."UTC Start Time" - INTERVAL 30 SECOND) < v."UTC Start Time" and
    (r."UTC Start Time" + INTERVAL 30 SECOND) > v."UTC Start Time" and
    (r."UTC End Time" - INTERVAL 30 SECOND) < v."UTC End Time" and 
    (r."UTC End Time" + INTERVAL 30 SECOND) > v."UTC End Time"
  )
  order by r_utc_start_time asc
), common_different as (
  select * from common
  where r_duration != v_duration
), identified_common_different as (
  select * from common_different
  where v_track is not null
), unidentified_common_different as (
  select * from common_different
  where v_track is null
)
select 'identified_diff' as 'diff type', * from identified_common_different
union
select 'unidentified_diff' as 'diff type', * from unidentified_common_different
"""


@dataclass(frozen=True)
class Query:
    sql_str: str
    col_names: list[str]
    report_filename: str


class QueryFactory:
    def __init__(self, report_month: int) -> None:
        self.report_month = report_month

    def __iter__(self) -> Iterator[Query]:
        yield Query(
            sql_str=LINES_EXISTING_IN_BOTH_REPORTS_BUT_DIFF_DURATION.format(report_month=self.report_month),
            col_names=[
				"diff type",
				"r_id",
				"v_id",
				"channel",
				"r_epg_title",
				"v_epg_title",
				"r_epg_type",
				"v_epg_type",
				"r_link",
				"v_link",
				"r_track",
				"v_track",
				"r_artist",
				"v_artist",
				"r_label",
				"v_label",
				"r_isrc",
				"v_isrc",
				"r_iswc",
				"v_iswc",
				"r_bmat_id",
				"v_bmat_id",
				"r_album",
				"v_album",
				"r_utc_start_time",
				"v_utc_start_time",
				"r_utc_end_time",
				"v_utc_end_time",
				"r_duration",
				"v_duration",
            ],
            report_filename=f"lines_existing_in_both_but_diff_duration_{self.report_month}",
        )
