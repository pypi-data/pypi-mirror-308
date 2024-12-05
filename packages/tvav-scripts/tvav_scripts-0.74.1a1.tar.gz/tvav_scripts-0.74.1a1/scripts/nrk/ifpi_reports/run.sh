#!/bin/bash
# BASE_DIR=$(dirname "$0")
# BUILDS_BASE_DIR=${BASE_DIR}/builds
# BUILD_DIR=${BUILDS_BASE_DIR}/${BUILD_NUMBER}
# OUTPUT_DIR=${BUILD_DIR}/output

# echo
# echo "Removing old files"
# # Remove built directories older than 2 days
# mkdir -p ${BUILDS_BASE_DIR}
# find ${BUILDS_BASE_DIR}/* -type d -ctime +2 -exec rm -fr {} \;

echo
echo "Activating environment"
python3 -m venv venv
. venv/bin/activate
pip install -U -r requirements.txt

echo
echo "Creating directories:"
# echo " - Output: ${OUTPUT_DIR}"
# mkdir -p ${OUTPUT_DIR}

echo "Generating IFPI report"
python ifpi_reports.py
