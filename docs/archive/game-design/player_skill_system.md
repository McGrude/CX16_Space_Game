# Player Skill System Summary

## Skill Storage
Skills are stored as floating-point values:

```basic
DIM SK(6)
```

### Skill Index Mapping
- **SK(0)** — Leadership  
- **SK(1)** — Tactical  
- **SK(2)** — Trading  
- **SK(3)** — Engineering  
- **SK(4)** — Navigation  
- **SK(5)** — Evasion  
- **SK(6)** — CyberTechs (Hacking / Systems Mastery)

## Skill Combination Model
Final effective skill rating is derived from:
- Player skill (`SK`)
- Crew contribution (`CR`)
- Ship/equipment contribution (`SH`)

### Modifiers
```
CREWM = .75 + CR/200
SHIPM = .75 + SH/200
```

### Effective Rating
```
EFF = SK * CREWM * SHIPM
IF EFF > 150 THEN EFF = 150
```

### Success Chance Mapping
```
CH = 20 + (EFF * .5)
IF CH > 95 THEN CH = 95
```

This ensures:
- A minimum 20% chance of success
- A maximum cap of 95% success, even at elite skill levels
- Player skill is the primary driver; crew and ship provide meaningful but controlled bonuses
