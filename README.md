# API-and-parsers

Парсер основных данных героя с сайта [DOTABUFF](https://ru.dotabuff.com/heroes/)

## Список доступных полей
- hero_name
- hero_roles
- popularity
- win_rate
- safe_lane
- off_lane
- mid_lane
- ability_build
- used_items
- best_versus
- worst_versus

## Пример ответа

```json
{
  "hero_name": "Riki",
  "hero_roles": [
    "ближнего боя",
    "Carry",
    "Disabler",
    "Escape"
  ],
  "popularity": "60th",
  "win_rate": "52.47%",
  "safe_lane": {
    "presence": "40.62%",
    "win_rate": "52.88%",
    "kda_ratio": 3.94,
    "gpm": 479,
    "xpm": 671
  },
  "off_lane": {
    "presence": "36.72%",
    "win_rate": "54.08%",
    "kda_ratio": 3.34,
    "gpm": 382,
    "xpm": 564
  },
  "mid_lane": {
    "presence": "14.60%",
    "win_rate": "55.67%",
    "kda_ratio": 3.62,
    "gpm": 431,
    "xpm": 604
  },
  "ability_build": [
    {
      "name": "Smoke Screen",
      "levels_choice": [
        4,
        13,
        14,
        16
      ]
    },
    {
      "name": "Blink Strike",
      "levels_choice": [
        1,
        3,
        5,
        7
      ]
    },
    {
      "name": "Tricks of the Trade",
      "levels_choice": [
        2,
        8,
        9,
        10
      ]
    },
    {
      "name": "Cloak and Dagger",
      "levels_choice": [
        6,
        12,
        18
      ]
    },
    {
      "name": "Talent: +50 Smoke Screen Radius",
      "levels_choice": [
        11
      ]
    },
    {
      "name": "Talent: +40% Tricks of the Trade Agility Increase",
      "levels_choice": [
        15
      ]
    }
  ],
  "used_items": [
    {
      "name": "Power Treads",
      "matches": 187000,
      "wins": 99034,
      "win_rate": "52.96%"
    },
    {
      "name": "Diffusal Blade",
      "matches": 172646,
      "wins": 89439,
      "win_rate": "51.80%"
    },
    {
      "name": "Wraith Band",
      "matches": 104346,
      "wins": 52568,
      "win_rate": "50.38%"
    },
    {
      "name": "Manta Style",
      "matches": 91985,
      "wins": 55723,
      "win_rate": "60.58%"
    },
    {
      "name": "Aghanim's Shard",
      "matches": 82941,
      "wins": 49379,
      "win_rate": "59.54%"
    },
    {
      "name": "Aghanim's Scepter",
      "matches": 78570,
      "wins": 48480,
      "win_rate": "61.70%"
    },
    {
      "name": "Daedalus",
      "matches": 64592,
      "wins": 41304,
      "win_rate": "63.95%"
    },
    {
      "name": "Magic Wand",
      "matches": 56779,
      "wins": 28578,
      "win_rate": "50.33%"
    },
    {
      "name": "Skull Basher",
      "matches": 53156,
      "wins": 29298,
      "win_rate": "55.12%"
    },
    {
      "name": "Quelling Blade",
      "matches": 36103,
      "wins": 16432,
      "win_rate": "45.51%"
    },
    {
      "name": "Abyssal Blade",
      "matches": 28141,
      "wins": 18372,
      "win_rate": "65.29%"
    },
    {
      "name": "Disperser",
      "matches": 27975,
      "wins": 18396,
      "win_rate": "65.76%"
    }
  ],
  "best_versus": [
    {
      "name": "Brewmaster",
      "advantage": "3.62%",
      "win_rate": "57.62%",
      "matches": 1168
    },
    {
      "name": "Storm Spirit",
      "advantage": "3.32%",
      "win_rate": "57.14%",
      "matches": 9988
    },
    {
      "name": "Puck",
      "advantage": "2.97%",
      "win_rate": "57.92%",
      "matches": 4812
    },
    {
      "name": "Anti-Mage",
      "advantage": "2.66%",
      "win_rate": "55.45%",
      "matches": 15940
    },
    {
      "name": "Slark",
      "advantage": "2.63%",
      "win_rate": "53.95%",
      "matches": 21211
    },
    {
      "name": "Weaver",
      "advantage": "2.54%",
      "win_rate": "55.81%",
      "matches": 7158
    },
    {
      "name": "Morphling",
      "advantage": "2.21%",
      "win_rate": "58.45%",
      "matches": 11657
    },
    {
      "name": "Enigma",
      "advantage": "2.06%",
      "win_rate": "56.12%",
      "matches": 5148
    },
    {
      "name": "Invoker",
      "advantage": "2.05%",
      "win_rate": "55.81%",
      "matches": 13391
    },
    {
      "name": "Queen of Pain",
      "advantage": "2.02%",
      "win_rate": "55.57%",
      "matches": 10394
    }
  ],
  "worst_versus": [
    {
      "name": "Bristleback",
      "disadvantage": "4.62%",
      "win_rate": "47.55%",
      "matches": 10640
    },
    {
      "name": "Underlord",
      "disadvantage": "4.00%",
      "win_rate": "46.21%",
      "matches": 4412
    },
    {
      "name": "Naga Siren",
      "disadvantage": "3.04%",
      "win_rate": "44.82%",
      "matches": 4884
    },
    {
      "name": "Leshrac",
      "disadvantage": "3.04%",
      "win_rate": "51.66%",
      "matches": 2284
    },
    {
      "name": "Phantom Assassin",
      "disadvantage": "2.72%",
      "win_rate": "52.83%",
      "matches": 17895
    },
    {
      "name": "Zeus",
      "disadvantage": "2.64%",
      "win_rate": "50.16%",
      "matches": 13149
    },
    {
      "name": "Bloodseeker",
      "disadvantage": "2.64%",
      "win_rate": "48.65%",
      "matches": 13269
    },
    {
      "name": "Drow Ranger",
      "disadvantage": "2.52%",
      "win_rate": "49.12%",
      "matches": 16029
    },
    {
      "name": "Luna",
      "disadvantage": "2.50%",
      "win_rate": "52.34%",
      "matches": 4622
    },
    {
      "name": "Spectre",
      "disadvantage": "2.47%",
      "win_rate": "45.80%",
      "matches": 8489
    }
  ]
}
```
