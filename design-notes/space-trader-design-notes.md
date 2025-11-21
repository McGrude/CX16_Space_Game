# Space Trader Game Design Document
**Platform:** Commander X16  
**Genre:** Turn-Based Space Trading/Combat RPG  
**Inspiration:** Escape Velocity series (Ambrosia Software)  
**Version:** 0.2 - Galaxy & Factions Update  
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
16. [Galaxy Data](#galaxy-data)
17. [Faction Details](#faction-details)

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
A sandbox space exploration and trading game with RPG elements, turn-based tactical combat, and faction-based storylines. Players start with a small ship in the Sol system and build their reputation, wealth, and fleet through trading, combat, and missions across 92 real star systems within 50 light years of Earth.

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
- **Authentic setting:** Real stellar neighborhood with actual star names and positions
- **8-bit appropriate:** Design within technical constraints

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

### Overview
The stellar neighborhood is divided among 9 factions: 5 major political powers with territory, 2 minor factions controlling key systems, and 2 mission-only organizations.

### Major Factions (Territorial Control)

#### 1. Terran Hegemony
**Capital:** Sol  
**Territory:** 20 systems, 32 ports  
**Government:** Authoritarian colonial empire

**Description:** 
The Terran Hegemony is a protectionist, militaristic human-supremacist government centered on Earth (Sol). They control the core systems of human space through military force and colonial administration. The Hegemony views itself as the rightful ruler of humanity and is deeply suspicious of AI technology and alien civilizations.

**Traits:** Colonial, militaristic, protectionist, authoritarian, xenophobic

**Technology Focus:**
- Heavy shields and armor
- Energy weapons (lasers, plasma)
- Military-grade equipment
- Patrol and battleship designs

**Relations:**
- **At WAR with:** Free Systems Coalition (-50)
- **Cold War with:** Frontier Alliance (-20)
- **Hostile to:** Velanthi Commonwealth (-40), Nexus Collective (-30)
- **Enemy of:** Crimson Cartel (-60)
- **Allied with:** Nova Mining Guild (+40)

#### 2. Free Systems Coalition
**Capital:** Tau Ceti  
**Territory:** 15 systems, 24 ports  
**Government:** Democratic federation

**Description:**
The Free Systems Coalition is a rebel independence movement fighting to break free from Hegemony control. They advocate for democratic governance, cultural diversity, and individual liberty. The Coalition is more open to alien contact and cautiously accepting of AI technology, though internal debate on these issues continues.

**Traits:** Rebel, democratic, independent, freedom-focused, diverse

**Technology Focus:**
- Fast, agile ships
- Missile systems and torpedoes
- Guerrilla warfare equipment
- Stealth and evasion tech

**Relations:**
- **At WAR with:** Terran Hegemony (-50)
- **Friendly with:** Frontier Alliance (+30)
- **Curious about:** Velanthi Commonwealth (+10)
- **Uneasy with:** Nexus Collective (-10)
- **Complicated with:** Crimson Cartel (-15)
- **Neutral with:** Nova Mining Guild (0)

#### 3. Frontier Alliance
**Capital:** Gliese 163  
**Territory:** 24 systems, 33 ports (largest territory)  
**Government:** Loose confederation

**Description:**
The Frontier Alliance is a pragmatic association of remote colonies focused on survival and self-sufficiency. They maintain neutrality in the Hegemony-Coalition war, though they sympathize with the Coalition's cause. Frontier systems trade with anyone and prioritize practical considerations over ideology.

**Traits:** Neutral, remote, independent, survivalist, pragmatic

**Technology Focus:**
- Utilitarian designs
- Mining and industrial equipment
- Long-range fuel systems
- Reliable, repairable tech

**Relations:**
- **Friendly with:** Free Systems Coalition (+30), Nova Mining Guild (+20)
- **Cold with:** Terran Hegemony (-20)
- **Cautious with:** Velanthi Commonwealth (+5)
- **Tolerates:** Crimson Cartel (-5)
- **Neutral with:** Nexus Collective (0)

#### 4. The Nexus Collective
**Capital:** Sirius  
**Territory:** 9 systems, 16 ports (scattered, non-contiguous)  
**Government:** Technocratic AI-human synthesis

**Description:**
The Nexus Collective is a mysterious technocratic society where humans have merged with AI through cybernetic augmentation. They display hive-mind tendencies and pursue goals that other factions find difficult to understand. The Hegemony fears them as an existential threat to human individuality.

**Traits:** Technocratic, AI, cyberpunk, mysterious, transhumanist

**Technology Focus:**
- Advanced AI systems
- Cybernetic implants
- Drone technology
- Experimental weapons
- Neural interfaces

**Relations:**
- **Fascinated by:** Velanthi Commonwealth (+25)
- **Partners with:** Nova Mining Guild (+35)
- **Views as opportunity:** Crimson Cartel (+10)
- **Suspected by:** Terran Hegemony (-30), Free Systems Coalition (-10)
- **Neutral with:** Frontier Alliance (0)

#### 5. Velanthi Commonwealth
**Capital:** Vega  
**Territory:** 7 systems, 8 ports (isolated, distant)  
**Government:** Alien civilization

**Description:**
The Velanthi are an enigmatic alien species with technology that rivals or exceeds humanity's. They are rarely encountered and their motives remain unclear. The Velanthi view the Hegemony's xenophobia as primitive and are curious about human diversity in the Coalition and Nexus.

**Traits:** Alien, advanced, mysterious, rare, non-interventionist

**Technology Focus:**
- Exotic alien technology
- Unique propulsion systems
- Unknown weapon types
- Advanced sensors
- Biological tech integration

**Relations:**
- **Fascinated by:** Nexus Collective (+25)
- **Hostile to:** Terran Hegemony (-40)
- **Curious about:** Free Systems Coalition (+10)
- **Cautious with:** Frontier Alliance (+5)
- **Disdains:** Crimson Cartel (-25)
- **Indifferent to:** Nova Mining Guild (0)

### Minor Factions

#### 6. Crimson Cartel
**Home System:** Wolf 359  
**Territory:** 2 systems (Wolf 359, Luyten 726-8)  
**Type:** Pirate confederation

**Description:**
An organized crime syndicate controlling key trade routes. They engage in piracy, smuggling, and extortion. The Cartel is the enemy of the Hegemony and tolerated (or secretly supported) by some Frontier and Coalition systems.

**Relations:**
- Enemy of Hegemony (-60), Guild (-30)
- Complicated with Coalition (-15)
- Tolerated by Frontier (-5)
- Opportunity for Nexus (+10)
- Disdained by Velanthi (-25)

#### 7. Nova Mining Guild
**Home System:** Epsilon Eridani  
**Territory:** 2 systems (Epsilon Eridani, Lacaille 9352)  
**Type:** Corporate mining monopoly

**Description:**
A powerful corporation controlling resource-rich systems. They supply minerals and rare materials to multiple factions, maintaining a delicate neutrality while being formally allied with the Hegemony.

**Relations:**
- Allied with Hegemony (+40)
- Partners with Nexus (+35)
- Cooperative with Frontier (+20)
- Neutral with Coalition (0)
- Extorted by Cartel (-30)

### Mission-Only Factions

#### 8. Free Traders Union
**Type:** Merchant guild (no territory)

**Description:**
A galaxy-spanning merchant organization offering trade missions, commodity contracts, and market information. They maintain strict neutrality and deal with all factions.

**Gameplay Role:**
- Trade missions and contracts
- Market intelligence
- Cargo transport jobs
- No reputation effects on other factions

#### 9. Archaeological Concord
**Type:** Academic organization (no territory)

**Description:**
A multi-species academic society dedicated to discovering and preserving ancient artifacts and historical sites throughout the galaxy.

**Gameplay Role:**
- Artifact recovery missions
- Archaeological site surveys
- Research expeditions
- Ancient technology quests

### Reputation System

**Scale:** -100 (Hostile) to +100 (Allied)

| Range | Status | Effects |
|-------|--------|---------|
| -100 to -25 | **Hostile** | Attacked on sight, can't dock, bounty hunters, no trade |
| -24 to +24 | **Neutral** | Basic trading, limited missions, standard prices |
| +25 to +74 | **Friendly** | Better equipment, faction missions, 10% discount, combat assistance |
| +75 to +100 | **Allied** | Unique ships, story missions, 20% discount, restricted system access |

### Reputation Changes

**Actions Affecting Reputation:**
```
POSITIVE:
+ Complete faction mission: +5 to +15
+ Destroy faction enemies: +2 to +10
+ Trade regularly: +1 per transaction
+ Protect faction ships: +5

NEGATIVE:
- Attack faction ships: -10 to -25
- Fail faction mission: -5 to -15
- Trade with enemies: -2 to -5
- Illegal actions in faction space: -10 to -30

CROSS-FACTION EFFECTS:
Example: Destroying Hegemony ship
  - Terran Hegemony: -15
  - Free Systems Coalition: +10
  - Frontier Alliance: +2
  - Nexus Collective: 0
  - Velanthi Commonwealth: +5
```

### Contested Systems

**5 systems are actively contested** between Terran Hegemony and Free Systems Coalition, representing active war zones with increased military presence and combat encounters.

**13 independent systems** remain unaligned, offering neutral trading posts and refuge for those wanted by major factions.

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

Travel Time (Days) = ceil(Distance / 10) + 1

Note: Distance compression factor of 10 applied to real stellar distances

Example:
Sol (0,0) → Alpha Centauri (-12,-3)
Distance = sqrt(144 + 9) = 12.4 compressed units
Travel Time = ceil(12.4 / 10) + 1 = 3 days
```

**Fuel Consumption:**
```
Fuel Cost = Distance × 2 units

Adjacent system: ~6-10 fuel units
Medium jump: ~15-30 fuel units
Long haul: ~50-100 fuel units

Fuel Price: 10 credits per unit
Tank Capacity: 50-200 units (ship dependent)
```

**Navigation Upgrades:**

| Equipment | Effect | Cost |
|-----------|--------|------|
| Standard Nav | Distance / 10 + 1 days | Included |
| Nav Computer I | Distance / 10 + 0.5 days | 5,000 cr |
| Nav Computer II | Distance / 10 × 0.9 + 0.5 days | 15,000 cr |
| Advanced Nav | Distance / 10 × 0.75 days (min 1) | 35,000 cr |

**Navigator Crew Bonus:**
- Navigation skill 10: -10% travel time

### Travel Interface

**Pre-Jump Display:**
```
Current System: Sol
Destination: Tau Ceti
Distance: 11.9 compressed units
Travel Time: 3 days
Fuel Required: 24 units
Arrival Date: Day 136

Current Day: Day 133
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

**Type:** Real stellar neighborhood  
**Size:** 92 star systems within ~50 light years of Sol  
**Coordinates:** Cartesian grid (-130 to +130 on compressed scale)  
**Total Ports:** 136 docking locations across all systems

**Design Philosophy:**
- Based on actual astronomical data
- Real star names and spectral types
- Compressed distances (10x factor) for gameplay
- Strategic positioning creates natural trade routes
- Faction territories based on stellar geography

### System Types

**Core Systems (Hegemony Space):**
- Close to Sol (< 30 units)
- High tech level (7-10)
- Heavy patrol presence
- All services available
- Higher prices, safer

**Mid-Range Systems (Coalition/Contested):**
- 30-60 units from Sol
- Medium tech level (5-8)
- Variable security
- Most services available
- Moderate prices, some risk

**Frontier Systems (Alliance/Remote):**
- 60+ units from Sol
- Low to medium tech (3-6)
- Light or no patrols
- Basic services only
- Lower prices, dangerous

**Scattered Systems (Nexus Territory):**
- Non-contiguous locations
- High tech (8-10)
- Advanced/unusual services
- Experimental equipment
- Mysterious

**Distant Systems (Velanthi Territory):**
- Isolated, far from Sol
- Very high tech (9-10)
- Alien technology available
- Rare encounters
- Unknown risks

### System Spectral Distribution

| Type | Count | Description | Color |
|------|-------|-------------|-------|
| M-type | 63 | Red dwarfs (most common) | Red |
| K-type | 13 | Orange stars | Orange |
| G-type | 9 | Yellow, Sun-like stars | Yellow |
| F-type | 2 | Yellow-white stars | Yellow-white |
| A-type | 4 | White stars (Sirius, Vega, Altair, Fomalhaut) | White |
| D-type | 1 | White dwarf (Van Maanen's Star) | White |

**Note:** G-type systems have slightly higher chance of multiple ports due to habitability.

### Port Types

Ports are docking locations where players can trade, repair, hire crew, and accept missions.

**Port Categories:**
1. **Planet** - Terrestrial world with surface settlements
2. **Moon** - Lunar base or settlement
3. **Space Station** - Orbital platform
4. **Mining Colony** - Resource extraction facility
5. **Trade Hub** - Commercial center
6. **Research Outpost** - Scientific facility
7. **Military Base** - Faction military installation
8. **Orbital Platform** - Industrial or residential orbital

**Port Distribution:**
- 66 systems (72%) have 1 port
- 16 systems (17%) have 2 ports
- 10 systems (11%) have 3 ports

### Notable Systems

**Sol (0, 0)** - Terran Hegemony Capital
- Starting location
- 1 port: Sol Prime
- All services available
- Highest security

**Alpha Centauri (-12, -3)** - Hegemony Territory
- Nearest neighbor to Sol
- 3 ports: Alpha Centauri Prime, Alpha, Beta
- Major trade hub
- 4.37 light years from Sol (real distance)

**Tau Ceti (38, -9)** - Free Systems Coalition Capital
- Coalition headquarters
- 1 port: Tau Ceti Prime
- Rebel shipyards
- 11.89 light years from Sol

**Sirius (-29, 10)** - Nexus Collective Capital
- AI-human hybrid society
- 1 port: Sirius Orbital
- Advanced technology
- 8.59 light years from Sol (brightest star in Earth's sky)

**Vega (-52, 65)** - Velanthi Commonwealth Capital
- Alien civilization home
- 1 port: Vega Station
- Exotic alien tech
- 25.04 light years from Sol

**Wolf 359 (24, 3)** - Crimson Cartel Base
- Pirate haven
- 1 port: Wolf 359 Station
- Black market
- 7.78 light years from Sol

**Epsilon Eridani (9, -32)** - Nova Mining Guild HQ
- Mining operations center
- 1 port: Epsilon Eridani Prime
- Industrial equipment
- 10.52 light years from Sol

**Other Notable Systems:**
- **Barnard's Star** (20, -2) - 3 ports, Hegemony military presence
- **Procyon** (-32, 6) - Famous star, Hegemony control
- **61 Cygni** (33, 40) - Binary system, Coalition territory
- **Gliese 163** (135, -68) - Distant, Frontier Alliance capital
- **Altair** (-38, 41) - Bright star, Coalition space
- **Fomalhaut** (31, -76) - 2 ports, southern frontier

### System Data Structure

**Per System (~100 bytes):**
```
- System ID: 1 byte
- Name: 20 bytes
- Coordinates X,Y: 4 bytes (2 each)
- Faction Control: 1 byte
- Faction Strength: 1 byte (0-100)
- Tech Level: 1 byte
- Spectral Type: 4 bytes
- Real Distance (light years): 2 bytes
- Port Count: 1 byte
- Commodity Prices: 10 bytes (one per commodity)
- Station Services Flags: 1 byte
- Special Flags: 1 byte (contested, capital, etc.)
- Description pointer: 2 bytes
```

**Per Port (~30 bytes):**
```
- Port ID: 1 byte
- System ID: 1 byte
- Name: 20 bytes
- Type: 1 byte (Planet, Moon, Station, etc.)
- Services Available: 1 byte (bitfield)
- Tech Level: 1 byte
```

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
- Faction Colors: Match faction palette

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

See **Data Files & External Storage** section in original document for complete implementation details.

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
15      20    Faction Reputations (10 factions × 2 bytes each, -100 to +100)
35      20    Cargo array (10 commodities × 2 bytes each)
55      10    Active Mission IDs (up to 5 missions × 2 bytes)
65      ...   Additional player state
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
1       2     X Coordinate (compressed)
3       2     Y Coordinate (compressed)
5       1     Faction Control ID
6       1     Faction Strength (0-100)
7       1     Tech Level
8       4     Spectral Type (string)
9       2     Real Distance (light years × 10)
11      1     Port Count
12      10    Current Commodity Prices (10 commodities)
22      1     Services Flags (bitfield)
23      1     Special Flags (contested, capital, etc.)
24      20    System Name
44      50    Additional data
```

### Save Game Structure (~4-5KB)
```
Section           Size    Description
-------           ----    -----------
Player Data       200 B   Player stats, skills, XP
Ship Data         50 B    Current ship state
Crew Data         65 B    5 crew × 13 bytes
Escort Data       100 B   2 escorts × 50 bytes
Faction Rep       20 B    10 factions × 2 bytes
Cargo             40 B    10-20 commodity quantities
Mission State     200 B   Active missions, completion flags
Discovered Systems 12 B   92 systems as bitfield
Statistics        100 B   Kills, trades, jumps, etc.
Flags             500 B   Story progression, special events
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
- [ ] Create initial data files (10 test systems, 5 ships, 5 commodities)
- [ ] Navigation system between test systems
- [ ] Simple trading (buy/sell 5 commodities)
- [ ] Basic turn-based combat (1v1)
- [ ] Player stats and leveling
- [ ] Basic UI screens (station, navigation, trading)
- [ ] Program module transitions (MAIN→DOCKED→SPACE)

**Estimated Effort:** 5-7 weeks

### Phase 2: Content Expansion (Pure BASIC)
**Goal:** Full galaxy content in data files

**Deliverables:**
- [ ] Complete galaxy data (92 systems in SYSTEMS.DAT)
- [ ] All 136 ports with names and types
- [ ] All factions (9 factions in FACTIONS.DAT)
- [ ] Faction territory assignments
- [ ] All ships (60-80 in SHIPS.DAT: 6-8 per faction)
- [ ] All equipment types (30-40 in EQUIPMENT.DAT)
- [ ] All commodities (10 in COMMODITIES.DAT)
- [ ] Complete pricing and trade system
- [ ] Crew system fully implemented
- [ ] Escort hiring and management
- [ ] Multi-ship combat (up to 7 ships)
- [ ] Mission system (3 tiers)
- [ ] Faction reputation system
- [ ] Complete UI screens (all modules)
- [ ] Dynamic events system

**Estimated Effort:** 8-12 weeks

### Phase 3: Faction Storylines (Pure BASIC)
**Goal:** Replayability through story content

**Deliverables:**
- [ ] 5 major faction story arcs (6-8 missions each)
- [ ] Branching mission paths
- [ ] Faction-specific ships and equipment
- [ ] Special/hidden systems
- [ ] Contested system mechanics
- [ ] Contraband and smuggling
- [ ] Bounty system
- [ ] Cross-faction reputation effects

**Estimated Effort:** 8-10 weeks

### Phase 4: Polish & Optimization
**Goal:** Professional presentation

**Deliverables:**
- [ ] Graphics improvements (PETSCII art, colors, faction emblems)
- [ ] Assembly helpers for bottlenecks
  - [ ] Banking routines
  - [ ] Combat calculation
  - [ ] Graphics drawing
- [ ] Sound effects (if desired)
- [ ] Balance testing (economy, combat, progression)
- [ ] Bug fixing
- [ ] Performance optimization
- [ ] Galaxy map visualization

**Estimated Effort:** 4-6 weeks

### Phase 5: Extended Content (Optional)
**Goal:** Additional gameplay depth

**Possible Features:**
- [ ] Minor faction storylines
- [ ] More ship classes
- [ ] Ship customization/painting
- [ ] Hidden alien artifacts
- [ ] Procedural mission generation
- [ ] Challenge modes
- [ ] New Game+ with increased difficulty

**Estimated Effort:** Variable

---

## Galaxy Data

### Complete System List

The game features **92 real star systems** based on our actual stellar neighborhood within ~50 light years of Sol. Systems use compressed coordinates (10x factor) to fit the playable game grid.

**System Distribution by Faction:**
- **Terran Hegemony:** 20 systems, 32 ports
- **Free Systems Coalition:** 15 systems, 24 ports
- **Frontier Alliance:** 24 systems, 33 ports
- **The Nexus Collective:** 9 systems, 16 ports
- **Velanthi Commonwealth:** 7 systems, 8 ports
- **Crimson Cartel:** 2 systems, 2 ports
- **Nova Mining Guild:** 2 systems, 4 ports
- **Independent:** 13 systems, 17 ports

**Notable System Examples:**

```
SOL (Terran Hegemony Capital)
Position: (0, 0)
Real Distance: 0.00 light years
Spectral Type: G2V
Ports: 1 - Sol Prime (Moon)
Description: Earth's home system and heart of the Terran Hegemony. 
Starting location for all players. Maximum security and all services.

ALPHA CENTAURI (Terran Hegemony)
Position: (-12, -3)
Real Distance: 4.37 light years
Spectral Type: G2V/K1V (binary)
Ports: 3 - Alpha Centauri Prime (Mining Colony), Alpha (Space Station), 
       Beta (Military Base)
Description: Humanity's first interstellar colony and major trade hub. 
Triple star system with extensive orbital infrastructure.

TAU CETI (Free Systems Coalition Capital)
Position: (38, -9)
Real Distance: 11.89 light years
Spectral Type: G8V
Ports: 1 - Tau Ceti Prime (Planet)
Description: Coalition headquarters and symbol of independence. 
Home to rebel shipyards and democratic government.

SIRIUS (Nexus Collective Capital)
Position: (-29, 10)
Real Distance: 8.59 light years
Spectral Type: A1V (brightest star in Earth's sky)
Ports: 1 - Sirius Orbital (Orbital Platform)
Description: AI-human synthesis civilization. Advanced cybernetic 
technology and mysterious research facilities.

VEGA (Velanthi Commonwealth Capital)
Position: (-52, 65)
Real Distance: 25.04 light years
Spectral Type: A0V
Ports: 1 - Vega Station (Space Station)
Description: Alien civilization's primary contact point with humanity. 
Exotic technology and rare encounters.

WOLF 359 (Crimson Cartel)
Position: (24, 3)
Real Distance: 7.78 light years
Spectral Type: M6V
Ports: 1 - Wolf 359 Station (Space Station)
Description: Notorious pirate haven. Black market and smuggling hub.

EPSILON ERIDANI (Nova Mining Guild)
Position: (9, -32)
Real Distance: 10.52 light years
Spectral Type: K2V
Ports: 1 - Epsilon Eridani Prime (Mining Colony)
Description: Guild headquarters with extensive asteroid mining operations.

BARNARD'S STAR (Terran Hegemony)
Position: (20, -2)
Real Distance: 5.96 light years
Spectral Type: M4V
Ports: 3 - Multiple military and trade facilities
Description: Major Hegemony military outpost near Sol.

PROCYON (Terran Hegemony)
Position: (-32, 6)
Real Distance: 11.46 light years
Spectral Type: F5IV-V
Ports: 1 - Procyon Prime (Trade Hub)
Description: Important Hegemony trade route junction.

61 CYGNI (Free Systems Coalition)
Position: (33, 40)
Real Distance: 11.41 light years
Spectral Type: K5V/K7V (binary)
Ports: 2 - Coalition colonies
Description: Strategic Coalition system on Hegemony border.

GLIESE 163 (Frontier Alliance Capital)
Position: (135, -68) [Note: Distant frontier location]
Real Distance: 49.40 light years
Spectral Type: M3.5V
Ports: 1 - Gliese 163 Station (Space Station)
Description: Remote Frontier Alliance capital. Independent and pragmatic.
```

**Spectral Type Distribution:**
- M-type (Red Dwarfs): 63 systems - Most common, small cool stars
- K-type (Orange): 13 systems - Medium-sized stars
- G-type (Yellow, Sun-like): 9 systems - Similar to Sol
- F-type (Yellow-white): 2 systems - Hotter than Sun
- A-type (White): 4 systems - Large, bright stars (Sirius, Vega, Altair, Fomalhaut)
- D-type (White Dwarf): 1 system - Stellar remnant (Van Maanen's Star)

**Port Distribution:**
- 1 port: 66 systems (72%)
- 2 ports: 16 systems (17%)
- 3 ports: 10 systems (11%)

**Complete galaxy data** is available in SYSTEMS.DAT and PORTS.DAT files. See Development Roadmap for implementation details.

---

## Faction Details

### Diplomatic Relations Matrix

Cross-faction reputation modifiers when taking actions:

| Action | TH | FSC | FA | NC | VC | CC | NMG |
|--------|----|----|----|----|----|----|-----|
| **Attack Hegemony ship** | -15 | +10 | +2 | 0 | +5 | +3 | -5 |
| **Attack Coalition ship** | +10 | -15 | -5 | -2 | -3 | 0 | 0 |
| **Attack Nexus ship** | +5 | +2 | 0 | -15 | -5 | 0 | -10 |
| **Attack Velanthi ship** | +3 | -5 | -3 | -5 | -20 | 0 | 0 |
| **Attack Cartel ship** | +5 | +2 | +1 | 0 | +1 | -15 | +3 |
| **Complete Hegemony mission** | +10 | -5 | -2 | -3 | -5 | -5 | +2 |
| **Complete Coalition mission** | -5 | +10 | +3 | -1 | +2 | +1 | 0 |
| **Trade at Guild station** | +1 | 0 | +1 | +1 | 0 | -1 | +5 |
| **Trade with Nexus** | -5 | -1 | 0 | +3 | +1 | 0 | +1 |

**Legend:**
- TH = Terran Hegemony
- FSC = Free Systems Coalition  
- FA = Frontier Alliance
- NC = Nexus Collective
- VC = Velanthi Commonwealth
- CC = Crimson Cartel
- NMG = Nova Mining Guild

### Faction-Specific Equipment

**Terran Hegemony:**
- Hegemony Battlecruiser (requires Allied status)
- Heavy Plasma Lance (energy weapon)
- Imperial Shield Array (superior shields)
- Military-grade armor plating

**Free Systems Coalition:**
- Coalition Interceptor (fast, agile)
- Freedom Fighter Missiles (high damage)
- Stealth Field Generator (evasion bonus)
- Democratic governance provides crew morale bonus

**Frontier Alliance:**
- Frontier Hauler (massive cargo capacity)
- Salvage equipment (recover more from wrecks)
- Long-range fuel tanks
- Survival systems (repair bonuses)

**The Nexus Collective:**
- Nexus Cruiser (AI-assisted)
- Neural Interface (skill bonuses)
- Drone Bay (automated defenses)
- Quantum Computing Core (targeting bonus)

**Velanthi Commonwealth:**
- Velanthi Starcruiser (alien design)
- Exotic Beam Weapons (unique damage type)
- Alien Shield Matrix (regenerates faster)
- Biological computer (mysterious bonuses)

### Mission Examples by Faction

**Hegemony - Tier 1 (Neutral):**
- "Transport military supplies to Alpha Centauri"
- "Patrol Sol system and report suspicious activity"
- "Deliver diplomatic message to Procyon"

**Hegemony - Tier 3 (Allied):**
- "Infiltrate Coalition base and steal battle plans"
- "Lead assault on contested system"
- "Escort Hegemony Admiral through war zone"

**Coalition - Tier 1 (Neutral):**
- "Deliver medical supplies to frontier colony"
- "Courier encrypted messages to 61 Cygni"
- "Scout Hegemony patrol routes"

**Coalition - Tier 3 (Allied):**
- "Sabotage Hegemony weapons facility"
- "Rally independent systems to Coalition cause"
- "Rescue Coalition leader from Hegemony prison"

**Nexus - Tier 2 (Friendly):**
- "Test experimental AI combat system"
- "Retrieve damaged drone from deep space"
- "Transport cybernetic components to Sirius"

**Velanthi - Tier 3 (Allied):**
- "First contact with unknown alien species"
- "Investigate ancient alien artifact"
- "Defend Velanthi ship from Hegemony attack"

**Cartel (Criminal Missions):**
- "Smuggle contraband through Hegemony blockade"
- "Raid Guild mining convoy"
- "Establish pirate cache in neutral system"

### Story Arc Examples

**Hegemony Campaign: "Imperial Restoration"**
1. Prove loyalty by destroying rebel ships
2. Infiltrate Coalition cell on border world
3. Recover stolen Hegemony prototype
4. Lead battle fleet in major offensive
5. Decision: Genocide rebel planet or accept surrender
6. Consequences: If merciful, secret Coalition ally; if ruthless, feared throughout galaxy
7. Final mission: Defend Sol from Coalition counterattack OR participate in peace negotiations

**Coalition Campaign: "Freedom's Price"**
1. Escape Hegemony persecution
2. Join underground resistance
3. Sabotage Hegemony supply lines
4. Rally neutral systems
5. Decision: Accept Nexus AI support or reject for ideological purity
6. Consequences: Nexus path = advanced tech but AI dependence; Pure path = maintain humanity but harder struggle
7. Final mission: Lead liberation of oppressed colony OR assassination of Hegemony leadership

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
8110 REM Save faction reputations
8120 FOR I=1 TO 10: PRINT#1, FACTION_REP(I): NEXT I
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
9110 REM Load faction reputations
9120 FOR I=1 TO 10: INPUT#1, FACTION_REP(I): NEXT I
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

### Galaxy Distance Calculation
```basic
5000 REM === CALCULATE TRAVEL TIME ===
5010 REM INPUT: SOURCE_ID, DEST_ID
5020 REM OUTPUT: TRAVEL_DAYS, FUEL_COST
5030 REM
5040 REM Load system coordinates
5050 GOSUB 6000: REM Get source X,Y
5060 SX = SYSTEM_X: SY = SYSTEM_Y
5070 GOSUB 6100: REM Get dest X,Y
5080 DX = SYSTEM_X: DY = SYSTEM_Y
5090 REM
5100 REM Calculate distance (Pythagorean)
5110 DX = DX - SX: DY = DY - SY
5120 DIST = SQR(DX*DX + DY*DY)
5130 REM
5140 REM Calculate travel time
5150 TRAVEL_DAYS = INT(DIST / 10) + 1
5160 IF TRAVEL_DAYS < 1 THEN TRAVEL_DAYS = 1
5170 REM
5180 REM Calculate fuel cost
5190 FUEL_COST = INT(DIST * 2)
5200 REM
5210 RETURN
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
5. **Authenticity:** Real stellar neighborhood creates immersive setting
6. **8-bit Authenticity:** Embrace constraints, don't fight them

### Balancing Guidelines
- Early game: Forgiving, tutorial-like (Sol system and nearby stars)
- Mid game: Strategic choices matter (faction selection becomes critical)
- Late game: Mastery and optimization rewarded (faction wars, unique ships)
- No dead ends: Player can always recover from mistakes
- Difficulty through interesting choices, not stat checks
- Reputation system allows gradual faction switching if desired

### Content Philosophy
- Every system should feel distinct (real star names help)
- Every faction should offer unique gameplay
- Every ship should have a purpose
- Every upgrade should enable new strategies
- Every mission should tell a story
- Faction conflicts create emergent narratives

---

## Future Considerations

### Potential Expansions
- **Planetary Landing:** Visit surfaces, cities, markets in major systems
- **Fleet Command:** More than 2 escorts for high-level players
- **Economy Simulation:** More dynamic market system with news propagation
- **Procedural Events:** Greater variety in random encounters
- **Modding Support:** External data files for custom missions/factions
- **Expanded Galaxy:** Add more distant stars (50-100 light years)
- **Alien Mysteries:** Discover ancient precursor civilization artifacts

### Technical Improvements
- **Graphics Mode:** Use VERA bitmap/tile modes for star map
- **Music:** Background music via PSG (faction themes)
- **Networking:** Multi-player trading via serial/network
- **Assembly Rewrite:** Full ML version for performance
- **Voice Synthesis:** Text-to-speech for mission briefings

### Accessibility
- **Difficulty Modes:** Easy/Normal/Hard settings affecting combat and economy
- **Tutorial System:** Optional guided first hour in Sol system
- **Save Anywhere:** Not just at stations
- **Quick Save:** Rapid save/load for experimentation
- **Color Blind Mode:** Alternative color schemes

---

## Appendices

### A. Glossary
- **Banking:** Switching between 8KB pages of extended RAM
- **PETSCII:** PET Standard Code of Information Interchange (C64/X16 character set)
- **VERA:** Video Enhanced Retro Adapter (X16's video chip)
- **d100:** 100-sided die roll (0-99 or 1-100)
- **Hex:** Hexagon, unit of tactical combat grid
- **Light Year:** Distance light travels in one year (~9.46 trillion km)
- **Parsec:** Astronomical unit, ~3.26 light years
- **Spectral Type:** Classification of stars by temperature and color (O, B, A, F, G, K, M)
- **Port:** Docking location (planet, station, moon, etc.)
- **Faction Rep:** Reputation score with political factions (-100 to +100)

### B. Real Astronomy Notes

**Distance Compression:**
Real stellar distances are compressed by a factor of 10 for gameplay. For example:
- Alpha Centauri: Real distance 4.37 ly → Game distance ~1.2 units → 3 day travel
- Vega: Real distance 25.04 ly → Game distance ~8.5 units → 2-3 day travel

**Spectral Classification:**
Stars are classified by spectral type from hottest to coolest:
- **O, B:** Very hot, blue-white (none in local neighborhood)
- **A:** Hot, white (Sirius, Vega, Altair, Fomalhaut)
- **F:** Yellow-white, hotter than Sun
- **G:** Yellow, Sun-like (Sol, Alpha Centauri, Tau Ceti)
- **K:** Orange, cooler than Sun
- **M:** Cool red dwarfs (most common type)
- **D:** White dwarf (stellar remnant)

**Binary Systems:**
Many real stars are binary (two stars orbiting each other):
- Alpha Centauri: Actually a triple system (A, B, and Proxima)
- 61 Cygni: Binary orange stars
- Sirius: White star with white dwarf companion

### C. References
- Commander X16 documentation: https://github.com/X16Community/x16-docs
- BASIC programming guide: X16 BASIC reference
- Escape Velocity series: Original inspiration
- Elite: Classic space trading game
- SIMBAD Astronomical Database: Real stellar data source
- Wikipedia: Stellar neighborhood data

### D. Credits
- **Design:** [Your Name]
- **Platform:** Commander X16 project
- **Inspiration:** Escape Velocity (Ambrosia Software), Elite (Acornsoft)
- **Astronomical Data:** SIMBAD, HYG Database, Wikipedia
- **Galaxy Generation:** Python scripts for real stellar data processing

---

**Document Version:** 0.2  
**Last Updated:** November 21, 2024  
**Status:** Galaxy & Factions Complete - Ready for Phase 1 Development  
**Next Review:** After Phase 1 prototype completion

---

*This is a living document. Update as design evolves through development.*

---

## Quick Reference Tables

### Faction Quick Reference

| Faction | Capital | Systems | Type | Primary Trait | Player Start Rep |
|---------|---------|---------|------|---------------|------------------|
| Terran Hegemony | Sol | 20 | Major | Militaristic | 0 (Neutral) |
| Free Systems Coalition | Tau Ceti | 15 | Major | Democratic | +10 (Slightly Friendly) |
| Frontier Alliance | Gliese 163 | 24 | Major | Neutral | 0 (Neutral) |
| Nexus Collective | Sirius | 9 | Major | AI-Cyberpunk | -10 (Suspicious) |
| Velanthi Commonwealth | Vega | 7 | Alien | Mysterious | 0 (Unknown) |
| Crimson Cartel | Wolf 359 | 2 | Minor | Criminal | -30 (Hostile) |
| Nova Mining Guild | Epsilon Eridani | 2 | Minor | Corporate | +5 (Friendly) |
| Free Traders Union | N/A | 0 | Mission | Commercial | 0 (Neutral) |
| Archaeological Concord | N/A | 0 | Mission | Academic | 0 (Neutral) |

### Key Systems Quick Reference

| System | Coordinates | Faction | Ports | Notes |
|--------|-------------|---------|-------|-------|
| Sol | (0, 0) | Hegemony | 1 | Player start, capital |
| Alpha Centauri | (-12, -3) | Hegemony | 3 | Nearest neighbor, major hub |
| Tau Ceti | (38, -9) | Coalition | 1 | Rebel capital |
| Sirius | (-29, 10) | Nexus | 1 | AI civilization |
| Vega | (-52, 65) | Velanthi | 1 | Alien capital |
| Wolf 359 | (24, 3) | Cartel | 1 | Pirate haven |
| Epsilon Eridani | (9, -32) | Guild | 1 | Mining HQ |

### Reputation Tiers

| Rep Range | Status | Station Access | Equipment | Missions | Prices |
|-----------|--------|----------------|-----------|----------|--------|
| -100 to -25 | Hostile | Denied | None | None | N/A |
| -24 to +24 | Neutral | Basic | Standard | Basic | Standard |
| +25 to +74 | Friendly | Full | Advanced | Faction | -10% |
| +75 to +100 | Allied | Full | Unique | Story | -20% |

---

**END OF DOCUMENT**
