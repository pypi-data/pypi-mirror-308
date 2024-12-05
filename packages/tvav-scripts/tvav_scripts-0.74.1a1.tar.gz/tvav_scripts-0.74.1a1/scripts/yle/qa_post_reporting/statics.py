prioritized_tags = [
    "rapnro",  # Unique ID -> av_work.work_ids.yle_numerical_id
    "julk_pvm_a",  # Transmission Date -> date part of schedule.start_time
    "aklo",  # Transmission Time -> time part of schedule.start_time
    "kanava",  # Channel -> schedule.channel
    "nimi",  # Program Name -> schedule.av_work.titles
    "plasma_ohjelma_id",  # Plasma ID -> schedule.av_work.work_ids.plasma_id
    "car_id",  # Part of Radioman ID -> schedule.av_work.work_ids.site_id
    "car_ohjelma_id",  # Part of Radioman ID -> schedule.av_work.work_ids.radioman_programme_id
    "areenajulkaisu",  # Publication days -> schedule.av_work.extras.web_available
    "ajopvm",  # Report Date (only exists in the XML)
    "t.duration",
    "t.count",
]

csv_datatype = {
    "rapnro": "string",
    "julk_pvm_a": "string",
    "aklo": "string",
    "kanava": "string",
    "nimi": "string",
    "plasma_ohjelma_id": "string",
    "car_id": "string",
    "car_ohjelma_id": "string",
    "areenajulkaisu": "string",
    "ajopvm": "string",
}
