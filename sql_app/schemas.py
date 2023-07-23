from pydantic import BaseModel


class HeroBase(BaseModel):
    id: int
    name: str
    popularity: str
    win_rate: float

    class Config:
        from_attributes = True


class HeroCreate(BaseModel):
    name: str
    popularity: str
    win_rate: float

class HeroUpdate(BaseModel):
    name:str
    new_popularity: str | None = None
    new_name: str | None = None
    new_win_rate: float | None = None

class RoleBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RoleCreate(BaseModel):
    name: str
    hero_name:str

class RoleAdd(BaseModel):
    role_name:str
    hero_name:str

class RoleUpdate(BaseModel):
    name: str
    new_name:str


class LineBase(BaseModel):
    presence: float | None = None
    win_rate: float | None = None
    kda_ratio: float | None = None
    gpm: int | None = None
    xpm: int | None = None


class LineCreate(LineBase):
    hero_name:str



class Line(LineBase):
    id: int
    hero_id: int


class AbilityBase(BaseModel):
    name: str
    levels_choice: str


class AbilityCreate(BaseModel):
    name: str
    levels_choice: list[int]
    hero_name:str

class AbilityUpdate(BaseModel):
    name: str
    new_levels_choice: list[int] | None = None
    new_name: str | None = None

class Ability(AbilityBase):
    id: int
    hero_id: int


class ItemBase(BaseModel):
    name: str
    matches: int
    wins: int
    win_rate: float


class ItemCreate(ItemBase):
    hero_name:str


class ItemUpdate(BaseModel):
    hero_id: int
    name: str
    new_name: str | None = None
    new_matches: int | None = None
    new_wins: int | None = None
    new_win_rate: float | None = None

class Item(ItemBase):
    id: int
    hero_id: int


class VersusBase(BaseModel):
    win_rate: float
    matches: int


class BestVSCreate(VersusBase):
    best_vs_hero_name: str
    advantage: float
    hero_name: str


class BestVersus(VersusBase):
    id:int
    best_vs_hero_name: str
    advantage: float

class BestVersusUpdate(BaseModel):
    hero_id: int
    best_vs_hero_name: str
    new_best_vs_hero_name: str | None = None
    new_advantage: float | None = None
    new_win_rate: float | None = None
    new_matches: int | None = None


class WorstVSCreate(VersusBase):
    worst_vs_hero_name: str
    disadvantage: float
    hero_name: str


class WorstVersusUpdate(BaseModel):
    hero_id: int
    worst_vs_hero_name: str
    new_worst_vs_hero_name: str | None = None
    new_disadvantage: float | None = None
    new_win_rate: float | None = None
    new_matches: int | None = None

class WorstVersus(VersusBase):
    id:int
    worst_vs_hero_name: str
    disadvantage: float


class Hero(HeroBase):
    hero_roles: list[RoleBase] = []
    safe_lane: Line | None
    off_lane: Line | None
    mid_lane: Line | None
    ability_build: list[Ability] = []
    used_items: list[Item] = []
    best_versus: list[BestVersus] = []
    worst_versus: list[WorstVersus] = []


class Role(RoleBase):
    heroes: list[HeroBase]
