from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .background_tasks import run_continuously
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {"name": "Hero", "description": r"Methods with the hero. Also here is adding an **existing role** to the hero."},
    {"name": "Role","description": r"Methods with roles. Also here **removing an existing role** from the hero."},
    {"name": "Lines","description": r"Methods with lines. Each line has its **own** methods."},
    {"name": "Ability"},
    {"name": "Item"},
    {"name": "Best VS Hero section","description": r"Methods with heroes that best counter the requested hero."},
    {"name": "Worst VS Hero section","description": r"Methods with heroes that worst counter the requested hero."},
    {"name": "Get Methods"},
    {"name": "Post Methods"},
    {"name": "Delete Methods"},
    {"name": "Put Methods"},
]
app = FastAPI(openapi_tags=tags_metadata,title="BuffAPI")

bg = run_continuously()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/hero/create", response_model=schemas.Hero, tags=["Post Methods", "Hero"])
def create_hero(hero: schemas.HeroCreate, db: Session = Depends(get_db)):
    db_hero = crud.get_hero_by_name(db, hero.name)
    if db_hero:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Hero already registered")
    return crud.create_hero(db=db, hero=hero)


@app.get("/heroes", response_model=list[schemas.Hero], tags=["Get Methods", "Hero"])
def read_heroes(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    heroes = crud.get_heroes(db, offset=offset, limit=limit)
    if not heroes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Heroes not found")
    return heroes


@app.get("/hero/{hero_id}", response_model=schemas.Hero, tags=["Get Methods", "Hero"])
def read_hero(hero_id: int, db: Session = Depends(get_db)):
    hero = crud.get_hero(db, hero_id)
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    return hero


@app.get("/hero/name/{hero_name}", response_model=schemas.Hero, tags=["Get Methods", "Hero"])
def read_hero_by_name(hero_name: str, db: Session = Depends(get_db)):
    hero = crud.get_hero_by_name(db, hero_name)
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    return hero


@app.put("/hero/update", response_model=schemas.Hero, tags=["Put Methods", "Hero"])
def update_hero(hero: schemas.HeroUpdate, db: Session = Depends(get_db)):
    db_hero = crud.get_hero_by_name(db, hero.name)
    if db_hero:
        return crud.update_hero(db=db, new_hero=hero)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")


@app.put("/hero/add/role", response_model=schemas.Hero, tags=["Put Methods", "Hero"])
def add_role_to_hero(data: schemas.RoleAdd, db: Session = Depends(get_db)):
    db_hero = crud.get_hero_by_name(db, data.hero_name)
    db_role = crud.get_role_by_name(db, data.role_name)
    if db_hero:
        if db_role:
            if list(filter(lambda x: x.name == data.role_name, db_hero.hero_roles)):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role already installed")
            return crud.add_role_to_hero(db=db, data=data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")


@app.delete("/hero/delete/{hero_id}", tags=["Delete Methods", "Hero"])
def delete_hero(hero_id: int, db: Session = Depends(get_db)):
    if crud.get_hero(db, hero_id):
        crud.delete_hero(db, hero_id)
        return {"status": "Ok"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")


@app.post("/role/create", response_model=schemas.Role, tags=["Post Methods", "Role"])
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    db_role = crud.get_role_by_name(db, role.name)
    db_hero = crud.get_hero_by_name(db, role.hero_name)
    if db_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role already registered")
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    return crud.create_role(db=db, role=role)


@app.get("/roles", response_model=list[schemas.Role], tags=["Get Methods", "Role"])
def read_roles(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    roles = crud.get_roles(db, offset=offset, limit=limit)
    if not roles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roles not found")
    return roles


@app.put("/role/update", response_model=schemas.Role, tags=["Put Methods", "Role"])
def update_role(role: schemas.RoleUpdate, db: Session = Depends(get_db)):
    db_role = crud.get_role_by_name(db, role.name)
    if db_role:
        if crud.get_role_by_name(db, role.new_name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New role must be unique")
        return crud.update_role(db=db, new_role=role)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")


@app.delete("/role/delete/{role}", tags=["Delete Methods", "Role"])
def delete_role(role: str, db: Session = Depends(get_db)):
    if crud.get_role_by_name(db, role):
        crud.delete_role(db, role)
        return {"status": "Ok"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")


@app.delete("/role/delete/{role}/{hero_id}", tags=["Delete Methods", "Role"])
def delete_hero_role(role: str, hero_id: int, db: Session = Depends(get_db)):
    if crud.get_role_by_name(db, role):
        if crud.get_hero(db, hero_id):
            crud.delete_hero_role(db, hero_id, role)
            return {"status": "Ok"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")


@app.get("/safe_line/{line_id}", response_model=schemas.Line, tags=["Get Methods", "Lines"])
def read_safe_line_by_line_id(line_id: int, db: Session = Depends(get_db)):
    s_line = crud.get_s_line(db, line_id)
    if not s_line:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Line not found")
    return s_line


@app.get("/safe_line/{hero_id}", response_model=schemas.Line, tags=["Get Methods", "Lines"])
def read_safe_line_by_hero_id(hero_id: int, db: Session = Depends(get_db)):
    s_line = crud.get_s_line_by_hero_id(db, hero_id)
    if not s_line:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Line not found")
    return s_line


@app.get("/safe_lines", response_model=list[schemas.Line], tags=["Get Methods", "Lines"])
def read_safe_lines(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    s_lines = crud.get_s_lines(db, offset=offset, limit=limit)
    if not s_lines:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lines not found")
    return s_lines


@app.post("/safe_line/create", response_model=schemas.Line, tags=["Post Methods", "Lines"])
def create_safe_line_data(line: schemas.LineCreate, db: Session = Depends(get_db)):
    db_hero = crud.get_hero_by_name(db, line.hero_name)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    db_safe_line = crud.get_s_line_by_hero_id(db, db_hero.id)
    if db_safe_line:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Safe line already registered")
    return crud.create_s_line(db=db, s_line=line)


@app.put("/safe_line/update", response_model=schemas.Line, tags=["Put Methods", "Lines"])
def update_safe_line_data(line: schemas.LineCreate, db: Session = Depends(get_db)):
    db_hero = crud.get_hero_by_name(db, line.hero_name)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    db_safe_line = crud.get_s_line_by_hero_id(db, db_hero.id)
    if db_safe_line:
        return crud.update_safe_line(db=db, line=line)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Safe line not found")


@app.get("/off_line/{line_id}", response_model=schemas.Line, tags=["Get Methods", "Lines"])
def read_off_line_by_line_id(line_id: int, db: Session = Depends(get_db)):
    o_line = crud.get_o_line(db, line_id)
    if not o_line:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Line not found")
    return o_line


@app.get("/off_line/{hero_id}", response_model=schemas.Line, tags=["Get Methods", "Lines"])
def read_off_line_by_hero_id(hero_id: int, db: Session = Depends(get_db)):
    o_line = crud.get_o_line_by_hero_id(db, hero_id)
    if not o_line:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Line not found")
    return o_line


@app.get("/off_lines", response_model=list[schemas.Line], tags=["Get Methods", "Lines"])
def read_off_lines(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    o_lines = crud.get_o_lines(db, offset=offset, limit=limit)
    if not o_lines:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=":ines not found")
    return o_lines


@app.post("/off_line/create", response_model=schemas.Line, tags=["Post Methods", "Lines"])
def create_off_line_data(line: schemas.LineCreate, db: Session = Depends(get_db)):
    db_hero = crud.get_hero_by_name(db, line.hero_name)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    db_off_line = crud.get_o_line_by_hero_id(db, db_hero.id)
    if db_off_line:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Off line already registered")
    return crud.create_o_line(db=db, o_line=line)


@app.put("/off_line/update", response_model=schemas.Line, tags=["Put Methods", "Lines"])
def update_off_line_data(line: schemas.LineCreate, db: Session = Depends(get_db)):
    db_hero = crud.get_hero_by_name(db, line.hero_name)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    db_safe_line = crud.get_s_line_by_hero_id(db, db_hero.id)
    if db_safe_line:
        return crud.update_off_line(db=db, line=line)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Off line not found")


@app.get("/mid_line/{line_id}", response_model=schemas.Line, tags=["Get Methods", "Lines"])
def read_mid_line_by_line_id(line_id: int, db: Session = Depends(get_db)):
    m_line = crud.get_m_line(db, line_id)
    if not m_line:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Line not found")
    return m_line


@app.get("/mid_line/{hero_id}", response_model=schemas.Line, tags=["Get Methods", "Lines"])
def read_mid_line_by_hero_id(hero_id: int, db: Session = Depends(get_db)):
    m_line = crud.get_m_line_by_hero_id(db, hero_id)
    if not m_line:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Line not found")
    return m_line


@app.get("/mid_lines", response_model=list[schemas.Line], tags=["Get Methods", "Lines"])
def read_mid_lines(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    m_lines = crud.get_m_lines(db, offset=offset, limit=limit)
    if not m_lines:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lines not found")
    return m_lines


@app.post("/mid_line/create", response_model=schemas.Line, tags=["Post Methods", "Lines"])
def create_mid_line_data(line: schemas.LineCreate, db: Session = Depends(get_db)):
    db_hero = crud.get_hero_by_name(db, line.hero_name)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    db_mid_line = crud.get_m_line_by_hero_id(db, db_hero.id)
    if db_mid_line:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mid line already registered")
    return crud.create_m_line(db=db, m_line=line)


@app.put("/mid_line/update", response_model=schemas.Line, tags=["Put Methods", "Lines"])
def update_mid_line_data(line: schemas.LineCreate, db: Session = Depends(get_db)):
    db_hero = crud.get_hero_by_name(db, line.hero_name)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    db_safe_line = crud.get_m_line_by_hero_id(db, db_hero.id)
    if db_safe_line:
        return crud.update_mid_line(db=db, line=line)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mid line not found")


@app.get("/ability/name/{ability_name}", response_model=schemas.Ability, tags=["Get Methods", "Ability"])
def read_ability_by_name(ability_name: str, db: Session = Depends(get_db)):
    ability = crud.get_ability_by_name(db, ability_name)
    if not ability:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ability not found")
    return ability


@app.get("/ability/{ability_id}", response_model=schemas.Ability, tags=["Get Methods", "Ability"])
def read_ability(ability_id: int, db: Session = Depends(get_db)):
    ability = crud.get_ability(db, ability_id)
    if not ability:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ability not found")
    return ability


@app.get("/abilities/{hero_id}", response_model=list[schemas.Ability], tags=["Get Methods", "Ability"])
def read_ability_by_hero_id(hero_id: int, db: Session = Depends(get_db)):
    abilities = crud.get_abilities_by_hero_id(db, hero_id)
    if not abilities:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Abilities not found")
    return abilities


@app.get("/abilities", response_model=list[schemas.Ability], tags=["Get Methods", "Ability"])
def read_abilities(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    abilities = crud.get_abilities(db, offset=offset, limit=limit)
    if not abilities:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Abilities not found")
    return abilities


@app.post("/ability/create", response_model=schemas.Ability, tags=["Post Methods", "Ability"])
def create_ability(ability: schemas.AbilityCreate, db: Session = Depends(get_db)):
    db_hero = crud.get_hero_by_name(db, ability.hero_name)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    db_ability = crud.get_ability_by_name(db, ability.name)
    if db_ability:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ability already registered")
    return crud.create_ability(db=db, ability=ability)


@app.put("/ability/update", response_model=schemas.Ability, tags=["Put Methods", "Ability"])
def update_ability_data(ability: schemas.AbilityUpdate, db: Session = Depends(get_db)):
    db_ability = crud.get_ability_by_name(db, ability.name)
    if crud.get_ability_by_name(db, ability.new_name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ability new_name must be unique")
    if db_ability:
        return crud.update_ability(db=db, ability=ability)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ability not found")


@app.delete("/ability/delete/{ability}", tags=["Delete Methods", "Ability"])
def delete_ability(ability: str, db: Session = Depends(get_db)):
    if crud.get_ability_by_name(db, ability):
        crud.delete_ability(db, ability)
        return {"status": "Ok"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ability not found")


@app.get("/items", response_model=list[schemas.Item], tags=["Get Methods", "Item"])
def read_items(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = crud.get_items(db, offset=offset, limit=limit)
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Items not found")
    return items


@app.get("/items/{hero_id}", response_model=list[schemas.Item], tags=["Get Methods", "Item"])
def read_items_by_hero_id(hero_id: int, offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if not crud.get_hero(db, hero_id=hero_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    items = crud.get_items_by_hero_id(db, hero_id=hero_id, offset=offset, limit=limit)
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Items not found")
    return items


@app.get("/item/{item_id}", response_model=schemas.Item, tags=["Get Methods", "Item"])
def read_items(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@app.get("/item", response_model=schemas.Item, tags=["Get Methods", "Item"])
def read_item_by_hero_id_and_item_name(hero_id: int, item_name: str, db: Session = Depends(get_db)):
    if not crud.get_hero(db, hero_id=hero_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    item = crud.get_item_by_hero_id_and_item_name(db, hero_id=hero_id, item_name=item_name)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@app.post("/item/create", response_model=schemas.Item, tags=["Post Methods", "Item"])
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_hero = crud.get_hero_by_name(db, item.hero_name)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    db_item = list(filter(lambda x: x.name == item.name, crud.get_items_by_hero_id(db, db_hero.id)))
    if db_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item already registered")
    return crud.create_item(db=db, item=item)


@app.put("/item/update", response_model=schemas.Item, tags=["Put Methods", "Item"])
def update_item_data(item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_hero = crud.get_hero(db, item.hero_id)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    if crud.get_item_by_hero_id_and_item_name(db, hero_id=item.hero_id, item_name=item.new_name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item new_name must be unique")
    db_item = crud.get_item_by_hero_id_and_item_name(db, hero_id=item.hero_id, item_name=item.name)
    if db_item:
        return crud.update_item(db=db, item=item)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@app.delete("/item/delete/{item_name}/{hero_id}", tags=["Delete Methods", "Item"])
def delete_hero_item(item_name: str, hero_id: int, db: Session = Depends(get_db)):
    if crud.get_item_by_hero_id_and_item_name(db, hero_id, item_name):
        crud.delete_hero_item(db, hero_id, item_name)
        return {"status": "Ok"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item or hero not found")


@app.get("/best_versus", response_model=list[schemas.BestVersus], tags=["Get Methods", "Best VS Hero section"])
def read_best_versus_heroes(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_b_vs = crud.get_best_versus_heroes(db, offset=offset, limit=limit)
    if not db_b_vs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Best vs heroes not found")
    return db_b_vs


@app.get("/best_versus", response_model=list[schemas.BestVersus], tags=["Get Methods", "Best VS Hero section"])
def read_best_versus_heroes_by_hero_id(hero_id: int, offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if not crud.get_hero(db, hero_id=hero_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    db_b_vs = crud.get_best_versus_heroes_by_hero_id(db, hero_id=hero_id, offset=offset, limit=limit)
    if not db_b_vs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Best vs heroes not found")
    return db_b_vs


@app.get("/best_versus/{b_vs_id}", response_model=schemas.BestVersus, tags=["Get Methods", "Best VS Hero section"])
def read_best_versus_hero(b_vs_id: int, db: Session = Depends(get_db)):
    db_b_vs = crud.get_best_versus_hero(db, id=b_vs_id)
    if not db_b_vs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Best vs hero not found")
    return db_b_vs


@app.get("/{hero_name}/best_versus", response_model=list[schemas.BestVersus],
         tags=["Get Methods", "Best VS Hero section"])
def read_best_versus_heroes_by_hero_name(hero_name: str, offset: int = 0, limit: int = 10,
                                         db: Session = Depends(get_db)):
    db_hero = crud.get_hero_by_name(db, hero_name=hero_name)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    db_b_vs = crud.get_best_versus_heroes_by_hero_id(db, hero_id=db_hero.id, offset=offset, limit=limit)
    if not db_b_vs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Best vs heroes not found")
    return db_b_vs


@app.post("/best_versus/create", response_model=schemas.BestVersus, tags=["Post Methods", "Best VS Hero section"])
def create_best_versus_hero(b_vs: schemas.BestVSCreate, db: Session = Depends(get_db)):
    db_hero = crud.get_hero_by_name(db, b_vs.hero_name)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    db_b_vs = list(filter(lambda x: x.best_vs_hero_name == b_vs.best_vs_hero_name,
                          crud.get_best_versus_heroes_by_hero_id(db, db_hero.id)))
    if db_b_vs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Best vs Hero already registered")
    return crud.create_best_vs_hero(db=db, b_vs_hero=b_vs)


@app.put("/best_versus/update", response_model=schemas.BestVersus, tags=["Put Methods", "Best VS Hero section"])
def update_best_versus_data(b_vs: schemas.BestVersusUpdate, db: Session = Depends(get_db)):
    db_hero = crud.get_hero(db, b_vs.hero_id)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    db_b_vs = crud.get_best_versus_heroes_by_hero_id(db, hero_id=b_vs.hero_id, offset=0, limit=100)
    if list(filter(lambda x: x.best_vs_hero_name == b_vs.new_best_vs_hero_name, db_b_vs)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" New best vs Hero must be unique")
    db_b_vs = [x for x in db_b_vs if x.best_vs_hero_name == b_vs.best_vs_hero_name]
    if db_b_vs:
        return crud.update_b_vs(db=db, b_vs=b_vs)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Best vs Hero not found")


@app.delete("/best_versus/delete/{b_vs_hero_name}/{hero_id}", tags=["Delete Methods", "Best VS Hero section"])
def delete_best_versus(b_vs_hero_name: str, hero_id: int, db: Session = Depends(get_db)):
    if crud.get_hero(db, hero_id):
        if list(filter(lambda x: x.best_vs_hero_name == b_vs_hero_name,
                       crud.get_best_versus_heroes_by_hero_id(db, hero_id, limit=100))):
            crud.delete_best_versus_hero(db, hero_id, b_vs_hero_name)
            return {"status": "Ok"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Best vs hero not found")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")


@app.get("/worst_versus", response_model=list[schemas.WorstVersus], tags=["Get Methods", "Worst VS Hero section"])
def read_worst_versus_heroes(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_w_vs = crud.get_worst_versus_heroes(db, offset=offset, limit=limit)
    if not db_w_vs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worst vs heroes not found")
    return db_w_vs


@app.get("/worst_versus", response_model=list[schemas.WorstVersus], tags=["Get Methods", "Worst VS Hero section"])
def read_worst_versus_heroes_by_hero_id(hero_id: int, offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if not crud.get_hero(db, hero_id=hero_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    db_w_vs = crud.get_worst_versus_heroes_by_hero_id(db, hero_id=hero_id, offset=offset, limit=limit)
    if not db_w_vs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worst vs heroes not found")
    return db_w_vs


@app.get("/worst_versus/{b_vs_id}", response_model=schemas.WorstVersus, tags=["Get Methods", "Worst VS Hero section"])
def read_worst_versus_hero(w_vs_id: int, db: Session = Depends(get_db)):
    db_w_vs = crud.get_worst_versus_hero(db, id=w_vs_id)
    if not db_w_vs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Best vs hero not found")
    return db_w_vs


@app.get("/{hero_name}/worst_versus", response_model=list[schemas.WorstVersus],
         tags=["Get Methods", "Worst VS Hero section"])
def read_worst_versus_heroes_by_hero_name(hero_name: str, offset: int = 0, limit: int = 10,
                                          db: Session = Depends(get_db)):
    db_hero = crud.get_hero_by_name(db, hero_name=hero_name)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    db_w_vs = crud.get_worst_versus_heroes_by_hero_id(db, hero_id=db_hero.id, offset=offset, limit=limit)
    if not db_w_vs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Best vs heroes not found")
    return db_w_vs


@app.post("/worst_versus/create", response_model=schemas.WorstVersus, tags=["Post Methods", "Worst VS Hero section"])
def create_worst_versus_hero(w_vs: schemas.WorstVSCreate, db: Session = Depends(get_db)):
    db_hero = crud.get_hero_by_name(db, w_vs.hero_name)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    db_w_vs = list(filter(lambda x: x.worst_vs_hero_name == w_vs.worst_vs_hero_name,
                          crud.get_worst_versus_heroes_by_hero_id(db, db_hero.id)))
    if db_w_vs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Worst vs Hero already registered")
    return crud.create_worst_vs_hero(db=db, w_vs_hero=w_vs)


@app.put("/worst_versus/update", response_model=schemas.WorstVersus, tags=["Put Methods", "Worst VS Hero section"])
def update_worst_versus_data(w_vs: schemas.WorstVersusUpdate, db: Session = Depends(get_db)):
    db_hero = crud.get_hero(db, w_vs.hero_id)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    db_w_vs = crud.get_worst_versus_heroes_by_hero_id(db, hero_id=w_vs.hero_id, offset=0, limit=100)
    if list(filter(lambda x: x.worst_vs_hero_name == w_vs.new_worst_vs_hero_name, db_w_vs)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" New worst vs Hero must be unique")
    db_w_vs = [x for x in db_w_vs if x.worst_vs_hero_name == w_vs.worst_vs_hero_name]
    if db_w_vs:
        return crud.update_w_vs(db=db, w_vs=w_vs)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worst vs Hero not found")


@app.delete("/worst_versus/delete/{w_vs_hero_name}/{hero_id}", tags=["Delete Methods", "Worst VS Hero section"])
def delete_worst_versus(w_vs_hero_name: str, hero_id: int, db: Session = Depends(get_db)):
    if crud.get_hero(db, hero_id):
        if list(filter(lambda x: x.worst_vs_hero_name == w_vs_hero_name,
                       crud.get_worst_versus_heroes_by_hero_id(db, hero_id, limit=100))):
            crud.delete_worst_versus_hero(db, hero_id, w_vs_hero_name)
            return {"status": "Ok"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worst vs hero not found")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
