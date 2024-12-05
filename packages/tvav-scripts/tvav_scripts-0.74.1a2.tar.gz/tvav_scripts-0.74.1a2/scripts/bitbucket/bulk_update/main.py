import importlib
import tqdm
from atlassian.bitbucket import Bitbucket
from atlassian.bitbucket.cloud import Cloud
from atlassian.bitbucket.cloud.repositories import Repository
from dotenv import load_dotenv
from pathlib import Path
from pprint import pprint
from pydantic_settings import BaseSettings
from typing import List, Optional, Protocol


class BitbucketConfig(BaseSettings):
    url: str
    app_username: str
    app_password: str
    workspace: str = "bmat-music"
    project: str = "TVAV"

    repos_to_check_txt: Optional[str]
    update_fn_name: str


class UpdateFn(Protocol):
    def __call__(
        self,
        workspace: str,
        client: Bitbucket,
        repo: Repository,
    ) -> str:
        ...


def update_bitbucket_repos(
    url: str,
    username: str,
    password: str,
    workspace: str,
    project: str,
    update_fn: UpdateFn,
    repos_to_check: Optional[List[str]] = None,
) -> dict:
    """Perform Bitbucket project-wide updates."""
    # just to collect stats
    stats = {}

    if repos_to_check is None:
        repos_to_check = []

    # simple client for custom requests
    client = Bitbucket(
        url=url,
        username=username,
        password=password,
        backoff_and_retry=True,
    )
    # cloud client with Objects and generators
    cloud = Cloud(
        url=url,
        username=username,
        password=password,
        backoff_and_retry=True,
    )

    # consume all repos to store them in memory
    # and for tqdm to show a simple progress bar
    repositories = [
        _
        for _ in cloud.workspaces.get(
            workspace
        ).projects.get(
            project
        ).repositories.each()
    ]

    # optionally filter repos
    if len(repos_to_check) > 0:
        repositories = filter(
            lambda r: r.name in repos_to_check,
            repositories
        )

    for repo in tqdm.tqdm(repositories):
        try:
            out = update_fn(
                workspace=workspace,
                client=client,
                repo=repo,
            )
        except Exception as e:
            stats[repo.name] = str(e)
        else:
            stats[repo.name] = out

    return stats


if __name__ == "__main__":
    load_dotenv()
    config = BitbucketConfig()  # type: ignore

    cur_dir = Path(__file__).parent

    update_fn = getattr(
        importlib.import_module("update_methods", package="."),
        config.update_fn_name
    )

    repos_to_check = []
    if config.repos_to_check_txt:
        repos_to_check_txt = cur_dir / config.repos_to_check_txt
        if (
            repos_to_check_txt.exists() and
            repos_to_check_txt.is_file()
        ):
            with repos_to_check_txt.open() as f:
                repos_to_check = [
                    line
                    for line in f.read().split("\n")
                    if line not in ["", " ", "\n"]
                ]

    stats = update_bitbucket_repos(
        url=config.url,
        username=config.app_username,
        password=config.app_password,
        workspace=config.workspace,
        project=config.project,
        update_fn=update_fn,
        repos_to_check=repos_to_check,
    )
    
    with (cur_dir / "stats.csv").open("wt") as f:
        for key, value in stats.items():
            f.write(f"{key},{value}\n")

    pprint(stats)
    print("stats.txt file updated")
