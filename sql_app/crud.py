from sqlalchemy.orm import Session

from . import models, schemas


# GET Section
## Hero
def get_heroes(db: Session, limit: int, offset: int):
    return db.query(models.Hero).offset(offset).limit(limit).all()


def get_hero(db: Session, hero_id: int):
    return db.query(models.Hero).filter(models.Hero.id == hero_id).first()


def get_hero_by_name(db: Session, hero_name: str):
    return db.query(models.Hero).filter(models.Hero.name == hero_name).first()


## Role
def get_roles(db: Session, limit: int = 31, offset: int = 0):
    return db.query(models.Role).offset(offset).limit(limit).all()


def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def get_role_by_name(db: Session, role_name: str):
    return db.query(models.Role).filter(models.Role.name == role_name).first()


## SLine
def get_s_lines(db: Session, limit: int = 31, offset: int = 0):
    return db.query(models.SLine).offset(offset).limit(limit).all()


def get_s_line(db: Session, line_id: int):
    return db.query(models.SLine).filter(models.SLine.id == line_id).first()


def get_s_line_by_hero_id(db: Session, hero_id: int):
    return db.query(models.SLine).filter(models.SLine.hero_id == hero_id).first()


## OLine
def get_o_lines(db: Session, limit: int = 31, offset: int = 0):
    return db.query(models.OLine).offset(offset).limit(limit).all()


def get_o_line(db: Session, line_id: int):
    return db.query(models.OLine).filter(models.OLine.id == line_id).first()


def get_o_line_by_hero_id(db: Session, hero_id: int):
    return db.query(models.OLine).filter(models.OLine.hero_id == hero_id).first()


## MLine
def get_m_lines(db: Session, limit: int = 31, offset: int = 0):
    return db.query(models.MLine).offset(offset).limit(limit).all()


def get_m_line(db: Session, line_id: int):
    return db.query(models.MLine).filter(models.MLine.id == line_id).first()


def get_m_line_by_hero_id(db: Session, hero_id: int):
    return db.query(models.MLine).filter(models.MLine.hero_id == hero_id).first()


## Ability
def get_abilities(db: Session, limit: int = 31, offset: int = 0):
    return db.query(models.Ability).offset(offset).limit(limit).all()


def get_abilities_by_hero_id(db: Session, hero_id: int, limit: int = 6, offset: int = 0):
    return db.query(models.Ability).filter(models.Ability.hero_id == hero_id).offset(offset).limit(limit).all()


def get_ability(db: Session, ability_id: int):
    return db.query(models.Ability).filter(models.Ability.id == ability_id).first()


def get_ability_by_name(db: Session, ability_name: str):
    return db.query(models.Ability).filter(models.Ability.name == ability_name).first()


## Item
def get_items(db: Session, limit: int = 31, offset: int = 0):
    return db.query(models.Item).offset(offset).limit(limit).all()


def get_items_by_hero_id(db: Session, hero_id: int, limit: int = 12, offset: int = 0):
    return db.query(models.Item).filter(models.Item.hero_id == hero_id).offset(offset).limit(limit).all()


def get_items_by_name(db: Session, item_name: str, limit: int = 12, offset: int = 0):
    return db.query(models.Item).filter(models.Item.name == item_name).offset(offset).limit(limit).all()


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_item_by_hero_id_and_item_name(db: Session, hero_id: int, item_name: str):
    return db.query(models.Item).filter(models.Item.name == item_name).filter(models.Item.hero_id == hero_id).first()


## BestVersus
def get_best_versus_heroes(db: Session, limit: int = 10, offset: int = 0):
    return db.query(models.BestVS).offset(offset).limit(limit).all()


def get_best_versus_heroes_by_hero_id(db: Session, hero_id: int, limit: int = 12, offset: int = 0):
    return db.query(models.BestVS).filter(models.BestVS.hero_id == hero_id).offset(offset).limit(limit).all()


def get_best_versus_hero(db: Session, id: int):
    return db.query(models.BestVS).filter(models.BestVS.id == id).first()


## WorstVersus
def get_worst_versus_heroes(db: Session, limit: int = 10, offset: int = 0):
    return db.query(models.WorstVS).offset(offset).limit(limit).all()


def get_worst_versus_heroes_by_hero_id(db: Session, hero_id: int, limit: int = 12, offset: int = 0):
    return db.query(models.WorstVS).filter(models.WorstVS.hero_id == hero_id).offset(offset).limit(limit).all()


def get_worst_versus_hero(db: Session, id: int):
    return db.query(models.WorstVS).filter(models.WorstVS.id == id).first()


# Create Section

def create_hero(db: Session, hero: schemas.HeroCreate):
    db_hero = models.Hero(
        name=hero.name,
        popularity=hero.popularity,
        win_rate=hero.win_rate
    )
    db.add(db_hero)
    db.commit()
    db.refresh(db_hero)
    return db_hero


