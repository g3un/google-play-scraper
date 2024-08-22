import json
from typing import List, Dict

from google_play_scraper.constants.element import ElementSpecs
from google_play_scraper.constants.regex import Regex
from google_play_scraper.constants.request import Formats
from google_play_scraper.utils.request import post
from google_play_scraper.constants.google_play import Collection, Category

def list(lang: str="en", country: str="us", num: int=100, collection: Collection=Collection.TOP_FREE, category: Category=Category.APPLICATION) -> List[Dict]:
    dom = post(
        Formats.List.build(lang=lang, country=country),
        Formats.List.build_body(num=num, collection=collection.value, category=category.value),
        {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'},
    )

    matches = json.loads(Regex.LIST.findall(dom)[0])
    container = json.loads(matches[0][2])[0][1][0][28][0]

    # Don't use list() here!
    result = []


    for app_info in container:
        info = dict()

        for k, spec in ElementSpecs.List.items():
            content = spec.extract_content(app_info)
            info[k] = content

        result.append(info)

    return result
