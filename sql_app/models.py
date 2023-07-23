from sqlalchemy import  Column, ForeignKey, Integer, String, Float, Table
from sqlalchemy.orm import  Relationship

from .database import Base


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




class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    heroes = Relationship("Hero", secondary=hero_role_association, back_populates="hero_roles")
    name = Column(String, unique=True)




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
