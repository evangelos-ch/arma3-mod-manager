import re
import requests
from bs4 import BeautifulSoup


def get_items(collection_url: str) -> dict:
    page = requests.get(collection_url)
    soup = BeautifulSoup(page.content, "html.parser")
    items = soup.find_all("div", id=lambda x: x and x.startswith("sharedfile_"))
    item_info = []
    for item in items:
        title = item.select("div.workshopItemTitle")[0].text
        _id = item.get("id").split("_")[1]
        item_info.append({"name": title, "id": _id})
    return item_info


def get_item(addon_url: str) -> dict:
    page = requests.get(addon_url)
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.select(".workshopItemTitle")[0].text
    _id_match = re.match(r".*\?id=(\d+).*", addon_url)
    return {"name": title, "id": _id_match.group(1)}
