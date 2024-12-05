import csv
import os
import subprocess
from atlassian.bitbucket.cloud import Cloud
from dotenv import load_dotenv
from pathlib import Path
from pprint import pprint
from tempfile import NamedTemporaryFile
from time import sleep
from tqdm import tqdm


class BitbucketConfig:
    def __init__(self) -> None:
        self.url = os.getenv("URL", "https://api.bitbucket.org/")
        self.app_username = os.getenv("APP_USERNAME")
        self.app_password = os.getenv("APP_PASSWORD")
        self.workspace = os.getenv("WORKSPACE", "bmat-music")
        self.project = os.getenv("PROJECT", "TVAV")
        self.max_deploys_per_batch = int(os.getenv("MAX_DEPLOYS_PER_BATCH", 3))
        self.wait_between_batches = int(os.getenv("WAIT_BETWEEN_BATCHES", 180))

        if __name__ == "__main__":
            self.parent_dir = Path(__file__).parent
        else:
            self.parent_dir = Path(os.getcwd())

        self.stats_report_file = self.parent_dir / "deploy_stats.csv"

        assert self.app_username is not None, "APP_USERNAME is missing"
        assert self.app_password is not None, "APP_PASSWORD is missing"


def deploy(config: BitbucketConfig) -> dict:
    """Selectively deploy customers from any repo in a Bitbucket workspace."""

    # just to collect stats
    stats = {}

    # try to detect current repo name
    try:
        local_repo_name = subprocess.check_output([
            "git", "remote", "get-url", "origin"
        ]).decode().split("/")[-1].replace(".git\n", "")
    except:
        local_repo_name = None

    repo_name = input(
        "Repository you want to deploy " +
        (
            f"({local_repo_name})" if local_repo_name else ""
        ) + ": "
    ) or local_repo_name

    cloud = Cloud(
        url=config.url, username=config.app_username,
        password=config.app_password,
        backoff_and_retry=True,
    )

    repo = cloud.repositories.get(config.workspace, repo_name)
    customer_branches = [
        branch.name
        for branch in repo.branches.each(q='name~"customer/"')
    ]

    if not customer_branches:
        print("No customer branches found")
        return stats

    temp_filename = None
    with NamedTemporaryFile(delete=False) as f:
        temp_filename = f.name
        f.write("\n".join(customer_branches).encode())
        f.seek(0)

        editor = os.getenv("EDITOR", "vim")
        try:
            subprocess.run([editor, temp_filename])
        except FileNotFoundError:
            print(
                "You don't have vim in your system. "
                "Please install it or define your preferred editor as an environment variable EDITOR"
            )
            return stats

    with open(temp_filename) as f:
        customer_branches = f.read().splitlines()

    Path(temp_filename).unlink(missing_ok=True)

    if not customer_branches:
        print("No customer branches to deploy")
        return stats

    print(
        f" - Customers to deploy: {len(customer_branches)}\n"
        f" - Max deploys per batch: {config.max_deploys_per_batch}\n"
        f" - Wait between consecutive batches: {config.wait_between_batches}\n"
    )

    main_branch: str = repo.data["mainbranch"]["name"]

    if input("Proceed? [y/N]") != "y":
        print("Bye!")
        return stats

    deploy_counter = 0

    for cust_branch in tqdm(customer_branches):
        if deploy_counter != 0 and deploy_counter % config.max_deploys_per_batch == 0:
            sleep(config.wait_between_batches)

        try:
            pr = repo.pullrequests.create(
                title="RELEASE",
                source_branch=main_branch,
                destination_branch=cust_branch,
            )
        except Exception as e:
            stats[cust_branch] = "could not create PR. " + str(e)
            continue

        try:
            pr.merge(merge_strategy=pr.MERGE_COMMIT)
        except Exception as e:
            stats[cust_branch] = (
                f"PR created (https://bitbucket.org/{config.workspace}/{repo_name}/pull-requests/{pr.id}) "
                "but could not merge. " + str(e)
            )
            continue
        stats[cust_branch] = "OK!"
        deploy_counter += 1

    return stats


def run():
    """I need to create this function to add scripts to poetry."""

    load_dotenv()
    config = BitbucketConfig()

    stats = deploy(config)
    
    pprint(stats)
    with config.stats_report_file.open("wt") as f:
        writer = csv.writer(f)
        for key, value in stats.items():
            writer.writerow([key, value])

    print(f"{config.stats_report_file.name} file updated")


if __name__ == "__main__":
    run()
