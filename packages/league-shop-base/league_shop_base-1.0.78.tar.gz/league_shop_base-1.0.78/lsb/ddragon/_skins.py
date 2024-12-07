"""Module to parse skins from ddragon"""

import json
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import cast

import requests
import requests_futures.sessions  # type: ignore

from ._ddragon import CHAMPION

__all__ = [
    "get_skins",
    "get_skin_value",
]


SKIN_VALUE_MAPPING = {
    "BUDGET": 1,
    "STANDARD": 2,
    "LIMITED": 2,
    "EPIC": 5,
    "LEGENDARY": 10,
    "ULTIMATE": 100,
    "MYTHIC": 1000,
    "UNKNOWN": 100,
}

ROLES = [
    "Assassin",
    "Fighter",
    "Mage",
    "Marksman",
    "Support",
    "Tank",
]


def get_lane(champion_rates: Dict[str, Any], champion_id: int):
    try:
        data = champion_rates["data"][str(champion_id)]
        data_list = [
            {"lane": k, "play_rate": v["playRate"]} for k, v in data.items()
        ]
        data_list.sort(key=lambda d: d["play_rate"])
        lane = data_list[-1]["lane"]
        if lane == "UTILITY":
            return "SUPPORT"
        return lane
    except KeyError:
        return None


def get_skins(
    patch: str,
    champions: Dict[str, Dict[str, Any]],
    champion_rates: Dict[str, Any],
):
    """Returns a list of skins data with values id, name, champion and tier`, returns None on error"""
    try:
        session = requests_futures.sessions.FuturesSession()
        futures = [
            {
                "future": session.get(  # type: ignore
                    CHAMPION.format(patch=patch, champion=k)
                ),
                "champion": {"name": k, "id": int(v["key"])},
            }
            for k, v in champions["data"].items()
        ]
        skins: List[Dict[str, Any]] = []
        for future in futures:
            champion: Dict[str, Any] = future["champion"]  # type: ignore
            response = cast(Dict[str, Any], future["future"].result().json())  # type: ignore
            champion_data = response["data"][champion["name"]]
            for skin in response["data"][champion["name"]]["skins"]:
                if skin["name"] == "default":
                    continue
                champion["roles"] = ", ".join(
                    t for t in champion_data["tags"] if t in ROLES
                )
                champion["lanes"] = get_lane(
                    champion_rates, champion_data["key"]
                )
                skins.append(
                    {
                        "id": skin["id"],
                        "name": skin["name"],
                        "champion": champion,
                        "tier": "STANDARD",
                    }
                )
        return skins
    except (
        requests.exceptions.RequestException,
        json.decoder.JSONDecodeError,
    ):
        return None


def get_skin_value(
    skin_id: int,
    skin_tier: str,
    top_sold_value_mapping: Dict[int, int],
    release_date: Optional[str] = None,
):
    value_by_tier = SKIN_VALUE_MAPPING.get(skin_tier, 100)
    try:
        if value_by_tier < 100 and release_date is not None:
            days_old = (
                datetime.now() - datetime.strptime(release_date, "%Y-%m-%d")
            ).days
            if days_old < 365:
                return 100
    except ValueError:
        pass
    if value_by_tier < 100 and skin_id in top_sold_value_mapping:
        return top_sold_value_mapping[skin_id]
    return value_by_tier
