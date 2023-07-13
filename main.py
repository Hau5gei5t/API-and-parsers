import copy
from time import sleep

from bs4 import BeautifulSoup as bs
import requests
import json

from sqlalchemy import create_engine, text, Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import declarative_base, Session, Relationship

Base = declarative_base()

hero_role_association = Table("hero_role_association", Base.metadata,
                              Column("hero_id", Integer, ForeignKey("heroes.id")),
                              Column("role_id", Integer, ForeignKey("roles.id")), )


class Hero(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String, unique=True)
    hero_roles = Relationship("Role", secondary=hero_role_association, back_populates="heroes")
    popularity = Column(String)
    win_rate = Column(Float)
    safe_lane = Relationship("SLine", uselist=False, backref="heroes")
    off_lane = Relationship("OLine", uselist=False, backref="heroes")
    mid_lane = Relationship("MLine", uselist=False, backref="heroes")
    ability_build = Relationship("Ability", backref="heroes")
    used_items = Relationship("Item", backref="heroes")
    best_versus = Relationship("BestVS", backref="heroes")
    worst_versus = Relationship("WorstVS", backref="heroes")

    def __repr__(self):
        return f"{self.name} {', '.join(self.roles)} {self.win_rate}%"


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    heroes = Relationship("Hero", secondary=hero_role_association, back_populates="hero_roles")
    name = Column(String, unique=True)

    def __repr__(self):
        return self.name


class SLine(Base):
    __tablename__ = "s_lines"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    hero_id = Column(Integer, ForeignKey("heroes.id"), unique=True)
    presence = Column(Float)
    win_rate = Column(Float)
    kda_ratio = Column(Float)
    gpm = Column(Integer)
    xpm = Column(Integer)


class OLine(Base):
    __tablename__ = "o_lines"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    hero_id = Column(Integer, ForeignKey("heroes.id"), unique=True)
    presence = Column(Float)
    win_rate = Column(Float)
    kda_ratio = Column(Float)
    gpm = Column(Integer)
    xpm = Column(Integer)


class MLine(Base):
    __tablename__ = "m_lines"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    hero_id = Column(Integer, ForeignKey("heroes.id"), unique=True)
    presence = Column(Float)
    win_rate = Column(Float)
    kda_ratio = Column(Float)
    gpm = Column(Integer)
    xpm = Column(Integer)


class Ability(Base):
    __tablename__ = "abilities"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    hero_id = Column(Integer, ForeignKey("heroes.id"))
    name = Column(String, unique=True)
    levels_choice = Column(String)

    def __repr__(self):
        return f"{self.heroes.name} -> {self.name} -> [{self.levels_choice}]"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    hero_id = Column(Integer, ForeignKey("heroes.id"))
    name = Column(String)
    matches = Column(Integer)
    wins = Column(Integer)
    win_rate = Column(Float)


class BestVS(Base):
    __tablename__ = "b_vs"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    hero_id = Column(Integer, ForeignKey("heroes.id"))
    best_vs_hero_name = Column(String)
    advantage = Column(Float)
    win_rate = Column(Float)
    matches = Column(Integer)

    def __repr__(self):
        return f"{self.heroes.name} VS {self.best_vs_hero_name} -> {self.advantage}"


class WorstVS(Base):
    __tablename__ = "w_vs"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    hero_id = Column(Integer, ForeignKey("heroes.id"))
    worst_vs_hero_name = Column(String)
    disadvantage = Column(Float)
    win_rate = Column(Float)
    matches = Column(Integer)

    def __repr__(self):
        return f"{self.heroes.name} VS {self.worst_vs_hero_name} -> {self.disadvantage}"


engine = create_engine(r'sqlite:///heroes.sqlite')
Base.metadata.create_all(bind=engine)
#
session = Session(bind=engine)


def Hero_DB(name, popularity, win_rate):
    hero = session.query(Hero).filter_by(name=name).first()
    if hero:
        hero.win_rate = win_rate
        hero.popularity = popularity
    else:
        hero = Hero(
            name=name,
            popularity=popularity,
            win_rate=win_rate
        )
    return hero


