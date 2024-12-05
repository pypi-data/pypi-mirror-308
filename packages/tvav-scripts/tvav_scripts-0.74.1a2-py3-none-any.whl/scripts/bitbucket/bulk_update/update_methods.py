import io
import yaml
from atlassian.bitbucket import Bitbucket
from atlassian.bitbucket.cloud.repositories import Repository
from requests import HTTPError


def add_main_branch_restrictions(repo: Repository, **_) -> str:
    """Adds restriction to not allow push events to the main branch."""
    # find main branch
    try:
        main_branch = repo.data["mainbranch"]["name"]
    except:
        return "failed to get main branch"

    main_branch_restrictions = [
        {
            'kind': 'push',
            'branch_match_kind': 'glob',
            'branch_pattern': main_branch,
            'value': None,
        },
        {
            'kind': 'force',
            'branch_match_kind': 'glob',
            'branch_pattern': main_branch,
            'value': None,
        },
        {
            'kind': 'require_no_changes_requested',
            'branch_match_kind': 'glob',
            'branch_pattern': main_branch,
            'value': None,
        },
        {
            'kind': 'require_passing_builds_to_merge',
            'branch_match_kind': 'glob',
            'branch_pattern': main_branch,
            'value': 1,
        },
        {
            'kind': 'delete',
            'branch_match_kind': 'glob',
            'branch_pattern': main_branch,
            'value': None,
        },
        {
            'kind': 'require_default_reviewer_approvals_to_merge',
            'branch_match_kind': 'glob',
            'branch_pattern': main_branch,
            'value': 1,
        }
    ]

    # __import__('ipdb').set_trace()

    for restriction in main_branch_restrictions:
        try:
            repo.branch_restrictions.create(**restriction)
        except HTTPError as e:
            if "already exists" in str(e):
                # let's try to update
                b_rest_id = str(e).split(" ")[-1].lstrip("(id=").rstrip(")")
                
                if not b_rest_id.isnumeric():
                    return "failed to get branch restriction id, could not update. " + str(e)

                # update needs different fields
                restriction["id"] = int(b_rest_id)
                restriction["type"] = "branchrestriction"
                restriction["pattern"] = restriction.pop("branch_pattern")

                try:
                    repo.branch_restrictions.get(id=b_rest_id).update(**restriction)
                except Exception as e:
                    return "could not update branch restriction. " + str(e)
                continue
            raise e

    return "okay!"


def update_drone_file_with_cicd_env_variables(workspace: str, client: Bitbucket, repo: Repository) -> str:
    """Updates .drone.yml file to contain cicd-scripts BITBUCKET API env variables."""
    # find main branch
    try:
        main_branch = repo.data["mainbranch"]["name"]
    except:
        return "failed to get main branch"

    try:
        # get drone contents from main branch
        drone_yml = get_repo_file(
            client,
            workspace,
            repo.slug,  # type: ignore
            main_branch,
            ".drone.yml"
        )
    except RuntimeError:
        # if does not have a drone.yml file in the main branch, skip
        return "no drone file"

    # check drone content
    # pyyaml doesn't allow for multiple yaml files inside one file
    drone_obj = yaml.safe_load(drone_yml.replace("---", ""))
    tag_step_found = False
    for i, step in enumerate(drone_obj["steps"]):
        if "tag" in step["name"]:
            tag_step_found = True
            break

    if not tag_step_found:
        # no tag step, no need to update
        return "has drone, but no tag step found"

    if "BITBUCKET__URL" in drone_obj["steps"][i].get("environment", {}):  # type: ignore
        # if secret already in drone, no need to update
        return "has drone, has tag step, no need to update bc already has environment variables"

    drone_obj["steps"][i]["environment"] = {  # type: ignore
        "BITBUCKET__URL": {"from_secret": "bitbucket__url"},
        "BITBUCKET__PROJECT_KEY": {"from_secret": "bitbucket__project_key"},
        "BITBUCKET__APP_USERNAME": {"from_secret": "bitbucket__app_username"},
        "BITBUCKET__APP_PASSWORD": {"from_secret": "bitbucket__app_password"},
    }

    try:
        drone_yml = yaml.safe_dump(drone_obj, sort_keys=False)
        update_repo_file(
            client,
            workspace,
            repo.slug,  # type: ignore
            ".drone.yml",
            drone_yml,
        )
    except Exception:
        return "has drone, has tag step, updated environment, but failed to push update to repo"

    return "okay!"


def update_repo_file(
    client: Bitbucket,
    workspace: str,
    repo_slug: str,
    filename: str,
    content: str
):
    url = "https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/src"
    data = {
        "message": "ci: update .drone_yml with Bitbucket API env variables required by cicd-scripts [CI SKIP]",
    }
    file = io.BytesIO(content.encode())

    res = client._session.post(
        url=url.format(
            workspace=workspace,
            repo_slug=repo_slug,
        ),
        data=data,
        timeout=client.timeout,
        verify=client.verify_ssl,
        proxies=client.proxies,
        cert=client.cert,
        files={filename: file},
    )
    res.raise_for_status()


def get_repo_file(
    client: Bitbucket,
    workspace: str,
    repo_slug: str,
    commit: str,
    path: str
) -> str:
    url = "2.0/repositories/{workspace}/{repo_slug}/src/{commit}/{path}"

    try:
        return client.get(  # type: ignore
            path=url.format(
                workspace=workspace,
                repo_slug=repo_slug,
                commit=commit,
                path=path,
            ),
        )
    except HTTPError as e:
        raise RuntimeError("Could not recover file") from e


