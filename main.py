from bs4 import BeautifulSoup as bs
import requests
import json

BASE_PAGE_URL = r"https://ru.dotabuff.com/heroes/"
HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
PROPERTY = {
    "popularity": lambda data: data.find("div", "header-content-secondary").dl.dd.text,
    "win_rate": lambda data: data.find("div", "header-content-secondary").dl.find_next("dl").dd.span.text,
    "safe_lane": lambda data: get_data_for_lane(data, "safe_lane"),
    "off_lane": lambda data: get_data_for_lane(data, "off_lane"),
    "mid_lane": lambda data: get_data_for_lane(data, "mid_lane"),
    "ability_build": lambda data: get_ability_build(data),
    "used_items": lambda data: get_used_items(data),
    "best_versus": lambda data: get_heroes(data, True),
    "worst_versus": lambda data: get_heroes(data, False),
}
LANES = {
    "safe_lane": lambda data: data.find_all("tbody")[1].find_all("tr")[0],
    "off_lane": lambda data: data.find_all("tbody")[1].find_all("tr")[1],
    "mid_lane": lambda data: data.find_all("tbody")[1].find_all("tr")[2],
}


def get_heroes(data: bs, best: bool) -> list:
    res = []
    if best:
        data_heroes = data.find_all("tbody")[3].find_all("tr")
    else:
        data_heroes = data.find_all("tbody")[4].find_all("tr")
    for line in data_heroes:
        columns = line.find_all("td")
        res.append({
            "name": columns[1].a.text,
            f"{('disadvantage', 'advantage')[best]}": columns[2].text,
            "win_rate": columns[3].text,
            "matches": int(columns[4].text.replace(",", "")),
        })
    return res


def get_used_items(data: bs) -> list:
    res = []
    data_items = data.find_all("tbody")[2].find_all("tr")
    for line in data_items:
        columns = line.find_all("td")
        res.append({
            "name": columns[1].a.text,
            "matches": int(columns[2].text.replace(",", "")),
            "wins": int(columns[3].text.replace(",", "")),
            "win_rate": columns[4].text,
        })
    return res


def get_ability_build(data: bs) -> list:
    res = []
    data_ab_build = data.find("article", class_="skill-choices smaller").find_all("div", class_="skill")
    for line in data_ab_build:
        ability_name = line.find("div", class_="image-container image-container-bigicon image-container-skill") \
            .a.img.get("alt", "")
        levels_choice = [int(x.text) for x in line.find_all("div", class_="entry choice")]
        res.append({
            "name": ability_name,
            "levels_choice": levels_choice
        })
    return res


def get_data_for_lane(data: bs, lane: str) -> dict:
    res = {}
    data_line = LANES[lane](data)
    res["presence"] = data_line.find_all("td")[1].text
    res["win_rate"] = data_line.find_all("td")[2].text
    res["kda_ratio"] = float(data_line.find_all("td")[3].text)
    res["gpm"] = int(data_line.find_all("td")[4].text)
    res["xpm"] = int(data_line.find_all("td")[5].text)
    return res


def get_html(hero_name: str) -> str:
    return requests.get(BASE_PAGE_URL + hero_name, headers=HEADER).text


def format_data(html: str, properties: list) -> dict:
    data = {}
    if DEBUG:
        data_html = bs(open("test.html", encoding="utf-8"), "lxml")
    else:
        data_html = bs(html, "lxml")
    for prop in properties:
        data[prop] = PROPERTY[prop](data_html)
    return data


if __name__ == "__main__":
    DEBUG = True
    if DEBUG:
        result = format_data("", ["popularity", "win_rate", "safe_lane",
                                  "off_lane", "mid_lane", "ability_build",
                                  "used_items", "best_versus", "worst_versus"])
    else:
        html = get_html(input())
        result = format_data(html, ["popularity", "win_rate", "safe_lane",
                                    "off_lane", "mid_lane", "ability_build",
                                    "used_items", "best_versus", "worst_versus"])
    result = json.dumps(result)
    print(result)
