# Space Trader Game Design Document
**Platform:** Commander X16  
**Genre:** Turn-Based Space Trading/Combat RPG  
**Inspiration:** Escape Velocity series (Ambrosia Software)  
**Version:** 0.1 - Initial Design  
**Last Updated:** November 21, 2024

---

## Table of Contents
1. [Technical Specifications](#technical-specifications)
2. [Core Concept](#core-concept)
3. [Player Progression](#player-progression)
4. [Crew System](#crew-system)
5. [Combat System](#combat-system)
6. [Escort System](#escort-system)
7. [Faction System](#faction-system)
8. [Economy & Trading](#economy--trading)
9. [Time & Navigation](#time--navigation)
10. [Universe Structure](#universe-structure)
11. [Ship & Equipment System](#ship--equipment-system)
12. [User Interface](#user-interface)
13. [Memory Organization](#memory-organization)
14. [Data Structures](#data-structures)
15. [Development Roadmap](#development-roadmap)

---

## Program Architecture

### Modular Design with Chain Loading

The game uses **multiple separate BASIC programs** that chain load between major interface changes. Each program handles one primary screen/mode, with game state persisted to disk between transitions.

**Core Modules:**
- **MAIN.BAS** - Title screen, new game setup, load game
- **DOCKED.BAS** - Station interface (trade, missions, hiring, outfitting)
- **SPACE.BAS** - Space travel, navigation, random encounters
- **COMBAT.BAS** - Turn-based combat sequences
- **MISSION.BAS** - Mission briefing and completion screens

### State Persistence

**GAMESTATE.DAT File:**
Contains all player/universe state that must persist across program transitions:
```
Player Core (50 bytes):
  - Credits (4 bytes)
  - Current System ID (1 byte)
  - Current Day (2 bytes)
  - Attributes: Piloting, Combat, Engineering, Navigation, Leadership (5 bytes)
  - Total XP (2 bytes)
  - Current Ship ID (1 byte)

Faction Data (20 bytes):
  - Reputation array (10 factions × 2 bytes = -100 to +100)

Ship State (50 bytes):
  - Hull/Shields current values
  - Installed equipment flags
  - Weapon slots
  - Cargo current
  - Fuel current

Crew Data (65 bytes):
  - 5 crew slots × 13 bytes each

Escort Data (100 bytes):
  - 2 escort slots × 50 bytes each

Cargo Inventory (40 bytes):
  - 10-20 commodity quantities

Mission State (100 bytes):
  - Active mission IDs and progress flags

Flags/Progress (100 bytes):
  - Story progression markers
  - Discovered systems
  - Unlocked content
```

**State Management Pattern:**
```basic
' At end of DOCKED.BAS
1000 GOSUB SAVE_STATE: ' Write GAMESTATE.DAT
1010 RUN "SPACE.BAS"

' At start of SPACE.BAS  
100 GOSUB LOAD_STATE: ' Read GAMESTATE.DAT
110 REM Continue with space interface
```

**Save/Load Implementation:**
```basic
8000 REM === SAVE STATE ===
8010 OPEN 1,8,2,"SAVES/GAMESTATE.DAT,S,W"
8020 PRINT#1, CREDITS
8030 PRINT#1, CURRENT_SYSTEM
8040 PRINT#1, CURRENT_DAY
8050 PRINT#1, PILOT_SKILL
8060 REM ... save all state variables
8100 CLOSE 1
8110 RETURN

9000 REM === LOAD STATE ===
9010 OPEN 1,8,2,"SAVES/GAMESTATE.DAT,S,R"
9020 INPUT#1, CREDITS
9030 INPUT#1, CURRENT_SYSTEM
9040 INPUT#1, CURRENT_DAY
9050 INPUT#1, PILOT_SKILL
9060 REM ... load all state variables
9100 CLOSE 1
9110 RETURN
```

### Shared Code Strategy

**No native #include in BASIC**, so shared code is handled via:

**Build-Time Assembly:**
Cross-development on modern machine (Mac/Linux) allows build scripts:
```makefile
# Makefile
COMMON := common.bas

DOCKED.BAS: $(COMMON) docked_main.bas
	cat $(COMMON) docked_main.bas > DOCKED.BAS

SPACE.BAS: $(COMMON) space_main.bas
	cat $(COMMON) space_main.bas > SPACE.BAS

COMBAT.BAS: $(COMMON) combat_main.bas
	cat $(COMMON) combat_main.bas > COMBAT.BAS
```

**Common Subroutines (in COMMON.BAS):**
- SAVE_STATE / LOAD_STATE
- CSV parser (PARSE_CSV)
- Data file loaders (FIND_SHIP, FIND_SYSTEM, etc.)
- Screen drawing helpers (DRAW_HEADER, DRAW_BORDER)
- Input validation routines
- Combat calculation helpers
- RNG utilities

**Code Tier Strategy:**
- **Tier 1 (Critical):** Copied into all modules - SAVE/LOAD state, file I/O
- **Tier 2 (Moderate):** Copied where needed - UI helpers, calculations  
- **Tier 3 (Specific):** Module-only - Combat AI, station menus

**Future Optimization:**
If performance becomes critical, frequently-used routines can be rewritten in assembly and loaded as machine language library (COMMON.ML).

### Development Workflow

**Cross-Development Setup:**
1. Edit source files on Mac/PC (VSCode, etc.)
2. Run Make to assemble final .BAS files
3. Transfer to X16 SD card image
4. Test on emulator or hardware
5. Iterate

**Source Structure:**
```
/SOURCE/
  common.bas          (shared subroutines)
  docked_main.bas     (docked-specific code)
  space_main.bas      (space-specific code)
  combat_main.bas     (combat-specific code)
  Makefile           (build automation)
  
/BUILD/
  DOCKED.BAS         (assembled output)
  SPACE.BAS
  COMBAT.BAS
```

**Version Control:**
Source files (.bas) in git, assembled output (.BAS) generated at build time.

---

## Technical Specifications

### Hardware
- **Platform:** Commander X16
- **CPU:** 65C02 @ 8MHz
- **RAM:** 512KB banked RAM
- **Video:** VERA graphics chip
- **Display Mode:** 80×60 character text mode

### Software
- **Primary Language:** BASIC
- **Optional:** Assembly language helpers for:
  - Graphics routines
  - Banking operations
  - Combat calculations
  - Performance-critical sections

### Memory Layout
- **Low RAM ($0000-$9EFF):** ~40KB for BASIC program and active game state
- **Banked RAM ($A000-$BFFF):** 8KB window into 512KB (64 banks × 8KB)
- **Banking Register:** $9F61

---

## Core Concept

### Game Overview
A sandbox space exploration and trading game with RPG elements, turn-based tactical combat, and faction-based storylines. Players start with a small ship and build their reputation, wealth, and fleet through trading, combat, and missions.

### Core Gameplay Loop
1. Accept missions or plan trade routes
2. Navigate between star systems (time-based travel)
3. Trade commodities at stations
4. Engage in turn-based combat when necessary
5. Manage crew, escorts, and ship upgrades
6. Build reputation with factions
7. Progress through faction storylines

### Design Philosophy
- **Sandbox freedom:** Player chooses their path (trader, pirate, military)
- **Meaningful choices:** Faction alignment locks out opposing paths
- **Deep but accessible:** Complex systems with intuitive interface
- **Replayability:** Multiple faction paths and ship progressions
- ** 8-bit appropriate:** Design within technical constraints

---

## Player Progression

### Character Attributes
All attributes range from 1-10, gained through XP and level-ups.

| Attribute | Affects | Bonus Formula |
|-----------|---------|---------------|
| **Piloting** | Ship evasion, fuel efficiency | +1% Evasion per level |
| **Combat** | Weapon accuracy and damage | +1% Accuracy per level |
| **Engineering** | Shield regeneration, armor effectiveness, repairs | +1% Shield Regen per level, +(level/2)% Armor |
| **Navigation** | Travel time, initiative, flee chance | +(level/2)% Initiative, +1% Flee per level |
| **Leadership** | Crew morale, escort effectiveness | +1% Escort Stats per level |

### Experience & Leveling
```
XP Sources:
- Combat victory: +50-200 XP (based on enemy difficulty)
- Mission completion: +100-500 XP
- Trade runs: +10-50 XP
- Discovery: +100 XP (new systems)

Level Up Requirements:
Level 1→2: 400 XP
Level 2→3: 800 XP
Level N→N+1: 400 × N XP
```

### Ship Progression Path

**Starter Ship: Scout**
- Hull: 100
- Shields: 50
- Armor: 5
- Weapons: 1 slot
- Equipment: 2 slots
- Cargo: 20 tons
- Cost: Starting ship

**Mid-Game: Armed Freighter**
- Hull: 250
- Shields: 100
- Armor: 15
- Weapons: 2 slots
- Equipment: 4 slots
- Cargo: 100 tons
- Cost: ~45,000 cr

**End-Game: Battlecruiser**
- Hull: 500
- Shields: 200
- Armor: 40
- Weapons: 4 slots
- Equipment: 6 slots
- Cargo: 50 tons
- Cost: ~250,000 cr

---

## Crew System

### Crew Positions
Maximum 5 crew members (including player as captain/pilot).

#### 1. Pilot (Player or Hired)
- **Primary Skill:** Piloting
- **Secondary Skill:** Combat
- **Bonuses:**
  - +Piloting% to Ship Evasion
  - +Combat% to Ship Accuracy
  - +(Leadership/2)% to Escort Effectiveness (if player is captain)

#### 2. Gunner
- **Primary Skill:** Combat
- **Secondary Skill:** Piloting
- **Bonuses:**
  - +Combat% to Weapon Damage
  - +Piloting% to Weapon Accuracy

#### 3. Engineer
- **Primary Skill:** Engineering
- **Secondary Skill:** None
- **Bonuses:**
  - +Engineering% to Shield Regeneration
  - +(Engineering/2)% to Armor Effectiveness
- **Special Ability:** Emergency repairs during combat

#### 4. Navigator
- **Primary Skill:** Navigation
- **Secondary Skill:** Engineering
- **Bonuses:**
  - +(Navigation/2)% to Initiative
  - +Navigation% to Flee Success
- **Special Ability:** Scan enemies to reveal full stats

#### 5. Tactical Officer (Optional)
- **Primary Skill:** Combat/Leadership
- **Bonuses:**
  - +Leadership% to all Escort stats
- **Special Ability:** Coordinate focused fire

### Crew Management

**Hiring:**
- Available at station Hiring Halls
- Cost: 400-800 cr/month depending on skills
- Skills randomized: Rookie (3-5), Experienced (6-7), Veteran (8-9), Ace (10)

**Progression:**
- Crew gain XP through combat and missions
- Level up: Skills improve by 1 (max 10)
- XP Requirements: 400 × Current Level

**Loyalty System:**
- 0-3 months: Normal (will leave if unpaid)
- 4-8 months: Loyal (1 month grace period)
- 9+ months: Devoted (won't leave, but morale drops)

**Monthly Salary:**
- Due every 30 in-game days
- Miss 1 payment: Warning, -10% effectiveness
- Miss 2 payments: Ultimatum
- Miss 3 payments: Crew deserts permanently

---

## Combat System

### Core Mechanics
**System:** Turn-based tactical, d100 percentile rolls

### Turn Order
```
Initiative = (Ship Speed × 10) + Pilot Skill + d20

Example:
Player Ship (Speed 3, Pilot 7): 30 + 7 + 12 = 49
Enemy Ship (Speed 4, Pilot 4): 40 + 4 + 15 = 59

Turn order: Enemy (59) → Player (49)
```

### Ship Combat Stats

| Stat | Range | Description |
|------|-------|-------------|
| Hull Points | 100-500 | Hit points |
| Shields | 0-200 | Regenerating defense (10-20/turn) |
| Armor | 0-50 | Reduces incoming damage |
| Accuracy | 40-80% | Base chance to hit |
| Evasion | 30-70% | Enemy penalty to hit |
| Speed | 1-5 | Movement points and initiative |
| Power | 100-300 | Energy for abilities |

### To-Hit Calculation
```
Base Hit Chance = Attacker's Accuracy
                - Defender's Evasion
                + Range Modifier (-10% per hex beyond optimal)
                + Weapon Accuracy Bonus
                + Attacker's Combat Skill
                + Gunner's Combat Skill (if present)
                = Final Hit %

Roll d100: If roll ≤ Final Hit %, attack hits
```

### Damage Calculation
```
IF hit:
  Base Damage = Weapon Damage
              + Variance (±20%)
              + Gunner Combat Skill% bonus
  
  Apply damage to Shields first
  Overflow damage → Hull (reduced by Armor)
  
Example:
  Laser deals 25 damage
  Variance roll: 23 damage
  Gunner (Combat 8): +8% = 25 damage total
  
  Enemy Shields: 20 → 0 (depleted)
  Remaining: 5 damage
  Enemy Armor: 15
  Hull damage: 0 (armor absorbed it)
```

### Combat Actions

**Standard Actions:**
1. **Attack [target]** - Fire weapons at selected enemy
2. **Defend** - +20% evasion this turn, no other action
3. **Flee** - Attempt escape (success based on speed difference)

**Special Actions (Power Cost):**
4. **EMP Blast (30 power)** - Enemy loses turn, shields drop 50%
5. **Emergency Repairs (20 power)** - Restore 50 hull points
6. **Overcharge Shields (40 power)** - Double shield regen for 3 turns
7. **Precision Shot (25 power)** - +30% accuracy, +50% damage this attack
8. **Coordinate Fire (leadership required)** - All escorts focus one target
9. **Scan Enemy (navigator required)** - Reveal full enemy stats

### Multi-Ship Combat
- **Player side:** 1 player ship + 0-2 escorts
- **Enemy side:** 1-4 enemy ships
- **Maximum total:** 7 ships in battle
- **AI Behavior:**
  - Enemies target weakest/lowest shields first
  - Spread damage when all targets healthy
  - 60% chance to finish wounded targets

### Critical Hits
- Natural roll of 95+ on successful hit
- Effect: Double damage OR disable random enemy system
- Player chooses which effect

### Victory Conditions
- **Win:** All enemy ships destroyed
- **Lose:** Player ship hull reaches 0
- **Flee:** Successful flee attempt (escorts must also escape)

### Loot & Rewards
```
Per destroyed enemy:
- Credits: 100-5000 (based on ship class)
- Salvage: Random equipment/weapons (20% chance)
- Cargo: Enemy cargo transferred to player (if space)
- XP: Distributed to player and crew
```

---

## Escort System

### Overview
- **Capacity:** 0-2 permanent hired escorts
- **Control:** AI-controlled with player commands
- **Cost:** Monthly salary (500-7,500 cr depending on ship/pilot)
- **Payment:** Due every 30 days along with crew

### Escort Ship Types

| Type | Hull | Shields | Weapons | Speed | Cost/Month |
|------|------|---------|---------|-------|------------|
| Fighter | 80 | 40 | 1 | 4 | 500 cr |
| Corvette | 150 | 80 | 2 | 3 | 1,200 cr |
| Frigate | 250 | 120 | 3 | 2 | 2,500 cr |
| Repair Ship | 100 | 60 | 0 | 2 | 1,800 cr |
| Tank | 300 | 150 | 1 | 1 | 2,200 cr |

### Escort Pilots

**Pilot Quality Multipliers:**
- **Rookie** (Skills 3-5): ×1.0 base cost
- **Experienced** (Skills 6-7): ×1.5 base cost
- **Veteran** (Skills 8-9): ×2.0 base cost
- **Ace** (Skills 10): ×3.0 base cost

### Escort Commands

**AI Behavior Modes:**
- **Aggressive:** Always attacks, targets weakest enemy
- **Defensive:** Protects player, intercepts attackers
- **Balanced:** Attacks but retreats if damaged <30%

**Direct Commands (during combat):**
- Focus Fire [target] - All escorts attack same target
- Defend Me - Stay close, intercept attacks on player
- Attack Freely - Independent targeting
- Retreat - Escorts flee (player can continue)

### Escort Management

**Hiring:**
- Location: Station Hiring Halls
- Availability: Affected by reputation and station quality
- Selection: View ship type, pilot name, skills, monthly cost

**Upgrading:**
- Upgrade escort ship at shipyards (keeps same pilot)
- Add equipment to escorts (weapons, shields)
- Fighter → Corvette: ~15,000 cr upgrade cost

**Dismissal:**
- Immediate, no severance pay
- Pilot returns to hiring pool

**Loyalty:**
- Same system as crew
- Long-term escorts (9+ months) are devoted

### Escort Progression
```
XP Gain: +50 per battle participation
Level Requirements: 400 × Current Level XP

Level Benefits:
- Skills improve (+1 per level, max 10)
- Ship stats improve (+5% per level)
- Better combat AI decisions
```

---

## Faction System

### Major Factions
**Recommended Structure:** 3-4 major factions

**Example Faction Setup:**
1. **Core Worlds Federation**
   - Lawful, military-focused
   - Controls central systems
   - Technology: Heavy shields, energy weapons

2. **Outer Colonies Alliance**
   - Independent, frontier justice
   - Controls outer rim systems
   - Technology: Fast ships, missiles

3. **Merchant Guild**
   - Neutral traders
   - Economic power
   - Technology: Cargo expansion, trade computers

4. **Pirates/Outlaws**
   - Hostile to most
   - Hidden bases
   - Technology: Cloaking, boarding

### Reputation System

**Scale:** -100 (Hostile) to +100 (Allied)

| Range | Status | Effects |
|-------|--------|---------|
| -100 to -25 | **Hostile** | Attacked on sight, can't dock, bounty hunters |
| -24 to +24 | **Neutral** | Basic trading, limited missions, standard prices |
| +25 to +74 | **Friendly** | Better equipment, faction missions, 10% discount, assistance in combat |
| +75 to +100 | **Allied** | Unique ships, story missions, 20% discount, access to restricted systems |

### Reputation Changes

**Actions Affecting Reputation:**
```
POSITIVE:
+ Complete faction mission: +5 to +15 (mission dependent)
+ Destroy faction enemies: +2 to +10
+ Trade regularly: +1 per transaction (slow build)
+ Protect faction ships: +5

NEGATIVE:
- Attack faction ships: -10 to -25
- Fail faction mission: -5 to -15
- Trade with enemies: -2 to -5
- Illegal actions in faction space: -10 to -30

CROSS-FACTION EFFECTS:
- Helping Federation: Rebels -5
- Helping Pirates: Federation -10, Merchants -5
- Neutral trade: Minimal impact
```

### Mission System

**Mission Tiers by Reputation:**

**Tier 1 (Neutral, +0 to +24):**
- Simple cargo delivery
- Courier missions
- Basic patrol

**Tier 2 (Friendly, +25 to +74):**
- Escort missions
- Bounty hunting
- Smuggling (if appropriate)
- Multi-leg trade routes

**Tier 3 (Allied, +75 to +100):**
- Faction story arc missions (6-8 missions)
- Special operations
- Faction warfare
- Access to unique rewards

### Faction Storylines

**Structure:**
- Each major faction: 6-8 mission story arc
- Branching points: Key decisions affect outcome
- Exclusivity: Completing one faction's arc may lock out opposing faction
- Consequences: Permanent reputation changes

**Rewards:**
- Unique ships available for purchase
- Special equipment
- Permanent discounts
- Access to restricted systems
- Title/rank within faction

---

## Economy & Trading

### Commodity System

**Core Commodities (6-10 types):**

| Commodity | Description | Typical Production | Typical Demand |
|-----------|-------------|-------------------|----------------|
| Metals | Basic materials | Mining colonies | Industrial worlds |
| Food | Agricultural products | Agricultural worlds | High-tech/urban worlds |
| Textiles | Clothing, fabrics | Agricultural/low-tech | All worlds (baseline) |
| Electronics | Tech goods | High-tech worlds | Low-tech/colony worlds |
| Medical Supplies | Medicine, equipment | High-tech worlds | All worlds, especially colonies |
| Luxury Goods | Art, jewelry | High-tech/wealthy | Wealthy worlds |
| Weapons | Military equipment | Industrial/military | Conflict zones |
| Machinery | Industrial equipment | Industrial worlds | Developing colonies |
| Pharmaceuticals | Advanced drugs | High-tech/medical worlds | All worlds |
| Contraband | Illegal goods | Pirate bases | Black markets |

### Pricing System

**Base Price Calculation:**
```
System Base Price = Commodity Base × Tech Level Modifier × Government Modifier

Price Variance: ±30% from base
Buy Price: Base Price × 1.1 (10% markup)
Sell Price: Base Price × 0.9 (10% markdown)

Price Updates: Every 3-5 in-game days
```

**Regional Specialization:**
- Agricultural worlds: Food cheap (-40%), Electronics expensive (+50%)
- Mining colonies: Metals cheap (-50%), Luxury goods expensive (+80%)
- High-tech worlds: Electronics cheap (-30%), Food expensive (+40%)
- Wealthy systems: Luxury goods normal, Basic goods expensive (+30%)

**Dynamic Events Affecting Prices:**
```
Event Types:
- War/Conflict: Weapons +50%, Food +30%
- Plague: Medical supplies +60%, Food -20%
- Discovery: Specific commodity -40%
- Shortage: Specific commodity +70%
- Festival: Luxury goods +40%

Event Duration: 5-15 days
Event Propagation: News spreads over time to nearby systems
```

### Trading Mechanics

**Cargo Management:**
- Cargo capacity: Ship-dependent (20-100 tons)
- Buy in bulk: Quantity limited by credits and cargo space
- Sell in bulk: Sell all or portion
- Jettison: Emergency cargo dump (lose goods)

**Trade Routes:**
- Player discovers profitable routes through exploration
- Trade computer (upgrade) can suggest routes
- Higher-tier computers show better opportunities

**Contraband:**
- Higher profit margins (100-300%)
- Illegal in Federation/lawful systems
- Risk: Cargo scans at stations
- Penalty if caught: Fine (50% cargo value), reputation loss, possible combat

---

## Time & Navigation

### Time System

**Time Tracking:**
- Simple day counter (Day 1, Day 2, etc.)
- No hours/minutes - day is atomic unit
- Monthly cycle: Every 30 days

**Time Passage:**
- Jumping between systems: Only time that passes
- Station activities: Instant (no time cost)
- Combat: No time cost
- Repairs/refueling: Instant

### Travel Mechanics

**Distance Calculation:**
```
Distance = sqrt((x2 - x1)² + (y2 - y1)²)

Travel Time (Days) = ceil(Distance) + 1

Example:
Sol (5,5) → Alpha Centauri (6,6)
Distance = sqrt(1² + 1²) = 1.414
Travel Time = ceil(1.414) + 1 = 3 days

Sol (5,5) → Sirius (10,8)
Distance = sqrt(25 + 9) = 5.831
Travel Time = ceil(5.831) + 1 = 7 days
```

**Fuel Consumption:**
```
Fuel Cost = ceil(Distance × 3) units

Adjacent system: ~3-6 fuel units
Medium jump: ~15-24 fuel units
Long haul: ~45-60 fuel units

Fuel Price: 10 credits per unit
Tank Capacity: 50-200 units (ship dependent)
```

**Navigation Upgrades:**

| Equipment | Effect | Cost |
|-----------|--------|------|
| Standard Nav | Distance + 1 days | Included |
| Nav Computer I | Distance + 0.5 days | 5,000 cr |
| Nav Computer II | Distance × 0.9 + 0.5 days | 15,000 cr |
| Advanced Nav | Distance × 0.75 days (min 1) | 35,000 cr |

**Navigator Crew Bonus:**
- Navigation skill 10: -10% travel time

### Travel Interface

**Pre-Jump Display:**
```
Current System: Sol
Destination: Betelgeuse
Distance: 8.2 light-years
Travel Time: 9 days
Fuel Required: 24 units
Arrival Date: Day 136

Current Day: Day 127
Next Payroll Due: Day 150 (14 days after arrival)

[JUMP] [CANCEL]
```

**Transit Events (5-10% chance on jumps >7 days):**
- Engine malfunction (delay or damage)
- Encounter distress signal
- Fuel leak (lose fuel)
- Crew incident (morale change)
- Nothing (most common)

### Monthly Expenses

**Payment Due: Day 30, 60, 90, etc.**
```
Payroll Breakdown:
- Crew wages: 400-800 cr/crew member
- Escort salaries: 500-7,500 cr/escort
- Ship maintenance: 0 cr (happens every 90 days separately)

Total: 2,000-10,000+ cr depending on crew size and escorts

Warning: 7 days before due date
Consequences: See Crew System and Escort System sections
```

**Ship Maintenance:**
```
Required: Every 90 days
Cost: 1,000-5,000 cr (ship dependent)

If skipped:
- All ship stats: -5%
- Risk of system failure during combat/travel
- Accumulating penalty each 90-day period
```

---

## Universe Structure

### Galaxy Layout

**Type:** Hand-crafted galaxy with fixed systems  
**Size:** 30-40 star systems  
**Coordinates:** Cartesian grid (0-30 on X and Y axes)

**Design Philosophy:**
- Quality over quantity
- Each system has personality and purpose
- Strategic positioning creates natural trade routes
- Faction territories clearly defined

### System Types

**Core Systems (Federation Space):**
- High tech level (8-10)
- High population
- All services available
- Heavy patrol presence
- Higher prices, safer

**Colony Systems (Outer Rim):**
- Medium tech level (4-7)
- Lower population
- Basic services
- Light patrol
- Lower prices, opportunities

**Frontier Systems:**
- Low tech level (2-5)
- Sparse population
- Limited services
- No patrols
- Extreme prices, dangerous

**Hidden/Special Systems:**
- Discoverable through exploration or missions
- Unique goods or services
- Story significance

### System Data Structure

**Per System (~100 bytes):**
```
- System ID: 1 byte
- Name: 20 bytes
- Coordinates X,Y: 4 bytes (2 each)
- Government Type: 1 byte
- Tech Level: 1 byte
- Population: 1 byte
- Commodity Prices: 10 bytes (one per commodity)
- Station Services Flags: 1 byte
- Faction Control: 1 byte
- Special Flags: 1 byte
- Description pointer: 2 bytes
- Mission availability flags: 2 bytes
```

### Randomization

**On New Game Start:**
- Initial commodity prices (within ranges): Randomized
- Crew availability at hiring halls: Random names/skills
- Minor event triggers: Randomized timing
- Starting reputation: Small random variance (±5)

**Persistent Across Game:**
- System positions: Fixed
- Base prices: Fixed
- Tech levels: Fixed
- Government types: Fixed

**Dynamic During Play:**
- Current commodity prices: Fluctuate based on events/time
- Available missions: Generated based on reputation/location
- NPC ship encounters: Random
- Faction territory control: Can shift based on missions

---

## Ship & Equipment System

### Ship Classes

**Scout (Starting Ship)**
```
Cost: Starting ship
Hull: 100/100
Shields: 50/50
Armor: 5
Accuracy: 50%
Evasion: 40%
Speed: 3
Power: 100/100
Fuel: 50/50
Cargo: 20 tons

Weapon Slots: 1
Equipment Slots: 2
Upgrade Slots: 4

Good for: Early exploration, courier missions
```

**Armed Freighter (Mid-Game)**
```
Cost: 45,000 cr
Hull: 250/250
Shields: 100/100
Armor: 15
Accuracy: 55%
Evasion: 30%
Speed: 2
Power: 150/200
Fuel: 100/100
Cargo: 100 tons

Weapon Slots: 2
Equipment Slots: 4
Upgrade Slots: 6

Good for: Trading, balanced combat
```

**Battlecruiser (End-Game)**
```
Cost: 250,000 cr
Hull: 500/500
Shields: 200/200
Armor: 40
Accuracy: 70%
Evasion: 25%
Speed: 2
Power: 200/300
Fuel: 150/150
Cargo: 50 tons

Weapon Slots: 4
Equipment Slots: 6
Upgrade Slots: 8

Good for: Heavy combat, faction warfare
```

### Weapons

**Laser Series:**
```
Laser Mk I:
  Damage: 15
  Accuracy: +5%
  Range: 3 hexes
  Power: 5/shot
  Cost: 2,000 cr

Laser Mk II:
  Damage: 25
  Accuracy: +10%
  Range: 4 hexes
  Power: 8/shot
  Cost: 8,000 cr

Laser Mk III:
  Damage: 40
  Accuracy: +15%
  Range: 5 hexes
  Power: 12/shot
  Cost: 25,000 cr
```

**Missiles:**
```
Missile Launcher Mk I:
  Damage: 50
  Accuracy: +20%
  Range: 6 hexes
  Ammo: 10 missiles
  Cost: 12,000 cr
  Ammo Cost: 500 cr/missile

Missile Launcher Mk II:
  Damage: 80
  Accuracy: +25%
  Range: 7 hexes
  Ammo: 15 missiles
  Cost: 30,000 cr
  Ammo Cost: 800 cr/missile
```

**Other Weapons:**
```
Railgun:
  Damage: 35
  Accuracy: -5%
  Range: 5 hexes
  Special: Ignores 50% of armor
  Power: 15/shot
  Cost: 18,000 cr

Plasma Cannon:
  Damage: 60
  Accuracy: 0%
  Range: 3 hexes
  Special: Deals 20 damage to shields even on miss
  Power: 25/shot
  Cost: 45,000 cr
```

### Defensive Equipment

**Shields:**
```
Shield Generator I:
  Max Shields: +50
  Regen: +5/turn
  Cost: 5,000 cr

Shield Generator II:
  Max Shields: +100
  Regen: +10/turn
  Cost: 15,000 cr

Shield Generator III:
  Max Shields: +150
  Regen: +15/turn
  Cost: 40,000 cr
```

**Armor:**
```
Armor Plating I:
  Armor: +10
  Cost: 3,000 cr

Armor Plating II:
  Armor: +20
  Cost: 10,000 cr

Armor Plating III:
  Armor: +30
  Cost: 25,000 cr
```

**ECM/Evasion:**
```
ECM Suite I:
  Evasion: +10%
  Cost: 6,000 cr

ECM Suite II:
  Evasion: +20%
  Cost: 18,000 cr
```

### System Upgrades

**Targeting:**
```
Targeting Computer I:
  Accuracy: +10%
  Cost: 8,000 cr

Targeting Computer II:
  Accuracy: +15%
  Cost: 20,000 cr

Advanced Sensors:
  Accuracy: +5%
  Special: Reveals enemy stats before combat
  Cost: 12,000 cr
```

**Utility:**
```
Cargo Expansion I:
  Cargo: +20 tons
  Cost: 5,000 cr

Cargo Expansion II:
  Cargo: +40 tons
  Cost: 15,000 cr

Fuel Scoop:
  Special: Refuel free in certain systems
  Cost: 10,000 cr

Fire Control System:
  Damage: +10%
  Cost: 15,000 cr

Repair Droid:
  Special: Auto-repair 5 hull per turn in combat
  Cost: 20,000 cr
```

**Trade Equipment:**
```
Trade Computer I:
  Special: Shows profit margins for nearby systems
  Cost: 5,000 cr

Trade Computer II:
  Special: Shows profit margins for all known systems
  Special: Suggests optimal trade routes
  Cost: 15,000 cr

Cargo Scanner:
  Special: Detect contraband on other ships
  Cost: 8,000 cr
```

### Upgrade System

**Installation:**
- Available at shipyards
- Instant installation (no time cost)
- Equipment can be removed and sold for 50% value
- Some equipment has tech level requirements

**Slot System:**
- Each ship has limited weapon/equipment/upgrade slots
- Installing equipment uses one slot
- Must have compatible slot type

---

## User Interface

### Display Specifications
- **Mode:** 80×60 character text mode
- **Graphics:** PETSCII characters for box drawing
- **Colors:** X16 16-color palette

### Standard Screen Layout

**Header (Lines 1-3):**
```
╔══════════════════════════════════════════════════════════════════════════════╗
║ SYSTEM: Sol Station        DAY: 127    CREDITS: 45,250 cr    FUEL: 38/100   ║
╠══════════════════════════════════════════════════════════════════════════════╣
```

**Content Area (Lines 4-57):** 54 lines for main content

**Footer (Lines 58-60):**
```
╠══════════════════════════════════════════════════════════════════════════════╣
║ [Commands and navigation hints]                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Key Screens

1. **Main Station/System Screen** - Hub for all activities
2. **Player Stats Screen** - Character attributes and reputation
3. **Crew Management Screen** - Hire/dismiss/view crew
4. **Ship Status Screen** - Hull, shields, equipment, weapons
5. **Cargo & Trading Screen** - Buy/sell commodities
6. **Navigation Computer** - Select destination, view nearby systems
7. **Stellar Map** - Full galaxy view with system positions
8. **Combat Screen** - Turn-based combat interface
9. **Mission Board** - Available and active missions
10. **Shipyard Screen** - Buy ships, install equipment
11. **Hiring Hall Screen** - Recruit crew and escorts

*(Full ASCII mockups available in main conversation)*

### Color Scheme

**General:**
- Headers/Borders: White or Light Blue
- Normal Text: Light Gray
- Emphasis: Yellow or Light Green
- Warnings: Orange
- Errors/Danger: Red

**Context-Specific:**
- Credits/Money: Yellow
- Hull Damage: Red bars
- Shields: Blue bars
- Friendly Ships: Green or Blue
- Enemy Ships: Red or Orange
- Reputation Positive: Green
- Reputation Negative: Red

### Navigation Between Screens

**Quick Keys (Available Most Places):**
- **P** - Player Stats
- **C** - Crew Management
- **S** - Ship Status
- **M** - Mission Board
- **N** - Navigation Computer
- **T** - Trading/Cargo
- **ESC** - Back/Exit
- **H** - Help

---

## Memory Organization

### Design Philosophy
With modular chain-loaded programs and external data files, RAM usage is dramatically reduced. Each program module only needs:
- Its own code (~6-10KB)
- Current game state variables (~2-3KB)
- Cached data for current context (ship, system, etc.) (~1-2KB)
- UI buffers (~2KB)

**Most data lives on SD card**, loaded on-demand.

### Low RAM Layout ($0000-$9EFF)
```
$0000-$00FF: Zero Page (256 bytes)
  - Most frequently accessed variables
  - Player credits (4 bytes)
  - Current system ID (1 byte)
  - Current day (2 bytes)
  - Ship hull/shields current values
  - Combat state flags

$0100-$01FF: Stack (256 bytes)
  - System stack

$0200-$0400: BASIC system area (512 bytes)

$0400-$07FF: Screen buffer (if used) (1KB)

$0800-$1FFF: Game code (6KB)
  - Main program
  - Core routines

$2000-$2FFF: Current system data (4KB)
  - Active system loaded from bank
  - Working copy for fast access

$3000-$3FFF: Combat/Mission data (4KB)
  - Enemy ships
  - Mission state
  - Temporary calculations

$4000-$7FFF: Additional code/data (16KB)
  - More game routines
  - String data
  - Lookup tables

$8000-$9EFF: Buffer space (~7KB)
  - UI rendering
  - Temporary storage
```

### Banked RAM Layout ($A000-$BFFF via banks)

**Note:** With CSV data files on SD card, banked RAM usage is significantly reduced. Banks primarily used for:
- Graphics data (tiles, sprites)
- Pre-loaded mission/dialog text
- Save game slots
- Future expansion
```
Banks 0-10: Reserved for BASIC system use

Banks 11-20: Graphics Data (80KB)
  Bank 11: UI tiles (borders, buttons, icons)
  Bank 12: Ship sprites (player ships)
  Bank 13: Ship sprites (enemies)
  Bank 14: Planet/station graphics
  Bank 15: Star map tiles
  Bank 16: Combat screen tiles
  Bank 17-20: Additional graphics/animation

Banks 21-25: Mission & Event Data (40KB)
  Bank 21-23: Pre-loaded mission scripts and text
  Bank 24: Random events table
  Bank 25: Dialog text cache

Banks 26-31: Reserved (48KB)
  Future expansion
  Sound data
  Additional content

Banks 32-63: Save Game Slots (256KB)
  Each save: ~4-5KB
  Possible slots: 50+
  Bank 32: Save Slot 1
  Bank 33: Save Slot 2
  etc.
```

**Data Access Pattern:**
Most game data (ships, systems, equipment, factions, commodities) is stored as CSV files on SD card and loaded on-demand via file I/O. This eliminates the need for large data tables in banked RAM.

### Primary Data Access: SD Card Files

With the shift to CSV data files, the primary data access pattern is:
1. Open file on SD card
2. Search sequentially for desired record
3. Parse CSV into BASIC variables
4. Close file
5. Work with cached variables

See **Data Files & External Storage** section for complete implementation details.

---

---

## Data Files & External Storage

### Overview
To minimize RAM usage, large data tables are stored as CSV files on SD card and loaded on-demand. This approach allows for:
- Easy external editing of game data
- No RAM overhead for unused data
- Simple balancing and content updates
- Potential for modding support

### Data File Strategy

**Access Pattern:**
```basic
1. Open data file (e.g., SHIPS.DAT)
2. Search for specific record by ID
3. Parse CSV into working variables
4. Close file
5. Use variables until next lookup needed
```

**Caching Strategy:**
- Frequently accessed data (current ship, current system) stays in BASIC variables
- Lookup only when changing context (buying new ship, jumping systems)
- Faction names/basic info loaded at game start, kept resident

### File Organization
```
/GAME/
  MAIN.BAS
  DOCKED.BAS
  SPACE.BAS
  COMBAT.BAS
  DATA/
    SHIPS.DAT       (60-80 records: 6-8 ships × 6-10 factions)
    SYSTEMS.DAT     (40-60 records)
    PLANETS.DAT     (60-150 records)
    EQUIPMENT.DAT   (20-40 records)
    FACTIONS.DAT    (6-10 records)
    COMMODITIES.DAT (10-20 records)
    MISSIONS.DAT    (mission templates)
  SAVES/
    GAMESTATE.DAT
```

### CSV Format Specification

**SHIPS.DAT Format:**
```csv
ID,NAME,FACTION,COST,CARGO,FUEL,ARMOR,SHIELDS,WEAPONS,ACCEL,TURN
1,SHUTTLE,1,15000,50,100,10,0,1,8,9
2,SCOUT,1,35000,20,150,15,10,2,12,11
3,COURIER,1,45000,30,200,20,25,2,10,10
```

**SYSTEMS.DAT Format:**
```csv
ID,NAME,X,Y,FACTION,TECH_LEVEL,GOVT,POPULATION
1,SOL,0,0,1,8,2,9
2,ALPHA CENTAURI,4,3,1,7,2,7
3,SIRIUS,8,-5,2,6,1,5
```

**FACTIONS.DAT Format:**
```csv
ID,NAME,HOMEWORLD,ALLIED_TO,ENEMY_OF,GOVT_TYPE
1,TERRAN FEDERATION,1,2,5,DEMOCRACY
2,MARS COLLECTIVE,3,1,5,REPUBLIC
3,OUTER RIM PIRATES,0,0,0,ANARCHY
```

**COMMODITIES.DAT Format:**
```csv
ID,NAME,BASE_PRICE,VARIANCE,ILLEGAL
1,FOOD,20,5,0
2,MINERALS,45,15,0
3,ELECTRONICS,120,30,0
4,WEAPONS,200,50,1
```

**EQUIPMENT.DAT Format:**
```csv
ID,NAME,TYPE,COST,TECH_REQ,STAT1,STAT2,STAT3
1,LASER MK I,WEAPON,2000,3,15,5,3
2,SHIELD GEN I,SHIELD,5000,4,50,5,0
3,ARMOR PLATE I,ARMOR,3000,2,10,0,0
```

### CSV Parsing in BASIC

**Generic CSV Parser:**
```basic
10000 REM === PARSE CSV LINE ===
10010 REM INPUT: L$ = CSV line
10020 REM OUTPUT: F$(1-N) = fields array
10030 C = 1: P = 1
10040 FOR I = 1 TO LEN(L$)
10050   IF MID$(L$,I,1) = "," THEN F$(C) = MID$(L$,P,I-P): C=C+1: P=I+1
10060 NEXT I
10070 F$(C) = MID$(L$,P) : REM Last field
10080 RETURN
```

**Find Record by ID Pattern:**
```basic
2000 REM === FIND SHIP BY ID ===
2010 REM INPUT: FIND_ID = ship to find
2020 REM OUTPUT: F$() array with ship data, or FOUND=0
2030 OPEN 1,8,2,"DATA/SHIPS.DAT,S,R"
2040 INPUT#1, L$ : REM Skip header
2050 FOUND = 0
2060 IF ST<>0 THEN 2120 : REM EOF check
2070 INPUT#1, L$
2080 GOSUB 10000 : REM Parse CSV
2090 IF VAL(F$(1)) = FIND_ID THEN FOUND=1: GOTO 2110
2100 GOTO 2060 : REM Keep searching
2110 CLOSE 1
2120 RETURN
```

**Usage Example:**
```basic
1000 REM Load player's ship data
1010 FIND_ID = PLAYER_SHIP_ID
1020 GOSUB 2000 : REM Find ship in SHIPS.DAT
1030 IF FOUND = 0 THEN PRINT "ERROR: SHIP NOT FOUND": END
1040 REM Cache in variables
1050 SHIP_NAME$ = F$(2)
1060 SHIP_FACTION = VAL(F$(3))
1070 SHIP_COST = VAL(F$(4))
1080 SHIP_CARGO = VAL(F$(5))
1090 REM ... etc
```

### Performance Characteristics

**Search Performance:**
- 60-80 ships: ~40 comparisons average (linear search)
- Estimated time: 100-200ms on X16 (imperceptible)
- No indexing needed at this scale

**Optimization Strategies if Needed:**
1. **Sorted files + binary search** - Reduces comparisons to ~6-7
2. **Index file** - Maps ID→byte offset for direct seek
3. **Faction-segregated files** - Search only relevant subset
4. **Caching** - Keep frequently accessed records in memory

**When to Optimize:**
- Only if file searches feel sluggish in playtesting
- If dataset exceeds ~100 records per file
- If same record looked up repeatedly (use caching first)

### Alternative Format: Fixed-Width

If CSV parsing proves too slow, fixed-width format is faster but less editable:
```
01SHUTTLE    00150000050010000100001080911
02SCOUT      00350000020015001000210121112
03COURIER    00450000030020002502210101013
```

**Parsing (faster - no loops):**
```basic
10000 REM === PARSE FIXED WIDTH ===
10010 SHIP_ID = VAL(MID$(L$,1,2))
10020 SHIP_NAME$ = MID$(L$,3,12)
10030 SHIP_COST = VAL(MID$(L$,15,8))
10040 SHIP_CARGO = VAL(MID$(L$,23,3))
10050 RETURN
```

**Recommendation:** Start with CSV, switch only if performance requires it.

---

## Data Structures

### Player Data Structure (~200 bytes)
```
Offset  Size  Description
------  ----  -----------
0       4     Credits (long int)
4       1     Current System ID
5       2     Current Day
7       1     Piloting Skill (1-10)
8       1     Combat Skill (1-10)
9       1     Engineering Skill (1-10)
10      1     Navigation Skill (1-10)
11      1     Leadership Skill (1-10)
12      2     Total XP
14      1     Ship Type ID
15      4     Faction Reputations (4 factions, -128 to +127 each)
19      20    Cargo array (10 commodities × 2 bytes each)
39      10    Active Mission IDs (up to 5 missions × 2 bytes)
49      ...   Additional player state
```

### Ship Data Structure (~50 bytes)
```
Offset  Size  Description
------  ----  -----------
0       1     Ship Type ID
1       2     Hull Current
3       2     Hull Max
5       2     Shields Current
7       2     Shields Max
9       1     Armor
10      1     Accuracy
11      1     Evasion
12      1     Speed
13      2     Power Current
15      2     Power Max
17      2     Fuel Current
19      2     Fuel Max
21      2     Cargo Current
23      2     Cargo Max
25      10    Equipment Flags (bit flags for installed equipment)
35      5     Weapon IDs (up to 5 weapons)
40      10    Upgrade Flags
```

### Crew Member Structure (~13 bytes each)
```
Offset  Size  Description
------  ----  -----------
0       1     Crew Position (0=Empty, 1=Pilot, 2=Gunner, etc.)
1       1     Primary Skill Level (1-10)
2       1     Secondary Skill Level (1-10)
3       2     XP
5       1     Level
6       2     Monthly Salary
8       1     Months Employed
9       1     Loyalty (0-3)
10      1     Morale (0-100)
11      20    Name (20 characters max)
```

### System Data Structure (~100 bytes)
```
Offset  Size  Description
------  ----  -----------
0       1     System ID
1       2     X Coordinate
3       2     Y Coordinate
5       1     Government Type
6       1     Tech Level
7       1     Population Level
8       10    Current Commodity Prices (10 commodities)
18      1     Services Flags (bitfield)
19      1     Faction Control
20      20    System Name
40      50    Description Text (pointer or short text)
90      10    Special Flags/Data
```

### Save Game Structure (~4-5KB)
```
Section           Size    Description
-------           ----    -----------
Player Data       200 B   Player stats, skills, XP
Ship Data         50 B    Current ship state
Crew Data         65 B    5 crew × 13 bytes
Escort Data       100 B   2 escorts × 50 bytes
Universe State    2048 B  System prices, flags (40 systems × ~50 bytes)
Mission State     500 B   Active missions, completion flags
Faction Data      100 B   Reputation, relationship state
Inventory         100 B   Equipment, cargo
Statistics        100 B   Kills, trades, jumps, etc.
Flags             500 B   Story progression, discoveries
```

---

## Development Roadmap

### Phase 1: Core Mechanics & Architecture (Pure BASIC)
**Goal:** Playable prototype with modular architecture

**Deliverables:**
- [ ] Build system setup (Makefile for assembling modules)
- [ ] Common library (COMMON.BAS with shared routines)
- [ ] State persistence (SAVE_STATE / LOAD_STATE routines)
- [ ] CSV data file system (parser, loaders)
- [ ] Create initial data files (5 ships, 5 systems, 3 commodities)
- [ ] Navigation system between test systems
- [ ] Simple trading (buy/sell 3-4 commodities)
- [ ] Basic turn-based combat (1v1)
- [ ] Player stats and leveling
- [ ] Basic UI screens (station, navigation, trading)
- [ ] Program module transitions (MAIN→DOCKED→SPACE)

**Estimated Effort:** 5-7 weeks

### Phase 2: Content Expansion (Pure BASIC)
**Goal:** Full game content in data files

**Deliverables:**
- [ ] Complete galaxy data (30-40 systems in SYSTEMS.DAT)
- [ ] All factions (6-10 in FACTIONS.DAT)
- [ ] All ships (60-80 in SHIPS.DAT: 6-8 per faction)
- [ ] All equipment types (20-40 in EQUIPMENT.DAT)
- [ ] All commodities (10-20 in COMMODITIES.DAT)
- [ ] Complete pricing and trade system
- [ ] Crew system fully implemented
- [ ] Escort hiring and management
- [ ] Multi-ship combat (up to 7 ships)
- [ ] Mission system (3 tiers, stored in MISSIONS.DAT)
- [ ] Faction reputation system
- [ ] Complete UI screens (all modules)
- [ ] Dynamic events system

**Estimated Effort:** 8-12 weeks

### Phase 3: Faction Storylines (Pure BASIC)
**Goal:** Replayability through story content

**Deliverables:**
- [ ] 3-4 faction story arcs (6-8 missions each)
- [ ] Branching mission paths
- [ ] Faction-specific ships and equipment
- [ ] Special/hidden systems
- [ ] Dynamic events system
- [ ] Contraband and smuggling
- [ ] Bounty system

**Estimated Effort:** 6-8 weeks

### Phase 4: Polish & Optimization
**Goal:** Professional presentation

**Deliverables:**
- [ ] Graphics improvements (PETSCII art, colors)
- [ ] Assembly helpers for bottlenecks
  - [ ] Banking routines
  - [ ] Combat calculation
  - [ ] Graphics drawing
- [ ] Sound effects (if desired)
- [ ] Balance testing
- [ ] Bug fixing
- [ ] Performance optimization

**Estimated Effort:** 4-6 weeks

### Phase 5: Extended Content (Optional)
**Goal:** Additional gameplay depth

**Possible Features:**
- [ ] More factions
- [ ] Larger galaxy
- [ ] Ship customization/painting
- [ ] Multiplayer trading (if feasible)
- [ ] Random universe generation mode
- [ ] Challenge modes

**Estimated Effort:** Variable

---

## Technical Notes

### CSV Data File Example
```basic
REM === EXAMPLE: Load a ship from SHIPS.DAT ===

1000 REM Request ship ID 5
1010 FIND_ID = 5
1020 GOSUB 2000: REM Find ship
1030 IF FOUND = 0 THEN PRINT "SHIP NOT FOUND": END
1040 REM
1050 REM Data now in F$() array
1060 SHIP_NAME$ = F$(2)
1070 SHIP_COST = VAL(F$(4))
1080 SHIP_CARGO = VAL(F$(5))
1090 PRINT "LOADED: ";SHIP_NAME$
1100 END

2000 REM === FIND SHIP BY ID ===
2010 OPEN 1,8,2,"DATA/SHIPS.DAT,S,R"
2020 INPUT#1, L$ : REM Skip header
2030 FOUND = 0
2040 IF ST<>0 THEN 2090
2050 INPUT#1, L$
2060 GOSUB 10000 : REM Parse CSV
2070 IF VAL(F$(1)) = FIND_ID THEN FOUND=1: GOTO 2090
2080 GOTO 2040
2090 CLOSE 1
2100 RETURN

10000 REM === PARSE CSV LINE ===
10010 REM INPUT: L$
10020 REM OUTPUT: F$(1-N)
10030 DIM F$(20): C=1: P=1
10040 FOR I=1 TO LEN(L$)
10050   IF MID$(L$,I,1)="," THEN F$(C)=MID$(L$,P,I-P): C=C+1: P=I+1
10060 NEXT I
10070 F$(C) = MID$(L$,P)
10080 RETURN
```

### State Persistence Example
```basic
8000 REM === SAVE STATE ===
8010 OPEN 1,8,2,"SAVES/GAMESTATE.DAT,S,W"
8020 PRINT#1, CREDITS
8030 PRINT#1, CURRENT_SYSTEM
8040 PRINT#1, CURRENT_DAY
8050 PRINT#1, PILOT_SKILL
8060 PRINT#1, COMBAT_SKILL
8070 PRINT#1, ENGINEER_SKILL
8080 PRINT#1, NAV_SKILL
8090 PRINT#1, LEADER_SKILL
8100 REM ... continue for all state variables
8200 CLOSE 1
8210 RETURN

9000 REM === LOAD STATE ===
9010 OPEN 1,8,2,"SAVES/GAMESTATE.DAT,S,R"
9020 INPUT#1, CREDITS
9030 INPUT#1, CURRENT_SYSTEM
9040 INPUT#1, CURRENT_DAY
9050 INPUT#1, PILOT_SKILL
9060 INPUT#1, COMBAT_SKILL
9070 INPUT#1, ENGINEER_SKILL
9080 INPUT#1, NAV_SKILL
9090 INPUT#1, LEADER_SKILL
9100 REM ... continue for all state variables
9200 CLOSE 1
9210 RETURN
```

### Combat Resolution BASIC Pseudocode
```basic
9000 REM === COMBAT TURN ===
9010 REM
9020 REM Calculate to-hit chance
9030 HITCHANCE = PLAYERACCURACY - ENEMYEVASION + WEAPONBONUS + SKILLBONUS
9040 REM
9050 REM Roll d100
9060 ROLL = INT(RND(1)*100)
9070 REM
9080 IF ROLL <= HITCHANCE THEN GOSUB 9500: REM Hit!
9090 IF ROLL > HITCHANCE THEN PRINT "MISS!": RETURN
9100 REM
9500 REM === HIT ROUTINE ===
9510 DAMAGE = WEAPONDAMAGE + INT(RND(1)*10) - 5: REM ±5 variance
9520 IF ENEMYSHIELDS > 0 THEN ENEMYSHIELDS = ENEMYSHIELDS - DAMAGE
9530 IF ENEMYSHIELDS < 0 THEN ENEMYHULL = ENEMYHULL + ENEMYSHIELDS: ENEMYSHIELDS = 0
9540 IF ENEMYSHIELDS = 0 THEN ENEMYHULL = ENEMYHULL - (DAMAGE - ENEMYARMOR)
9550 PRINT "HIT! ";DAMAGE;" DAMAGE"
9560 RETURN
```

### Screen Drawing Optimization
```basic
REM MINIMIZE PRINT STATEMENTS
REM Bad: Multiple PRINTs
PRINT "╔"
PRINT "║"
PRINT "╗"

REM Good: Single PRINT with concatenation
PRINT "╔════════════════════╗"

REM Better: Pre-build strings
A$ = "╔════════════════════╗"
PRINT A$
```

---

## Design Principles

### Core Values
1. **Depth without Complexity:** Systems interact meaningfully but rules are clear
2. **Player Agency:** Multiple valid approaches to every situation
3. **Consequence:** Choices matter and affect future options
4. **Respect Player Time:** Clear feedback, no grinding requirements
5. **8-bit Authenticity:** Embrace constraints, don't fight them

### Balancing Guidelines
- Early game: Forgiving, tutorial-like
- Mid game: Strategic choices matter
- Late game: Mastery and optimization rewarded
- No dead ends: Player can always recover from mistakes
- Difficulty through interesting choices, not stat checks

### Content Philosophy
- Every system should feel distinct
- Every faction should offer unique gameplay
- Every ship should have a purpose
- Every upgrade should enable new strategies
- Every mission should tell a story

---

## Future Considerations

### Potential Expansions
- **Planetary Landing:** Visit surfaces, cities, markets
- **Fleet Command:** More than 2 escorts
- **Economy Simulation:** More dynamic market system
- **Procedural Events:** Greater variety in random encounters
- **Modding Support:** External data files for systems/missions

### Technical Improvements
- **Graphics Mode:** Use VERA bitmap/tile modes
- **Music:** Background music via PSG
- **Networking:** Multi-player trading via serial/network
- **Assembly Rewrite:** Full ML version for performance

### Accessibility
- **Difficulty Modes:** Easy/Normal/Hard settings
- **Tutorial System:** Optional guided first hour
- **Save Anywhere:** Not just at stations
- **Quick Save:** Rapid save/load for experimentation

---

## Appendices

### A. Glossary
- **Banking:** Switching between 8KB pages of extended RAM
- **PETSCII:** PET Standard Code of Information Interchange (C64/X16 character set)
- **VERA:** Video Enhanced Retro Adapter (X16's video chip)
- **d100:** 100-sided die roll (0-99 or 1-100)
- **Hex:** Hexagon, unit of tactical combat grid

### B. References
- Commander X16 documentation: https://github.com/X16Community/x16-docs
- BASIC programming guide: X16 BASIC reference
- Escape Velocity series: Original inspiration
- Elite: Classic space trading game

### C. Credits
- Design: [Your Name]
- Platform: Commander X16 project
- Inspiration: Escape Velocity (Ambrosia Software)

---

**Document Version:** 0.1  
**Last Updated:** November 21, 2024  
**Status:** Initial Design Phase  
**Next Review:** After Phase 1 prototype completion

---

*This is a living document. Update as design evolves through development.*
