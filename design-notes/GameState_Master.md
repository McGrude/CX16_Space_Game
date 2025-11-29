# Commander X16 Space RPG — Complete Game State Document

This is the unified master document containing all finalized systems:
- Game World State
- Player Skills
- Crew Model
- Ship Identity
- Equipment System
- Action Integration

---

# 1. Game World State

## 1.1 Core Fields
- `DA%` — Days since game start  
- `SY%` — Current star system  
- `LO%` — Current local location  
- `RS%` — RNG seed  
- `EV%(0..15)` — Global event flags

World time of day, global econ, and political states are deliberately excluded.

---

# 2. Player Skills

Skills (float):
```
SK(0)=Leadership
SK(1)=Tactical
SK(2)=Trading
SK(3)=Engineering
SK(4)=Navigation
SK(5)=Evasion
SK(6)=CyberTechs
```

Each skill feeds the unified formula for gameplay actions.

---

# 3. Crew Model

Crew roles map 1:1 to skills:

| Skill | Role | Short |
|-------|------|-------|
| Leadership | Executive Officer | XO |
| Tactical | Tactical Officer | TacOff |
| Trading | *(none)* | – |
| Engineering | Chief Engineer | CE |
| Navigation | Navigator | Nav |
| Evasion | Evasive Systems Officer | ESO |
| CyberTechs | CyberOps Technician | CyTech |

Crew contributions:
```
CR(skillIndex)
```

---

# 4. Ship Identity (Dynamic State)

Stored in save game:
```
SH%   ' ship type ID
SH$   ' ship name
SR$   ' registration ID
FL    ' current fuel level
```

Not saved (static):
- Fuel max, cargo max, equipment cap  
- Ship class, builder ID  

Loaded from ShipType CSV.

---

# 5. Equipment System

Equipment mapped to skills:

| Skill | Equipment |
|-------|-----------|
| Leadership | none |
| Tactical | beam weapons, torpedo weapons, tactical computer, tactical scanner |
| Trading | none |
| Engineering | reactor, engines, shields, armor |
| Navigation | ore scanner, navigation computer, long-range scanner |
| Evasion | ECM, jammers, stealth plating, heat management |
| CyberTechs | cyberdeck, intrusion suite, decryption modules, ICE |

Equipment modifies gameplay via:
```
SH(skillIndex)
```

---

# 6. Action Integration

Every meaningful action picks a skill index `SI`.

```
CREWM = .75 + CR(SI)/200
SHIPM = .75 + SH(SI)/200

EFF = SK(SI) * CREWM * SHIPM
IF EFF > 150 THEN EFF = 150

CH = 20 + (EFF * .5)
IF CH > 95 THEN CH = 95
```

Used for:
- Combat  
- Navigation  
- Trading  
- Evasion  
- Engineering checks  
- Cyber intrusion  
- Leadership checks  

---

# 7. CSV Formats (Static Databases)

## 7.1 Ship Types CSV
```
TYPE_ID, NAME, CLASS, FUEL_MAX, CARGO_MAX, EQP_CAP, BUILDER_ID
```

## 7.2 Equipment CSV (future)
- EQUIP_ID
- NAME
- SKILL_INDEX
- SH_VALUE
- CLASS_REQ
- SLOT_TYPE

---

# 8. Save Game Contents

**Saved:**
- Player skills
- Crew contributions
- Installed equipment IDs
- Ship identity (SH%, SH$, SR$, FL)
- Mission state
- Cargo contents
- EV% flags

**Not saved:**
- Static databases (ship types, equipment definitions)
- Derived values

---

This master document reflects all finalized systems so far.