def Role_DB(name, hero):
    role = session.query(Role).filter_by(name=name).first()
    if role and role not in hero.hero_roles:
        hero.hero_roles.append(role)
    if not role:
        role = Role(name=name)
        hero.hero_roles.append(role)
        session.add(role)


def Line_DB(hero, type, presence, win_rate, kda_ratio, gpm, xpm):
    match type:
        case "safe":
            line = session.query(SLine).filter_by(hero_id=hero.id).first()
            if line:
                line.presence = presence
                line.win_rate = win_rate
                line.kda_ratio = kda_ratio
                line.gpm = gpm
                line.xpm = xpm
            else:
                line = SLine(
                    presence=presence,
                    win_rate=win_rate,
                    kda_ratio=kda_ratio,
                    gpm=gpm,
                    xpm=xpm
                )
                hero.safe_lane = line
                session.add(line)
        case "off":
            line = session.query(OLine).filter_by(hero_id=hero.id).first()
            if line:
                line.presence = presence
                line.win_rate = win_rate
                line.kda_ratio = kda_ratio
                line.gpm = gpm
                line.xpm = xpm
            else:
                line = OLine(
                    presence=presence,
                    win_rate=win_rate,
                    kda_ratio=kda_ratio,
                    gpm=gpm,
                    xpm=xpm
                )
                hero.off_lane = line
                session.add(line)
        case "mid":
            line = session.query(MLine).filter_by(hero_id=hero.id).first()
            if line:
                line.presence = presence
                line.win_rate = win_rate
                line.kda_ratio = kda_ratio
                line.gpm = gpm
                line.xpm = xpm
            else:
                line = MLine(
                    presence=presence,
                    win_rate=win_rate,
                    kda_ratio=kda_ratio,
                    gpm=gpm,
                    xpm=xpm
                )
                hero.mid_lane = line
                session.add(line)


def Ability_build_DB(hero, name, lvl):
    ability = session.query(Ability).filter_by(name=name).first()
    if ability:
        ability.levels_choice = lvl
    else:
        ability = Ability(
            name=name,
            levels_choice=lvl
        )
        hero.ability_build.append(ability)
        session.add(ability)


def Used_items_DB(hero, name, matches, wins, win_rate):
    item = session.query(Item).filter_by(hero_id=hero.id, name=name).first()
    if item:
        item.win_rate = win_rate
        item.matches = matches
        item.wins = wins
    else:
        item = Item(
            name=name,
            wins=wins,
            win_rate=win_rate,
            matches=matches
        )
        hero.used_items.append(item)
        session.add(item)


def vs_DB(hero, best, name, adv, win_rate, matches):
    if best:
        vs = session.query(BestVS).filter_by(hero_id=hero.id, best_vs_hero_name=name).first()
        if vs:
            vs.advantage = adv
            vs.win_rate = win_rate
            vs.matches = matches
        else:
            vs = BestVS(
                best_vs_hero_name=name,
                advantage=adv,
                win_rate=win_rate,
                matches=matches
            )
            hero.best_versus.append(vs)
            session.add(vs)
    else:
        vs = session.query(WorstVS).filter_by(hero_id=hero.id, worst_vs_hero_name=name).first()
        if vs:
            vs.disadvantage = adv
            vs.win_rate = win_rate
            vs.matches = matches
        else:
            vs = WorstVS(
                worst_vs_hero_name=name,
                disadvantage=adv,
                win_rate=win_rate,
                matches=matches
            )
            hero.worst_versus.append(vs)
            session.add(vs)


def save_in_DB(res):
    hero = Hero_DB(res["hero_name"], res["popularity"], res["win_rate"])
    for i in res["hero_roles"]:
        Role_DB(i, hero)
    for i in ["safe", "off", "mid"]:
        Line_DB(hero, i, *res[f"{i}_lane"].values())
    for i in res["ability_build"]:
        Ability_build_DB(hero, *i.values())
    for i in res["used_items"]:
        Used_items_DB(hero, *i.values())
    for i in res["best_versus"]:
        vs_DB(hero, True, *i.values())
    for i in res["worst_versus"]:
        vs_DB(hero, False, *i.values())
    session.add(hero)
    session.commit()


