#!/bin/zsh

if [ -z "$1" ]; then
    echo "Usage: $0 <system_path>"
    exit 1
fi


REPORTS_FOLDER="$1"
echo $REPORTS_FOLDER
#
## Program Stats
echo "Total number of reported cue-sheets: " `grep -r "<rapnro>" ${REPORTS_FOLDER}\/*.xml | awk -F".xml:\t\t" '{print $2}' | awk -F">" '{print $2}' | awk -F"<" '{print $1}' | wc -l`
echo "Unique number of reported cue-sheets: " `grep -r "<rapnro>" ${REPORTS_FOLDER}\/*.xml | awk -F".xml:\t\t" '{print $2}' | awk -F">" '{print $2}' | awk -F"<" '{print $1}' | sort | uniq | wc -l`
#
## SoMe
echo "Total number of reported cue-sheets for SoMe ONLY: " `grep -r "<rapnro>" ${REPORTS_FOLDER}\/(report_FB|report_PS|report_TT|report_WA|report_IG|report_SC|report_TW|report_YT)_*.xml | awk -F".xml:\t\t" '{print $2}' | awk -F">" '{print $2}' | awk -F"<" '{print $1}' | wc -l`
echo "Unique number of reported cue-sheets for SoMe ONLY: " `grep -r "<rapnro>" ${REPORTS_FOLDER}\/(report_FB|report_PS|report_TT|report_WA|report_IG|report_SC|report_TW|report_YT)_*.xml | awk -F".xml:\t\t" '{print $2}' | awk -F">" '{print $2}' | awk -F"<" '{print $1}' | sort | uniq | wc -l`
#
## Music Stats
echo "Total number of reported music tracks: " `grep -r "<reportal_teos_id>" ${REPORTS_FOLDER}\/*.xml | awk -F".xml:\t\t" '{print $2}' | awk -F">" '{print $2}' | awk -F"<" '{print $1}' | wc -l`
echo "Total number of reported unique music works: " `grep -r "<reportal_teos_id>" ${REPORTS_FOLDER}\/*.xml | awk -F".xml:\t\t" '{print $2}' | awk -F">" '{print $2}' | awk -F"<" '{print $1}' | sort | uniq | wc -l`
#
## Music Contributor Stats
echo "Unique number of tracks with a missing performer: " `grep -r "<esittajat/>" ${REPORTS_FOLDER}\/*.xml -A 28 | grep reportal_teos_id  | awk -F".xml-\t\t" '{print $2}' | awk -F">" '{print $2}' | awk -F"<" '{print $1}' | sort | uniq | wc -l`
echo "Unique number of tracks with a missing composer/author: " `grep -r "<saveltajat/>" ${REPORTS_FOLDER}\/*.xml -A 28 | grep reportal_teos_id  | awk -F".xml-\t\t" '{print $2}' | awk -F">" '{print $2}' | awk -F"<" '{print $1}' | sort | uniq | wc -l`
#
echo "Total of programs starting with YLEMUSA_XXX: " `grep -r "YLEMUSA_"  ${REPORTS_FOLDER}\/*.xml | wc -l`
