"""
NOTE(diego): This is a module that I used already for a bunch of Atlassian related things,
and I haven't cleaned it up, I just added logic to dowload Jira attachments for Jira tickets.

If you see functions that make no sense to you here, they have probably nothing to do with
downloading attachments, apologies for the mess.

In order to download the right attachments in all the YLE Jira tickets, you need to:

- export JIRA_USERNAME with the username, and JIRA_API_TOKEN with the API token.
- call the script: `python3 jira.py yle-jira-attachments`

"""

import sys
import os
import json
from typing import Any, Callable, Iterable
import requests
from requests.auth import AuthBase, HTTPBasicAuth
import subprocess
import zipfile


## Jira

ATLASSIAN_BASE_URL = "https://bmat-music.atlassian.net"


def _reorganise_jira_keys(data: dict[str, Any]) -> dict[str, Any]:
    result = {**data}

    if "expand" in result:
        del result["expand"]

    if "summary" in result.get("fields", {}):
        result["summary"] = result["fields"]["summary"]
        del result["fields"]["summary"]

    if "name" in result.get("fields", {}).get("status"):
        result["status"] = result["fields"]["status"]["name"]

    if "created" in result.get("fields", {}):
        result["created"] = result["fields"]["created"]

    if "name" in (result.get("fields", {}).get("priority") or {}):
        result["priority"] = result["fields"]["priority"]["name"]

    result["assignee"] = (result.get("fields", {}).get("assignee") or {}).get("displayName")

    to_remove = []
    for key in result.get("fields", {}).keys():
        if key.startswith("customfield_"):
            to_remove.append(key)

    for key in to_remove:
        del result["fields"][key]

    del result["self"]

    issue_key = result["key"]

    result["url"] = f"{ATLASSIAN_BASE_URL}/browse/{issue_key}"

    return result


def jiramain(
    jql: str | None,
    handler: Callable[[AuthBase, Iterable[dict[str, Any]]], None] | None = None,
):
    username = os.environ["JIRA_USERNAME"]
    api_token = os.environ["JIRA_API_TOKEN"]

    headers = {"accept": "application/json"}
    jql = jql or "updateddate>='-60d' and assignee = 'dveralli@bmat.com' and status != Done order by updatedDate desc"
    auth = HTTPBasicAuth(username, api_token)

    def get_all_pages():

        start_at = 0

        while True:
            query = {"jql": jql, "startAt": start_at}

            response = requests.get(
                (ATLASSIAN_BASE_URL + "/rest/api/3/search?fields=*navigable,attachment"),
                headers=headers,
                auth=auth,
                params=query,
            )

            response_dict = json.loads(response.text)

            yield from response_dict["issues"]

            if start_at + response_dict["maxResults"] > response_dict["total"]:
                break

            start_at += response_dict["maxResults"]

    if handler is None:
        _output_json_array(_reorganise_jira_keys(r) for r in get_all_pages())
    else:
        handler(auth, (_reorganise_jira_keys(r) for r in get_all_pages()))


## Common Helpers


def _output_json_array(rows: Iterable[dict[str, Any]]):
    print("[")
    sep = "\n"
    for result in rows:
        print(sep)
        print(json.dumps(result, sort_keys=True))
        sep = ",\n"

    print("]")


def _get_token_from_pass(token_path: str) -> str:
    api_token_bytes = subprocess.check_output(["pass", token_path])

    return api_token_bytes.decode("utf-8").strip()


def download_attachments(auth: AuthBase, rows: Iterable[dict[str, Any]]):
    import csv

    SKIPPED_EXTENSIONS = set(
        [
            ".png",
            ".txt",
            ".json",
            ".mkv",
            ".mp4",
            ".mov",
            ".pdf",
            ".xlsx",
            ".csv",
            ".edl",
            ".gif",
            ".m4a",
            ".ogg",
            ".webm",
            ".jpg",
        ]
    )

    with open("attachments.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["ISSUE", "ATTACHMENT", "CREATED", "LOCAL_PATH"])
        for row in rows:
            for attachment in row["fields"].get("attachment", []):
                filename = attachment["filename"]
                ext = os.path.splitext(filename)[1]
                if not ext or ext.lower() in SKIPPED_EXTENSIONS:
                    continue

                output_file = make_unique_filename(row["key"], attachment["created"], filename)

                try:
                    if download_attachment(
                        auth,
                        attachment["id"],
                        row["key"],
                        attachment["created"],
                        filename,
                        output_file,
                    ):
                        writer.writerow([row["key"], filename, attachment["created"], output_file])
                except Exception as e:
                    print(f"Failed to process {row['key']}: {filename}", file=sys.stderr)
                    print(str(e), file=sys.stderr)
                    continue


def make_unique_filename(key: str, created_at: str, filename) -> str:
    return "{}_{}_{}".format(key, created_at, filename.replace("/", "_"))


def is_yle_report(filename: str) -> bool:
    basename = os.path.basename(filename).lower()
    return basename.startswith("report_")


def download_attachment(
    auth: AuthBase,
    id: str,
    key: str,
    created_at: str,
    original_filename: str,
    output_file: str,
):
    response = requests.get(
        (ATLASSIAN_BASE_URL + "/rest/api/3/attachment/content/{}".format(id)),
        auth=auth,
    )

    with open(output_file, "wb") as f:
        f.write(response.content)

    ext = os.path.splitext(output_file)[1]

    if ext.lower() == ".zip":
        zip_archive = zipfile.ZipFile(output_file)
        for f in zip_archive.namelist():
            if not is_yle_report(f):
                continue

            ext = os.path.splitext(f)[1]
            if ext.lower() == ".xml":
                with zip_archive.open(f) as zipf:
                    name = make_unique_filename(key, created_at, f)
                    with open(name, "wb") as f:
                        f.write(zipf.read())

        os.remove(output_file)

    elif not is_yle_report(original_filename):
        os.remove(output_file)
        return False

    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "yle-jira-attachments":
        # 13526 is the "YLE" Jira project
        jiramain("project IN (13526) AND (attachments IS NOT EMPTY)", handler=download_attachments)
    elif len(sys.argv) > 1 and sys.argv[1] == "jira":
        if len(sys.argv) > 2:
            jiramain(sys.argv[2])
        else:
            jiramain(None)
    else:
        raise ValueError(f"Invalid args: {sys.argv}")
