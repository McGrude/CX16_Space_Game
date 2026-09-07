# Commander X16 Space RPG — Crew Model Specification

This document defines the **finalized crew model** for the game, aligned with the finalized skill system and equipment interaction model.  
It reflects a **lean, intentional crew structure** where every role directly contributes to exactly one defined player skill and no role is redundant.

---

# 1. Overview

Crew members serve as **skill amplifiers** for the player, each tied to one of the seven player skills:

- Leadership (SK 0)
- Tactical (SK 1)
- Trading (SK 2)
- Engineering (SK 3)
- Navigation (SK 4)
- Evasion (SK 5)
- CyberTechs (SK 6)

Each crew role contributes to exactly one skill category through the crew skill array:

```
CR(skillIndex)
```

There are **seven meaningful crew roles**, matching the seven skills.  
No additional roles (Quartermaster, Medical Officer) are included because they do not contribute to any active skill or mechanic in the current version of the game.

---

# 2. Crew Roles (Finalized)

## 2.1 Captain (Player)
- Primary source of the **Leadership** skill.
- Determines morale baseline.
- Affects crisis reactions and overall command effectiveness.
- Is not represented in crew arrays (the captain’s skill is SK(0)).

## 2.2 Executive Officer (XO)
- Secondary Leadership contributor.
- Helps stabilize crew morale.
- Assists in crisis decision-making.
- Contributes to:
  ```
  CR(0)  ' Leadership
  ```

## 2.3 Tactical Officer
- Contributes to **Tactical** skill.
- Improves accuracy of beam and torpedo weapons.
- Helps determine combat initiative.
- Contributes to:
  ```
  CR(1)  ' Tactical
  ```

## 2.4 Chief Engineer
- Contributes to **Engineering** skill.
- Improves repair speed and reduces repair costs.
- Helps determine eligibility for high-tech equipment upgrades.
- Contributes to:
  ```
  CR(3)  ' Engineering
  ```

## 2.5 Navigator
- Contributes to **Navigation** skill.
- Improves jump fuel efficiency.
- Reduces hazard encounter chances.
- Increases jump accuracy.
- Contributes to:
  ```
  CR(4)  ' Navigation
  ```

## 2.6 Evasive Systems Officer (ESO)
- Contributes to **Evasion** skill.
- Manages EM emissions, stealth plating, ECM, heat control modules.
- Reduces scan chance and improves disengagement chances.
- Contributes to:
  ```
  CR(5)  ' Evasion
  ```

## 2.7 CyberOps Technician (CyTech)
- Contributes to **CyberTech** skill.
- Operates cyberdeck, intrusion software, defensive ICE, and SIGINT hardware.
- Performs hacking, counter-hacking, and communications interception.
- Contributes to:
  ```
  CR(6)  ' CyberTechs
  ```

---

# 3. Crew Storage Model (8-bit Friendly)

## 3.1 Crew Skill Contributions
Each crew role contributes a **0 to 100** rating to one specific skill category.

```
DIM CR(6)
```

Mapping:
- `CR(0)` — Leadership bonus (XO)
- `CR(1)` — Tactical bonus (Tactical Officer)
- `CR(2)` — Trading (unused; remains 0)
- `CR(3)` — Engineering (Chief Engineer)
- `CR(4)` — Navigation (Navigator)
- `CR(5)` — Evasion (ESO)
- `CR(6)` — CyberTech (CyTech)

**Note:**  
Trading has **no crew role**, so `CR(2)` remains unused (set to 0).

## 3.2 Crew Names and Metadata
Optionally store names or simple identifiers:

```
DIM CREW$(6)   ' Crew member names, if needed
DIM CROLE$(6)  ' Crew role titles (optional, static)
```

Example:
```
CROLE$(0)="XO"
CROLE$(1)="Tactical Officer"
CROLE$(2)=""
CROLE$(3)="Chief Engineer"
CROLE$(4)="Navigator"
CROLE$(5)="ESO"
CROLE$(6)="CyTech"
```

## 3.3 Crew Morale / Loyalty (Optional)
If morale is tracked:
```
DIM CMO(6)    ' Morale or loyalty for each role
```

Morale effects are applied through:
- Leadership (SK(0))
- XO contributions
- Events and crises

---

# 4. Effective Skill Formula Integration

Crew contributions fit into the core skill calculation pipeline:

```
CREWM = .75 + CR(SI)/200
EFF = SK(SI) * CREWM * SHIPM
```

Where:
- `SI` = skill index (0..6)
- `CR(SI)` = crew contribution for that role
- `SHIPM` = equipment modifier for that skill

This ensures **crew always matters**, but never overshadows the player's skill.

---

# 5. Roles Not Included

The following roles were explicitly removed because they do not meaningfully interact with the skill system or game mechanics:

- Quartermaster  
- Medical Officer  
- Supply Officer  
- Science Officer  
- Passenger roles  
- Civilians or non-officers  

These may be reintroduced later only if associated gameplay systems are added.

---

# 6. Summary Table

| Skill Index | Skill Name   | Crew Role                | Equipment Tied | Notes |
|-------------|--------------|--------------------------|----------------|------|
| 0           | Leadership   | Executive Officer (XO)   | None           | Captain provides SK(0) |
| 1           | Tactical     | Tactical Officer         | Tactical gear  | Weapons & combat |
| 2           | Trading      | *(none)*                 | None           | Player-only skill |
| 3           | Engineering  | Chief Engineer           | Reactor/Eng/Armor/Shields | Repairs & tech |
| 4           | Navigation   | Navigator                | Nav gear       | Jumps, hazards |
| 5           | Evasion      | Evasive Systems Officer  | ECM/Jammers/Stealth | Scans & stealth |
| 6           | CyberTechs   | CyberOps Technician      | Cyberdeck/ICE  | Hacking/defense |

---

This specification represents the **finalized and fully cohesive crew system** for your Commander X16 space RPG.  
