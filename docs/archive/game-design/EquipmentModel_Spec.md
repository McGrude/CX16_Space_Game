# Commander X16 Space RPG — Equipment Model Specification

This document defines the **final equipment model**, mapping equipment to skills, subsystems, crew roles, and installation rules.

---

# 1. Overview

Equipment modifies player effectiveness through the shared formula:

```
SHIPM = .75 + SH(skillIndex)/200
EFF = SK(skillIndex) * CREWM * SHIPM
```

Equipment contributes only through **SH(skillIndex)**.  
Each equipment item aligns with **exactly one skill**, ensuring mechanic clarity and no redundancy.

---

# 2. Equipment Categories by Skill

## 2.1 Leadership — SK(0)
**Equipment:** None  
Leadership is influenced only by:
- Captain (player)
- Executive Officer (XO)

---

## 2.2 Tactical — SK(1)
**Equipment:**
- Beam weapon
- Torpedo weapon
- Tactical computer
- Tactical scanner

**Purpose:**  
Improve combat accuracy, critical chances, initiative, and targeting.

---

## 2.3 Trading — SK(2)
**Equipment:** None  
Trading remains entirely player‑driven.

---

## 2.4 Engineering — SK(3)
**Equipment:**
- Reactor
- Engines
- Shields
- Armor

**Purpose:**  
Affects repair rate/cost, energy performance, resilience, and tech eligibility.

---

## 2.5 Navigation — SK(4)
**Equipment:**
- Ore scanner
- Navigation computer
- Long-range scanner

**Purpose:**  
Improves jump efficiency, hazard avoidance, resource scanning, and route accuracy.

---

## 2.6 Evasion — SK(5)
**Equipment:**
- ECM
- Sensor jammers
- Stealth plating
- Heat management systems

**Purpose:**  
Reduces scan detection, smuggling risk, interception, and enhances disengagement.

---

## 2.7 CyberTechs — SK(6)
**Equipment:**
**Offensive:**
- Cyberdeck
- Intrusion suite (ICE-breakers)
- Exploit modules

**SIGINT / Passive:**
- Decryption modules
- Comms interceptors

**Defensive:**
- ICE (Intrusion Countermeasures Electronics)
- Firewall modules

**Purpose:**  
Hacking, counter-hacking, SIGINT, enemy subsystem disruption.

---

# 3. Subsystem Slots (High-Level)

Each ship has a limited number of equipment slots, allocated by ship type.

Proposed initial layout:
- 1 × Reactor
- 1 × Engine
- 1 × Shield
- 1 × Armor
- 2 × Tactical weapons
- 1 × Tactical computer
- 1 × Tactical scanner
- 1 × Navigation computer
- 1 × Long-range scanner
- 1 × Ore scanner
- 1 × ECM
- 1 × Stealth/Jammer slot
- 1 × Cyberdeck
- 1 × ICE module

Ships may have fewer slots depending on class.

---

# 4. Installation Rules

- Ship class gating:  
  Certain equipment requires minimum class level (e.g., heavy reactor needs ship class ≥ 3).

- Equipment capacity:  
  `ST_EQP(shipType)` defines the installation budget or slot count.

- No duplicate conflict items unless explicitly allowed.  
  (e.g., only one reactor, one engine, one cyberdeck.)

---

# 5. Save Game Behavior

**Saved:**  
- Installed equipment IDs  
- Dynamic equipment states (damage, ammo, condition)

**Not saved:**  
- Static equipment definitions (reload from CSV)

---

This document defines the complete equipment model for the game.
