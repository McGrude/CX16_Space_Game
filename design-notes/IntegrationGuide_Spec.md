# Commander X16 Space RPG — Skill + Crew + Equipment Integration Guide

This document explains how **skills**, **crew**, and **equipment** combine to determine all gameplay actions.

---

# 1. Core Formula

Every action in the game maps to a primary skill `SI` (0..6):

```
CREWM = .75 + CR(SI)/200
SHIPM = .75 + SH(SI)/200

EFF = SK(SI) * CREWM * SHIPM
IF EFF > 150 THEN EFF = 150

CH = 20 + (EFF * .5)
IF CH > 95 THEN CH = 95
```

Where:
- `SK()` = player skills
- `CR()` = crew contributions
- `SH()` = equipment contributions
- `EFF` = internal effective rating
- `CH` = final success chance (%)

---

# 2. How Each Action Maps to Skills

## 2.1 Trading (SK 2)
- Better buy/sell prices  
- Better mission payouts  
- Better fine/bribe modifiers  
(Trading has no crew or equipment.)

## 2.2 Combat – Tactical (SK 1)
- Hit chance  
- Critical chance  
- Defensive hit mitigation  
Crew: Tactical Officer  
Equipment: Weapons, tactical computers/scanners

## 2.3 Repairs / Engineering Actions (SK 3)
- Faster repairs  
- Lower repair costs  
- Tech upgrade eligibility  
Crew: Chief Engineer  
Equipment: Reactor, engines, shields, armor

## 2.4 Navigation / Travel (SK 4)
- Fuel efficiency  
- Hazard avoidance  
- Jump accuracy  
Crew: Navigator  
Equipment: Nav computer, long-range scanner, ore scanner

## 2.5 Evasion / Stealth (SK 5)
- Avoid scans  
- Escape combat  
- Reduce interception chance  
Crew: ESO  
Equipment: ECM, jammers, stealth plating, heat management

## 2.6 CyberTech / Hacking (SK 6)
- Disable enemy subsystems  
- Spoof IDs  
- Crack comms  
- Counter-hack defense  
Crew: CyTech  
Equipment: Cyberdeck, intrusion suite, decryption modules, ICE

## 2.7 Leadership (SK 0)
- Crew morale  
- Crisis outcomes  
- Crew reaction bonuses  
Crew: Captain, XO  
No equipment.

---

# 3. Ensuring Every Skill and Equipment Matters

- Each skill has **one main crew role** and **one curated equipment set**.
- Equipment always modifies `SH(SI)` for exactly one skill.
- No duplicated or dead-end items.
- Crew and equipment amplify but do not overshadow the player.

---

# 4. Secondary Interactions

Optional but easy to add:
- Morale modifies crew performance through Leadership  
- System damage reduces equipment effectiveness (`SH()` temporarily)  
- Crew injury reduces `CR()`  

---

This guide ensures that every game action flows consistently through skills, crew, and equipment.
