import csv
import logging
import os
import subprocess
from typing import Optional
import xml.etree.ElementTree as ET
from collections import OrderedDict
from datetime import datetime

import pandas as pd
from tqdm import tqdm

from scripts.yle.qa_post_reporting.statics import csv_datatype

logger = logging.getLogger("YLE-QA-POST-REPORT-UTILS ")


def convert_string_to_seconds(time_string):
    try:
        minutes = int(time_string[:3])
        seconds = int(time_string[3:])
        total_seconds = minutes * 60 + seconds
        return total_seconds
    except ValueError:
        # Handle the case where the input string is not in the expected format
        logger.error("Invalid input format. Please provide a 5-character string in the format MMMSS.")
        return None


def flatten_xml(xml_element, parent_key="", delimiter="_"):
    """
    Flatten XML element to an ordered dictionary to preserve order.
    """
    flat_dict = OrderedDict()

    for child in xml_element:
        key = f"{child.tag}"

        if child:
            if child.tag in flat_dict:
                # If the tag already exists in the dictionary, treat it as a list
                if not isinstance(flat_dict[key], list):
                    flat_dict[key] = [flat_dict[key]]
                flat_dict[key].append(flatten_xml(xml_element=child, parent_key=key, delimiter=delimiter))
            else:
                flat_dict[key] = flatten_xml(xml_element=child, parent_key=key, delimiter=delimiter)
        else:
            if key == "kesto" and child.text:
                flat_dict[key] = convert_string_to_seconds(child.text)
            else:
                flat_dict[key] = child.text

    return flat_dict


def convert_xml_to_csv(xml_file_path, flattened_data, prioritized_tags=None):
    """
    Convert XML file to flattened dictionary.
    """
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    current_data = flatten_xml(root)

    if prioritized_tags:
        if isinstance(current_data.get("ohjelma_esitys"), str):
            prioritized_data = OrderedDict((tag, current_data.get(tag, "")) for tag in prioritized_tags)
            out_dict = OrderedDict(**prioritized_data)
            flattened_data.append(out_dict)

        elif isinstance(current_data.get("ohjelma_esitys"), list):
            for items in current_data.get("ohjelma_esitys"):
                items["t.duration"] = 0
                items["t.count"] = 0

                if isinstance(items.get("aanite"), list):
                    for tracks in items["aanite"]:
                        if "kesto" in tracks.get("teokset", {}).get("teos", {}).get("aanite_teos", {}):
                            items["t.duration"] += tracks["teokset"]["teos"]["aanite_teos"]["kesto"]
                            items["t.count"] += 1
                else:
                    if "kesto" in items.get("aanite", {}).get("teokset", {}).get("teos", {}).get("aanite_teos", {}):
                        items["t.duration"] += items["aanite"]["teokset"]["teos"]["aanite_teos"]["kesto"]
                        items["t.count"] += 1

                prioritized_data = OrderedDict((tag, items.get(tag, "")) for tag in prioritized_tags)

                out_dict = OrderedDict(**prioritized_data)
                flattened_data.append(out_dict)


def convert_all_xml_to_csv(input_folder, output_csv_path, prioritized_tags=None) -> bool:
    """
    Convert all XML files in a folder to a single CSV file.
    """
    flattened_data = []
    if not os.path.exists(output_csv_path):
        for root, _, files in os.walk(input_folder):
            for file in tqdm(files):
                if file.lower().endswith(".xml"):
                    xml_file_path = os.path.join(root, file)
                    convert_xml_to_csv(xml_file_path, flattened_data, prioritized_tags)

        if flattened_data:
            with open(output_csv_path, "w", newline="", encoding="utf-8") as csv_file:
                fieldnames = list(flattened_data[0].keys())  # Use the keys of the first dictionary as fieldnames
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(flattened_data)
                return True
    return False


def filter_for_media_type(input_csv_path: str, output_csv_path: str, media_type_startswith: str):
    """
    This function checks if there exists duplicate programs within the input csv and creates an output csv with
    the duplicates found.
    """
    df = pd.read_csv(input_csv_path)

    # Filter rows where the 'kanava' column starts with 'r' or 't'
    filtered_df = df[df['kanava'].str.startswith(media_type_startswith)]

    # Export the rows with filtered programs to a new CSV file
    filtered_df.to_csv(output_csv_path, index=False)


