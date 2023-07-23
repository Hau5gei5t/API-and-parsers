import copy
import threading
import time

import schedule
from . import models
from .database import SessionLocal
from time import sleep

from bs4 import BeautifulSoup as bs
import requests


def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run





class UpdateDB:
    def __init__(self):
        self.session = SessionLocal()
        self.BASE_PAGE_URL = r"https://ru.dotabuff.com/heroes/"
        self.HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
        self.PROPERTY = {
            "hero_name": lambda data: self.get_req_hero_name(data),
            "hero_roles": lambda data: data.find("div", class_="header-content-title").h1.small.text.split(", "),
            "popularity": lambda data: data.find("div", "header-content-secondary").dl.dd.text,
            "win_rate": lambda data: float(
                data.find("div", "header-content-secondary").dl.find_next("dl").dd.span.text[:-1]),
            "safe_lane": lambda data: self.get_data_for_lane(data, "safe_lane"),
            "off_lane": lambda data: self.get_data_for_lane(data, "off_lane"),
            "mid_lane": lambda data: self.get_data_for_lane(data, "mid_lane"),
            "ability_build": lambda data: self.get_ability_build(data),
            "used_items": lambda data: self.get_used_items(data),
            "best_versus": lambda data: self.get_heroes(data, True),
            "worst_versus": lambda data: self.get_heroes(data, False),
        }
        self.LANES = {
            "safe_lane": lambda data: data.find_all("tbody")[1].find_all("tr")[0],
            "off_lane": lambda data: data.find_all("tbody")[1].find_all("tr")[1],
            "mid_lane": lambda data: data.find_all("tbody")[1].find_all("tr")[2],
        }

    def format_data(self, html: str, properties: list) -> dict:
        data = {}
        data_html = bs(html, "lxml")
        for prop in properties:
            data[prop] = self.PROPERTY[prop](data_html)
        return data

    def get_req_hero_name(self, data: bs) -> str:
        cdata = copy.copy(data.find("div", class_="header-content-title"))
        cdata.h1.small.extract()
        return cdata.h1.text

    def get_heroes(self, data: bs, best: bool) -> list:
        res = []
        if best:
            data_heroes = data.find_all("tbody")[3].find_all("tr")
        else:
            data_heroes = data.find_all("tbody")[4].find_all("tr")
        for line in data_heroes:
            columns = line.find_all("td")
            res.append({
                "name": columns[1].a.text,
                f"{('disadvantage', 'advantage')[best]}": float(columns[2].text[:-1]),
                "win_rate": float(columns[3].text[:-1]),
                "matches": int(columns[4].text.replace(",", "")),
            })
        return res

    def get_used_items(self, data: bs) -> list:
        res = []
        data_items = data.find_all("tbody")[2].find_all("tr")
        for line in data_items:
            columns = line.find_all("td")
            res.append({
                "name": columns[1].a.text,
                "matches": int(columns[2].text.replace(",", "")),
                "wins": int(columns[3].text.replace(",", "")),
                "win_rate": float(columns[4].text[:-1]),
            })
        return res

    def get_ability_build(self, data: bs) -> list:
        res = []
        data_ab_build = data.find("article", class_="skill-choices smaller").find_all("div", class_="skill")
        for line in data_ab_build:
            ability_name = line.find("div", class_="image-container image-container-bigicon image-container-skill") \
                .a.img.get("alt", "")
            levels_choice = [x.text for x in line.find_all("div", class_="entry choice")]
            res.append({
                "name": ability_name,
                "levels_choice": ", ".join(levels_choice)
            })
        return res

    def format_data_lane(self, res, i):
        res["presence"] = float(i.find_all("td")[1].text[:-1])
        res["win_rate"] = float(i.find_all("td")[2].text[:-1])
        res["kda_ratio"] = float(i.find_all("td")[3].text)
        res["gpm"] = int(i.find_all("td")[4].text)
        res["xpm"] = int(i.find_all("td")[5].text)

    def get_data_for_lane(self, data: bs, lane: str) -> dict:
        res = {}
        for i in data.find_all("tbody")[1].find_all("tr"):
            if lane == "safe_lane" and "Легкая" in i.find_all("td")[0].text:
                self.format_data_lane(res, i)
            elif lane == "off_lane" and "Сложная" in i.find_all("td")[0].text:
                self.format_data_lane(res, i)
            elif lane == "mid_lane" and "Центральная" in i.find_all("td")[0].text:
                self.format_data_lane(res, i)
            else:
                res["presence"] = None
                res["win_rate"] = None
                res["kda_ratio"] = None
                res["gpm"] = None
                res["xpm"] = None

        return res

    def get_html(self, hero_name: str) -> str:
        return requests.get(self.BASE_PAGE_URL + hero_name, headers=self.HEADER).text

    def Hero_DB(self, name, popularity, win_rate):
        hero = self.session.query(models.Hero).filter_by(name=name).first()
        if hero:
            hero.win_rate = win_rate
            hero.popularity = popularity
        else:
            hero = models.Hero(
                name=name,
                popularity=popularity,
                win_rate=win_rate
            )
        return hero

    def Role_DB(self, name, hero):
        role = self.session.query(models.Role).filter_by(name=name).first()
        if role and role not in hero.hero_roles:
            hero.hero_roles.append(role)
        if not role:
            role = models.Role(name=name)
            hero.hero_roles.append(role)
            self.session.add(role)

    def Line_DB(self, hero, type, presence, win_rate, kda_ratio, gpm, xpm):
        match type:
            case "safe":
                line = self.session.query(models.SLine).filter_by(hero_id=hero.id).first()
                if line:
                    line.presence = presence
                    line.win_rate = win_rate
                    line.kda_ratio = kda_ratio
                    line.gpm = gpm
                    line.xpm = xpm
                else:
                    line = models.SLine(
                        presence=presence,
                        win_rate=win_rate,
                        kda_ratio=kda_ratio,
                        gpm=gpm,
                        xpm=xpm
                    )
                    hero.safe_lane = line
                    self.session.add(line)
            case "off":
                line = self.session.query(models.OLine).filter_by(hero_id=hero.id).first()
                if line:
                    line.presence = presence
                    line.win_rate = win_rate
                    line.kda_ratio = kda_ratio
                    line.gpm = gpm
                    line.xpm = xpm
                else:
                    line = models.OLine(
                        presence=presence,
                        win_rate=win_rate,
                        kda_ratio=kda_ratio,
                        gpm=gpm,
                        xpm=xpm
                    )
                    hero.off_lane = line
                    self.session.add(line)
            case "mid":
                line = self.session.query(models.MLine).filter_by(hero_id=hero.id).first()
                if line:
                    line.presence = presence
                    line.win_rate = win_rate
                    line.kda_ratio = kda_ratio
                    line.gpm = gpm
                    line.xpm = xpm
                else:
                    line = models.MLine(
                        presence=presence,
                        win_rate=win_rate,
                        kda_ratio=kda_ratio,
                        gpm=gpm,
                        xpm=xpm
                    )
                    hero.mid_lane = line
                    self.session.add(line)

    def Ability_build_DB(self, hero, name, lvl):
        ability = self.session.query(models.Ability).filter_by(name=name).first()
        if ability:
            ability.levels_choice = lvl
        else:
            ability = models.Ability(
                name=name,
                levels_choice=lvl
            )
            hero.ability_build.append(ability)
            self.session.add(ability)

    def Used_items_DB(self, hero, name, matches, wins, win_rate):
        item = self.session.query(models.Item).filter_by(hero_id=hero.id, name=name).first()
        if item:
            item.win_rate = win_rate
            item.matches = matches
            item.wins = wins
        else:
            item = models.Item(
                name=name,
                wins=wins,
                win_rate=win_rate,
                matches=matches
            )
            hero.used_items.append(item)
            self.session.add(item)

    def vs_DB(self, hero, best, name, adv, win_rate, matches):
        if best:
            vs = self.session.query(models.BestVS).filter_by(hero_id=hero.id, best_vs_hero_name=name).first()
            if vs:
                vs.advantage = adv
                vs.win_rate = win_rate
                vs.matches = matches
            else:
                vs = models.BestVS(
                    best_vs_hero_name=name,
                    advantage=adv,
                    win_rate=win_rate,
                    matches=matches
                )
                hero.best_versus.append(vs)
                self.session.add(vs)
        else:
            vs = self.session.query(models.WorstVS).filter_by(hero_id=hero.id, worst_vs_hero_name=name).first()
            if vs:
                vs.disadvantage = adv
                vs.win_rate = win_rate
                vs.matches = matches
            else:
                vs = models.WorstVS(
                    worst_vs_hero_name=name,
                    disadvantage=adv,
                    win_rate=win_rate,
                    matches=matches
                )
                hero.worst_versus.append(vs)
                self.session.add(vs)

    def save_in_DB(self, res):
        hero = self.Hero_DB(res["hero_name"], res["popularity"], res["win_rate"])
        for i in res["hero_roles"]:
            self.Role_DB(i, hero)
        for i in ["safe", "off", "mid"]:
            self.Line_DB(hero, i, *res[f"{i}_lane"].values())
        for i in res["ability_build"]:
            self.Ability_build_DB(hero, *i.values())
        for i in res["used_items"]:
            self.Used_items_DB(hero, *i.values())
        for i in res["best_versus"]:
            self.vs_DB(hero, True, *i.values())
        for i in res["worst_versus"]:
            self.vs_DB(hero, False, *i.values())
        self.session.add(hero)
        self.session.commit()

    def parse_all_data(self):
        t = bs(open(r"parser.html", encoding="utf-8"), "lxml").find("div", class_="hero-grid").find_all("a")
        t = [x["href"].split("/")[-1] for x in t]
        if t:
            for i in t:
                print(f"parse hero {i}")
                html = self.get_html(i)
                result = self.format_data(html, ["hero_name", "hero_roles", "popularity", "win_rate", "safe_lane",
                                                 "off_lane", "mid_lane", "ability_build",
                                                 "used_items", "best_versus", "worst_versus"])
                print(f"parse hero {i} complete")
                self.save_in_DB(result)
                print(f"save {i} in DB")
                print(f"waiting 15 sec...")
                sleep(15)


db_h = UpdateDB()

schedule.every().sunday.at("00:00").do(db_h.parse_all_data)