# exit()

BASE_PAGE_URL = r"https://ru.dotabuff.com/heroes/"
HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
PROPERTY = {
    "hero_name": lambda data: get_req_hero_name(data),
    "hero_roles": lambda data: data.find("div", class_="header-content-title").h1.small.text.split(", "),
    "popularity": lambda data: data.find("div", "header-content-secondary").dl.dd.text,
    "win_rate": lambda data: float(data.find("div", "header-content-secondary").dl.find_next("dl").dd.span.text[:-1]),
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


def get_req_hero_name(data: bs) -> str:
    cdata = copy.copy(data.find("div", class_="header-content-title"))
    cdata.h1.small.extract()
    return cdata.h1.text


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
            f"{('disadvantage', 'advantage')[best]}": float(columns[2].text[:-1]),
            "win_rate": float(columns[3].text[:-1]),
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
            "win_rate": float(columns[4].text[:-1]),
        })
    return res


def get_ability_build(data: bs) -> list:
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


def format_data_lane(res, i):
    res["presence"] = float(i.find_all("td")[1].text[:-1])
    res["win_rate"] = float(i.find_all("td")[2].text[:-1])
    res["kda_ratio"] = float(i.find_all("td")[3].text)
    res["gpm"] = int(i.find_all("td")[4].text)
    res["xpm"] = int(i.find_all("td")[5].text)


def get_data_for_lane(data: bs, lane: str) -> dict:
    res = {}
    for i in data.find_all("tbody")[1].find_all("tr"):
        if lane == "safe_lane" and "Легкая" in i.find_all("td")[0].text:
            format_data_lane(res, i)
        elif lane == "off_lane" and "Сложная" in i.find_all("td")[0].text:
            format_data_lane(res, i)
        elif lane == "mid_lane" and "Центральная" in i.find_all("td")[0].text:
            format_data_lane(res, i)
        else:
            res["presence"] = None
            res["win_rate"] = None
            res["kda_ratio"] = None
            res["gpm"] = None
            res["xpm"] = None

    return res


def get_html(hero_name: str) -> str:
    return requests.get(BASE_PAGE_URL + hero_name, headers=HEADER).text


def format_data(html: str, properties: list) -> dict:
    data = {}
    if DEBUG:
        data_html = bs(open("test2.html", encoding="utf-8"), "lxml")
    else:
        data_html = bs(html, "lxml")
    for prop in properties:
        data[prop] = PROPERTY[prop](data_html)
    return data


if __name__ == "__main__":
    DEBUG = False
    PARSE_ALL = True
    t = None
    if DEBUG:
        result = format_data("", ["hero_name", "hero_roles", "popularity", "win_rate", "safe_lane",
                                  "off_lane", "mid_lane", "ability_build",
                                  "used_items", "best_versus", "worst_versus"])
    else:
        if PARSE_ALL:
            t = bs(open("parser.html", encoding="utf-8"), "lxml").find("div", class_="hero-grid").find_all("a")
            t = [x["href"].split("/")[-1] for x in t]
        if t:
            for i in t:
                print(f"parse hero {i}")
                html = get_html(i)
                result = format_data(html, ["hero_name", "hero_roles", "popularity", "win_rate", "safe_lane",
                                            "off_lane", "mid_lane", "ability_build",
                                            "used_items", "best_versus", "worst_versus"])
                print(f"parse hero {i} complete")
                save_in_DB(result)
                print(f"save {i} in DB")
                print(f"waiting 15 sec...")
                sleep(15)
        else:
            html = get_html(input())
            result = format_data(html, ["hero_name", "hero_roles", "popularity", "win_rate", "safe_lane",
                                        "off_lane", "mid_lane", "ability_build",
                                        "used_items", "best_versus", "worst_versus"])
            save_in_DB(result)
