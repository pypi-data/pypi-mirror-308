"""Module to parse data from ddragon"""

from typing import Any
from typing import Dict
from typing import List

import json

import requests

VERSIONS = "http://ddragon.leagueoflegends.com/api/versions.json"
CHAMPIONS = (
    "http://ddragon.leagueoflegends.com/cdn/{patch}/data/en_US/champion.json"
)
CHAMPION = "http://ddragon.leagueoflegends.com/cdn/{patch}/data/en_US/champion/{champion}.json"
RUNES = "http://ddragon.leagueoflegends.com/cdn/{patch}/data/en_US/runesReforged.json"


__all__ = [
    "get_patch",
    "get_champions",
    "get_champions_mapping",
    "get_runes",
    "get_rune_slots",
    "get_rune_category",
    "get_rune_name",
]


def get_patch(index: int = 0):
    """Parses patch from ddragon"""
    try:
        response = requests.get(VERSIONS)
        if response.ok:
            return response.json()[index]
        return None
    except (
        requests.exceptions.RequestException,
        json.decoder.JSONDecodeError,
        IndexError,
    ):
        return None


def get_champions(patch: str):
    """Parses champions from ddragon"""
    try:
        url = CHAMPIONS.format(patch=patch)
        return requests.get(url).json()
    except (
        requests.exceptions.RequestException,
        json.decoder.JSONDecodeError,
    ):
        return None


def get_champions_mapping(patch: str):
    """Parses champions from ddragon"""
    champions = get_champions(patch)
    if champions is None:
        return None
    return {k: int(v["key"]) for k, v in champions["data"].items()}


def get_runes(patch: str):
    """Parses runes from ddragon"""
    try:
        url = RUNES.format(patch=patch)
        return requests.get(url).json()
    except (
        requests.exceptions.RequestException,
        json.decoder.JSONDecodeError,
    ):
        return None


def get_rune_slots(runes: List[Dict[str, Any]]):
    """Creates rune id to slot mapping"""
    slots: Dict[str, int] = {}
    for category in runes:
        for i, slot in enumerate(category["slots"]):
            for rune in slot["runes"]:
                slots[rune["id"]] = i
    return slots


def get_rune_category(runes: List[Dict[str, Any]]):
    """Creates rune id to category mapping"""
    output: Dict[str, Any] = {}
    for category in runes:
        for slot in category["slots"]:
            for rune in slot["runes"]:
                output[rune["id"]] = category["id"]
    return output


def get_rune_name(runes: List[Dict[str, Any]]):
    """Creates rune id to rune name mapping"""
    output: Dict[str, str] = {}
    for category in runes:
        for slot in category["slots"]:
            for rune in slot["runes"]:
                output[rune["id"]] = rune["key"]
    return output