def find_duplicates_within_one_csv(input_csv_path: str, output_csv_path: str, duplicate_columns=None) -> bool:
    """
    This function checks if there exists duplicate programs within the input csv and creates an output csv with
    the duplicates found.
    """
    # Read the CSV file into a pandas DataFrame
    if duplicate_columns is None:
        duplicate_columns = ["julk_pvm_a", "aklo", "kanava", "plasma_ohjelma_id", "car_ohjelma_id", "nimi"]

    df = pd.read_csv(input_csv_path)

    # Find duplicate programs
    duplicate_programs = df[df.duplicated(subset=duplicate_columns, keep=False)]

    if not duplicate_programs.empty:
        # Export the rows with duplicate programs to a new CSV file
        duplicate_programs.to_csv(output_csv_path, index=False)
        return False
    return True


def find_duplicates_between_two_csvs(main_csv_path: str, input_csv_path: str, output_csv_path: str, duplicate_columns=None) -> bool:
    """
    This function checks if there exists duplicate programs between the input csv and master csv.
    It creates an output csv with the duplicates found.
    """

    # Read the main csv file into a pandas DataFrame
    if duplicate_columns is None:
        duplicate_columns = ["rapnro", "julk_pvm_a", "aklo", "plasma_ohjelma_id", "car_id", "car_ohjelma_id"]

    main_df = pd.read_csv(main_csv_path, low_memory=False, dtype=csv_datatype)  # type: ignore

    # Read the incoming CSV file into another pandas DataFrame
    incoming_df = pd.read_csv(input_csv_path, low_memory=False, dtype=csv_datatype)  # type: ignore

    # Define the columns to check for duplicates
    duplicate_programs = main_df.merge(incoming_df, how="inner", on=duplicate_columns)  # type: ignore

    if not duplicate_programs.empty:
        # Export the rows with duplicate programs to a new CSV file
        duplicate_programs.to_csv(output_csv_path, index=False)
        return False
    return True


def find_duplicates_combining_two_csvs(
    main_csv_path: str,
    input_csv_path: str,
    output_csv_path: str,
    report_date: datetime,
    duplicate_columns: Optional[list] = None
) -> bool:
    """
    This function first combines the 2 csvs and checks if there exists duplicate programs within it.
    It creates an output csv with the duplicates found.
    """
    # Read the main csv file into a pandas DataFrame
    if duplicate_columns is None:
        duplicate_columns = ["rapnro", "julk_pvm_a", "aklo", "plasma_ohjelma_id", "car_id", "car_ohjelma_id"]

    main_df = pd.read_csv(main_csv_path, low_memory=False, dtype=csv_datatype)

    # Read the incoming CSV file into another pandas DataFrame
    incoming_df = pd.read_csv(input_csv_path, low_memory=False, dtype=csv_datatype)

    # Concatenate the two DataFrames
    combined_df = pd.concat([main_df, incoming_df], ignore_index=True)

    # Now filter rows that have empty Plasma IDs
    combined_df = combined_df[pd.notna(combined_df["plasma_ohjelma_id"])]

    combined_df = combined_df.sort_values(by=["aklo", "julk_pvm_a"], ascending=[True, True])

    duplicate_programs = combined_df[combined_df.duplicated(subset=duplicate_columns, keep=False)]

    duplicate_programs = duplicate_programs.sort_values(by=["plasma_ohjelma_id"], ascending=[True])

    # Filter only for results that come from the current report_date
    duplicate_programs = duplicate_programs[duplicate_programs["ajopvm"] == report_date.strftime("%Y%m%d")]

    if not duplicate_programs.empty:
        # Export the rows with duplicate programs to a new CSV file
        duplicate_programs.to_csv(output_csv_path, index=False)
        return False
    return True


def run_shell_command(command):
    try:
        # Run the shell command and capture its output
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Decode the stdout and stderr bytes to strings
        stdout_str = result.stdout.decode('utf-8')
        stderr_str = result.stderr.decode('utf-8')

        return stdout_str, stderr_str
    except subprocess.CalledProcessError:
        return None, None


def generate_report_stats(stats_folder_path):
    """
    Creates a file in the stats_folder_path with the following information
    - Total number of reported cue-sheets
    - Unique number of reported cue-sheets
    - Total number of reported cue-sheets for SoMe ONLY if possible
    - Unique number of reported cue-sheets for SoMe ONLY
    - Total number of reported music tracks
    - Total number of reported unique music works
    - Unique number of tracks with a missing performer (esittajat)
    - Unique number of tracks with a missing composer/author (saveltajat)
    - Total of programs starting with YLEMUSA_XXX
    """
    run_shell_command(
        f"zsh stats.sh {stats_folder_path}/ > {stats_folder_path}/batch_stats.txt",
    )