def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(
        name=role.name
    )
    db_role.heroes.append(get_hero_by_name(db, role.hero_name))
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def create_s_line(db: Session, s_line: schemas.LineCreate):
    db_s_line = models.SLine(
        presence=s_line.presence,
        win_rate=s_line.win_rate,
        kda_ratio=s_line.kda_ratio,
        gpm=s_line.gpm,
        xpm=s_line.xpm
    )
    get_hero_by_name(db, s_line.hero_name).safe_lane = db_s_line
    db.add(db_s_line)
    db.commit()
    db.refresh(db_s_line)
    return db_s_line


def create_o_line(db: Session, o_line: schemas.LineCreate):
    db_o_line = models.OLine(
        presence=o_line.presence,
        win_rate=o_line.win_rate,
        kda_ratio=o_line.kda_ratio,
        gpm=o_line.gpm,
        xpm=o_line.xpm
    )
    get_hero_by_name(db, o_line.hero_name).off_lane = db_o_line
    db.add(db_o_line)
    db.commit()
    db.refresh(db_o_line)
    return db_o_line


def create_m_line(db: Session, m_line: schemas.LineCreate):
    db_m_line = models.MLine(
        presence=m_line.presence,
        win_rate=m_line.win_rate,
        kda_ratio=m_line.kda_ratio,
        gpm=m_line.gpm,
        xpm=m_line.xpm
    )
    get_hero_by_name(db, m_line.hero_name).mid_lane = db_m_line
    db.add(db_m_line)
    db.commit()
    db.refresh(db_m_line)
    return db_m_line


