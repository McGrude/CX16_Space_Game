# Commander X16 Space RPG — Canonical Game State Model (Updated)

This document captures **all decisions made so far**, consolidating the initial 12‑category state model with updated, finalized choices for the **Game World State** and **Player Skill System**.

It is written as a reference for:
- continuing design,
- implementation in Commander X16 BASIC,
- save/load serialization,
- future expansion.

---

# 1. Game World State (Finalized)

These define what the *universe itself* keeps track of.  
We have intentionally trimmed unnecessary fields and moved economy/politics to later categories.

## **Final Fields**
- **DA%** — *Elapsed days since game start*  
- **SY%** — *Current star system ID*  
- **LO%** — *Current local location ID within that system*  
- **RS%** — *RNG seed/state for deterministic behavior*  
- **EV%(0..15)** — *Global event flags (16 reserved), meaning defined later*

## **Removed / Moved**
- Time of day → *Not used*
- Global economic index → *Economy will be per system/faction*
- Political state → *Handled in Faction model*
- Mission counters → *Handled in Mission/Narrative state*
- Universal anomaly flags → *Handled inside EV%() or Mission flags*

This category is intentionally minimal for simplicity and performance.

---

# 2. Player Character (Updated With Decisions)

The player’s state includes identity, economy, and faction relationships.  
We removed *attributes* (INT, PER, etc.) and replaced them with finalized **skills**.

## **Player Identity**
- **PN$** — Player name  
- **Species/origin** — (Optional, world‑building only)

## **Vital Statistics**
- **XP** — Experience points (float)
- **LV** — Level (derived from XP or stored)
- **HP**, **HP_MAX** — Current / maximum health

## **Economy & Reputation**
- **CRD** — Currency / credits
- **REP%(factionIndex)** — Reputation per faction
- **FIN%(factionIndex)** — Fines or bounties per faction
- **TAG$()** — Special status tags (e.g., WANTED, DIPLOPASS)

## **Final Player Skills (7 skills)**
Stored as floats for performance:

```
DIM SK(6)
```

### Skill Mapping
- **SK(0)** — Leadership  
- **SK(1)** — Tactical  
- **SK(2)** — Trading  
- **SK(3)** — Engineering  
- **SK(4)** — Navigation  
- **SK(5)** — Evasion  
- **SK(6)** — CyberTechs (hacking & tech mastery)

### Effective Skill Calculation
Crew modifier:

```
CREWM = .75 + CR/200
```

Ship modifier:

```
SHIPM = .75 + SH/200
```

Effective rating:

```
EFF = SK * CREWM * SHIPM
IF EFF > 150 THEN EFF = 150
```

Success chance:

```
CH = 20 + (EFF * .5)
IF CH > 95 THEN CH = 95
```

---

# 3. Ship Identity

High‑level ship information independent of crew and systems.

- **Ship type** (index to ship database)
- **Ship name**
- **Registration ID**

## **Location**
- Docked at station ID (`LO%` covers this)
- OR free‑space coordinates (future)
- OR in‑transit flag (future)

## **Fuel & Cargo**
- **Fuel level**
- **Fuel capacity**
- **Cargo capacity** (max)

---

# 4. Ship Crew

Crew members provide bonuses in the same skill categories as the player.

Minimum crew roles:
- Navigator  
- Engineer  
- Helmsman  
- Tactical Officer  
- Quartermaster  
- Medical Officer  

Each has:
- Name
- `CR()` rating for each skill they influence (0–100)
- Health
- Experience (optional)
- Loyalty/morale
- Status (active/injured/off‑ship)

8‑bit compressed form:

```
CREW$(i)
CR(i,j)      ' crew skill j for crew member i
CHP(i)       ' health
CMO(i)       ' morale/loyalty
```

---

# 5. Ship Systems & Subsystems

Core, weapon, defensive, and utility systems.  
Each system supports:

- Installed flag  
- Performance rating  
- Damage level  

## **Core Systems**
- Hull integrity
- Shields (current/max)
- Engines (power/damage)
- Jump drive
- Life support
- Reactor output

## **Weapons**
Per slot:
- Type
- Damage
- Energy cost
- Reload/cooldown
- Ammo count (if applicable)
- Condition

## **Defensive Systems**
- Shield generator variant
- Armor plating
- ECM/ECCM
- Cloaking
- Point-defense

## **Utility Systems**
- Navigation computer
- Sensors
- Cargo scanner
- Mining laser
- Tractor beam
- Auto-pilot
- Fuel scoop
- Docking computer

---

# 6. Cargo & Goods

Cargo inventory is tracked as parallel arrays.

```
TYPE(i)
QTY(i)
COST(i)     ' average cost per unit
FLAG(i)     ' illegal, hazardous, mission-critical, perishable
```

Also:
- Cargo free space
- Special containers (cryopods, hazmat, etc.)

---

# 7. Missions & Narrative State

Minimal persistent mission system:

- Active mission IDs  
- Mission destination  
- Mission deadline  
- Target object/person  
- Status flags (in progress / failed / complete)  
- Story flags (wormhole opened, rebellions, artifacts destroyed)

---

# 8. Local World at Current Location

Cached details for quick UI response:

- Station services available  
- Local economic multipliers  
- Local faction control  
- Available missions  
- Local law level (scan strictness, contraband rules)

---

# 9. Player Meta Options

Not part of the world, but part of the save state:

- Difficulty  
- Game settings  
- Save-format version  

---

# 10. Internal Engine State

Useful for resuming:

- Last visited system  
- Last docked port  
- Last random encounter ID  
- Current ambient track  
- Menu selection indexes  

---

# 11. Derived Stats

These may be stored or computed:

- Player combat rating  
- Ship combat rating  
- Trade efficiency score  
- Faction alignment summary  
- Total ship power draw  
- Effective sensor range  
- Effective jump distance  

---

# 12. Debug & Dev Fields

Optional but useful during development:

- DEBUG mode flag  
- TRACE index  
- SEED$ (stringified seed)
- Error code/message buffers  

---

# Implementation Mapping Next Steps

Future work will map this model to:

- Commander X16 BASIC variables  
- Arrays like `AN%()`, `AF()`, `AS$()`  
- Save‑game file format (ASCII or tokenized)
- Compression strategies for a RAM‑limited 8‑bit environment  
- Subroutine architecture that keeps state handling organized

---

This document summarizes the *entire state model so far*, incorporating all design decisions made.  
