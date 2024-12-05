import json
import logging
import os
import requests
from dotenv import load_dotenv
from pathlib import Path


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__.split("/")[-1].rstrip(".py"))
VERICAST_API = "https://api-vericast-private.bmat.me"


def get_customer_id_by_name(customer_name: str) -> str:
    """Get customer_id from Vericast API using its name."""
    try:
        customer_id = requests.get(
            url=VERICAST_API + "/customers/"+customer_name
        ).json()["items"][0]["id"]
    except Exception as e:
        raise RuntimeError(
            "Could not get customer_id for %s" % customer_name
        ) from e

    logger.info(f"{customer_name=} --> {customer_id=}")
    return customer_id


def get_sigpools_by_customer_id(customer_id: str) -> list[str]:
    """Get sigpool list for a specific customer_id."""
    logger.info(f"Getting sigpools for {customer_id=}")

    sigpools = set()
    offset, has_more = 0, True
    while has_more:
        res = requests.get(
            url=VERICAST_API + "/subscriptions",
            params={
                "customer_id": customer_id,
                "offset": offset,
                "limit": 100_000,
            }
        ).json()
        has_more = res["has_more"]
        offset += len(res["items"])

        for subscription in res["items"]:
            sigpool_type = subscription["match_role"]["firstlayer_fptype_name"]
            sigpool_name = subscription["signature_pool"]["collection"]["name"]
            sigpool = f"{sigpool_name}_{sigpool_type}"
            sigpools.add(sigpool)

    logger.info(f"Found {len(sigpools)} sigpools for {customer_name=}")
    return list(sigpools)


if __name__ == "__main__":
    load_dotenv()

    sigpools_json = Path("sigpools.json")
    customer_name = os.getenv("CUSTOMER_NAME")

    if not customer_name:
        raise RuntimeError(f"{customer_name=}")

    customer_id = get_customer_id_by_name(customer_name)
    sigpools = get_sigpools_by_customer_id(customer_id)

    logger.info(f"Writing {len(sigpools)} sigpools to file {sigpools_json.name}")
    with sigpools_json.open("wt") as f:
        json.dump(sigpools, f)

    logger.info("DONE")