def create_ability(db: Session, ability: schemas.AbilityCreate):
    db_ability = models.Ability(
        name=ability.name,
        levels_choice=", ".join(map(str, ability.levels_choice))
    )
    get_hero_by_name(db, ability.hero_name).ability_build.append(db_ability)
    db.add(db_ability)
    db.commit()
    db.refresh(db_ability)
    return db_ability


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(
        name=item.name,
        wins=item.wins,
        win_rate=item.win_rate,
        matches=item.matches
    )
    get_hero_by_name(db, item.hero_name).used_items.append(db_item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_best_vs_hero(db: Session, b_vs_hero: schemas.BestVSCreate):
    db_best_vs_hero = models.BestVS(
        best_vs_hero_name=b_vs_hero.best_vs_hero_name,
        advantage=b_vs_hero.advantage,
        win_rate=b_vs_hero.win_rate,
        matches=b_vs_hero.matches
    )
    get_hero_by_name(db, b_vs_hero.hero_name).best_versus.append(db_best_vs_hero)
    db.add(db_best_vs_hero)
    db.commit()
    db.refresh(db_best_vs_hero)
    return db_best_vs_hero


def create_worst_vs_hero(db: Session, w_vs_hero: schemas.WorstVSCreate):
    db_worst_vs_hero = models.WorstVS(
        worst_vs_hero_name=w_vs_hero.worst_vs_hero_name,
        disadvantage=w_vs_hero.disadvantage,
        win_rate=w_vs_hero.win_rate,
        matches=w_vs_hero.matches
    )
    get_hero_by_name(db, w_vs_hero.hero_name).worst_versus.append(db_worst_vs_hero)
    db.add(db_worst_vs_hero)
    db.commit()
    db.refresh(db_worst_vs_hero)
    return db_worst_vs_hero


# Update Section

def update_hero(db: Session, new_hero: schemas.HeroUpdate):
    db_hero = get_hero_by_name(db, new_hero.name)
    if new_hero.new_win_rate:
        db_hero.win_rate = new_hero.new_win_rate
    if new_hero.new_name:
        db_hero.name = new_hero.new_name
    if new_hero.new_popularity:
        db_hero.popularity = new_hero.new_popularity
    db.commit()
    db.refresh(db_hero)
    return db_hero


def add_role_to_hero(db: Session, data: schemas.RoleAdd):
    hero = get_hero_by_name(db, data.hero_name)
    role = get_role_by_name(db, data.role_name)
    hero.hero_roles.append(role)
    db.commit()
    db.refresh(hero)
    db.refresh(role)
    return hero


def update_role(db: Session, new_role: schemas.RoleUpdate):
    db_role = get_role_by_name(db, new_role.name)
    db_role.name = new_role.new_name
    db.commit()
    db.refresh(db_role)
    return db_role


def update_safe_line(db: Session, line: schemas.LineCreate):
    db_hero_id = get_hero_by_name(db, line.hero_name).id
    db_line = get_s_line_by_hero_id(db, db_hero_id)
    if line.presence:
        db_line.presence = line.presence
    if line.win_rate:
        db_line.win_rate = line.win_rate
    if line.kda_ratio:
        db_line.kda_ratio = line.kda_ratio
    if line.gpm:
        db_line.gpm = line.gpm
    if line.xpm:
        db_line.xpm = line.xpm
    db.commit()
    db.refresh(db_line)
    return db_line


def update_off_line(db: Session, line: schemas.LineCreate):
    db_hero_id = get_hero_by_name(db, line.hero_name).id
    db_line = get_o_line_by_hero_id(db, db_hero_id)
    if line.presence:
        db_line.presence = line.presence
    if line.win_rate:
        db_line.win_rate = line.win_rate
    if line.kda_ratio:
        db_line.kda_ratio = line.kda_ratio
    if line.gpm:
        db_line.gpm = line.gpm
    if line.xpm:
        db_line.xpm = line.xpm
    db.commit()
    db.refresh(db_line)
    return db_line


def update_mid_line(db: Session, line: schemas.LineCreate):
    db_hero_id = get_hero_by_name(db, line.hero_name).id
    db_line = get_m_line_by_hero_id(db, db_hero_id)
    if line.presence:
        db_line.presence = line.presence
    if line.win_rate:
        db_line.win_rate = line.win_rate
    if line.kda_ratio:
        db_line.kda_ratio = line.kda_ratio
    if line.gpm:
        db_line.gpm = line.gpm
    if line.xpm:
        db_line.xpm = line.xpm
    db.commit()
    db.refresh(db_line)
    return db_line


def update_ability(db: Session, ability: schemas.AbilityUpdate):
    db_ability = get_ability_by_name(db, ability.name)
    if ability.new_name:
        db_ability.name = ability.new_name
    if ability.new_levels_choice:
        db_ability.levels_choice = ", ".join(map(str, ability.new_levels_choice))
    db.commit()
    db.refresh(db_ability)
    return db_ability


def update_item(db: Session, item: schemas.ItemUpdate):
    db_item = get_item_by_hero_id_and_item_name(db, hero_id=item.hero_id, item_name=item.name)
    if item.new_name:
        db_item.name = item.new_name
    if item.new_matches:
        db_item.matches = item.new_matches
    if item.new_wins:
        db_item.wins = item.new_wins
    if item.new_win_rate:
        db_item.win_rate = item.new_win_rate
    db.commit()
    db.refresh(db_item)
    return db_item


def update_b_vs(db: Session, b_vs: schemas.BestVersusUpdate):
    db_b_vs = get_best_versus_heroes_by_hero_id(db, hero_id=b_vs.hero_id, offset=0, limit=100)
    db_b_vs = [x for x in db_b_vs if x.best_vs_hero_name == b_vs.best_vs_hero_name][0]
    if b_vs.new_best_vs_hero_name:
        db_b_vs.best_vs_hero_name = b_vs.new_best_vs_hero_name
    if b_vs.new_advantage:
        db_b_vs.advantage = b_vs.new_advantage
    if b_vs.new_win_rate:
        db_b_vs.win_rate = b_vs.new_win_rate
    if b_vs.new_matches:
        db_b_vs.matches = b_vs.new_matches
    db.commit()
    db.refresh(db_b_vs)
    return db_b_vs


def update_w_vs(db: Session, w_vs: schemas.WorstVersusUpdate):
    db_w_vs = get_worst_versus_heroes_by_hero_id(db, hero_id=w_vs.hero_id, offset=0, limit=100)
    db_w_vs = [x for x in db_w_vs if x.best_vs_hero_name == w_vs.best_vs_hero_name][0]
    if w_vs.new_worst_vs_hero_name:
        db_w_vs.worst_vs_hero_name = w_vs.new_worst_vs_hero_name
    if w_vs.new_disadvantage:
        db_w_vs.disadvantage = w_vs.new_disadvantage
    if w_vs.new_win_rate:
        db_w_vs.win_rate = w_vs.new_win_rate
    if w_vs.new_matches:
        db_w_vs.matches = w_vs.new_matches
    db.commit()
    db.refresh(db_w_vs)
    return db_w_vs


# del Section
def delete_hero(db: Session, hero_id: int):
    db_hero = get_hero(db, hero_id)
    db.delete(db_hero.safe_lane)
    db.delete(db_hero.off_lane)
    db.delete(db_hero.mid_lane)
    for abil in db_hero.ability_build:
        db.delete(abil)
    for item in db_hero.used_items:
        db.delete(item)
    for item in db_hero.best_versus:
        db.delete(item)
    for item in db_hero.worst_versus:
        db.delete(item)
    db.delete(db_hero)
    db.commit()


def delete_hero_role(db: Session, hero_id: int, role: str):
    db_hero = get_hero(db, hero_id)
    roles = list(filter(lambda x: x.name != role, db_hero.hero_roles))
    db_hero.hero_roles = roles
    db.commit()


def delete_role(db: Session, role: str):
    db.delete(get_role_by_name(db, role))
    db.commit()


def delete_ability(db: Session, ability: str):
    db.delete(get_ability_by_name(db, ability))
    db.commit()


def delete_hero_item(db: Session, hero_id: int, item: str):
    db.delete(get_item_by_hero_id_and_item_name(db, hero_id, item))
    db.commit()


def delete_best_versus_hero(db: Session, hero_id: int, b_vs_hero_name: str):
    db.delete(db.query(models.BestVS)
              .filter(models.BestVS.hero_id == hero_id).filter(
        models.BestVS.best_vs_hero_name == b_vs_hero_name).first())
    db.commit()


def delete_worst_versus_hero(db: Session, hero_id: int, w_vs_hero_name: str):
    db.delete(db.query(models.WorstVS)
              .filter(models.WorstVS.hero_id == hero_id).filter(
        models.WorstVS.worst_vs_hero_name == w_vs_hero_name).first())
    db.commit()
