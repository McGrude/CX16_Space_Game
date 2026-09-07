# PHASE 3 — Civilization Expansion & Historical Simulation

## Master Specification Document

This document defines the complete specification for Phase 3 of the Commander X16 Space-Trading RPG universe generation pipeline. It builds upon the foundations established in Phases 0–2 and provides the framework for simulating human expansion into the stars.

---

# Part I: Cultural Heritage Foundations

Before simulating civilization expansion, we establish the cultural pillars that inform naming conventions, faction identities, and historical flavor.

---

## 1. Cultural Heritage Pillars

Human civilization in the expansion era draws from eight major cultural heritage streams. These pillars provide pools for person names, place names, ship names, and corporate/faction naming conventions.

### 1.1 The Eight Pillars

| Pillar | Primary Influences | Naming Character |
|--------|-------------------|------------------|
| **Anglo** | English, American, Australian, Canadian | Williams, Chen Station, New Bristol, HMS Defiant |
| **Sino** | Chinese (Mandarin), Taiwanese, Singaporean | Wei, Huang, Tiangong, Jade Harbor, Longwei |
| **Indic** | Hindi, Sanskrit, Tamil, Bengali | Sharma, Patel, Naveen, Surya Station, Prithvi |
| **Nihon** | Japanese | Tanaka, Yamamoto, Hikari, Tsukuba, Akatsuki |
| **Hispano** | Spanish, Portuguese, Latin American | Garcia, Santos, Nueva Esperanza, El Dorado |
| **Slavic** | Russian, Ukrainian, Polish, Czech | Volkov, Petrov, Novgorod, Zarya, Mir |
| **Arabic** | Middle Eastern, North African | Al-Rashid, Hakim, Qamar, Medina Station |
| **African** | Swahili, Yoruba, Ethiopian, pan-African | Okonkwo, Abebe, Nyota, Wakanda, Ubuntu |

### 1.2 Pillar Usage Guidelines

Each pillar provides:

- **Personal Names**: First names and surnames for historical figures, NPCs, ship captains
- **Place Names**: Colony names, station names, outpost designations
- **Ship Names**: Vessel naming conventions (poetic, military, commercial)
- **Corporate Style**: Naming patterns for businesses originating from that culture
- **Titles and Honorifics**: Governor, Director, Admiral equivalents

### 1.3 Cultural Blending Rules

By the expansion era, cultures have blended significantly:

- **Core Worlds** (Sol system, first colonies): Highly multicultural, mixed naming
- **Outer Colonies**: Often dominated by founding culture (colony ship origin)
- **Corporate Zones**: Named after founding corporation's cultural origin
- **Frontier Stations**: Pragmatic names, often descriptive (Refinery-7, Outpost Delta)

### 1.4 Name Generation Determinism

Name selection is deterministic based on:

```
name_seed = hash(system_id, object_id, "person"|"place", index)
cultural_pillar = weighted_selection(seed, pillar_weights_for_region)
name = select_from_pool(pillar, seed)
```

This ensures reproducibility across generation runs.

---

## 1.5 Sample Name Pools (Abbreviated)

### Anglo Names
**Surnames**: Williams, Chen, O'Brien, MacGregor, Thompson, Wright, Chen, Park
**Given (M)**: James, William, Thomas, Michael, David, Robert
**Given (F)**: Elizabeth, Sarah, Catherine, Victoria, Margaret, Anne
**Places**: New Bristol, Armstrong, Aldrin Station, Pioneer's Rest

### Sino Names
**Surnames**: Wang, Li, Zhang, Liu, Chen, Yang, Huang, Zhou
**Given (M)**: Wei, Jun, Ming, Tao, Lei, Feng
**Given (F)**: Mei, Ling, Xiu, Hui, Yan, Jing
**Places**: Tiangong, Longmen, Jade Harbor, Celestial Gate, Qilin Station

### Indic Names
**Surnames**: Sharma, Patel, Singh, Kumar, Rao, Nair, Gupta
**Given (M)**: Arjun, Raj, Vikram, Naveen, Sanjay, Anil
**Given (F)**: Priya, Deepa, Anita, Sunita, Lakshmi, Radha
**Places**: Surya Station, Prithvi, Chandra Base, Indra's Eye, Agni Point

### Nihon Names
**Surnames**: Tanaka, Yamamoto, Suzuki, Sato, Nakamura, Kobayashi
**Given (M)**: Hiroshi, Takeshi, Kenji, Yuki, Ryu, Shin
**Given (F)**: Yuki, Sakura, Haruki, Emi, Akiko, Mika
**Places**: Hikari, Tsukuba, Akatsuki Station, Yamato, Shinjuku Orbital

### Hispano Names
**Surnames**: Garcia, Rodriguez, Martinez, Lopez, Santos, Silva, Costa
**Given (M)**: Carlos, Miguel, Juan, Pedro, Rafael, Diego
**Given (F)**: Maria, Ana, Carmen, Rosa, Elena, Sofia
**Places**: Nueva Esperanza, El Dorado, Puerto Celeste, Estrella Station

### Slavic Names
**Surnames**: Volkov, Petrov, Ivanov, Sokolov, Kuznetsov, Novak
**Given (M)**: Alexei, Dmitri, Ivan, Mikhail, Yuri, Sergei
**Given (F)**: Natasha, Katya, Olga, Irina, Svetlana, Anya
**Places**: Novgorod Station, Zarya, Mir II, Vostok, Gagarin Point

### Arabic Names
**Surnames**: Al-Rashid, Al-Amin, Hakim, Khalil, Mansour, Nasser
**Given (M)**: Ahmed, Omar, Khalid, Tariq, Yusuf, Hassan
**Given (F)**: Fatima, Layla, Amira, Zara, Nadia, Leila
**Places**: Qamar Station, Medina Orbital, Al-Burj, Sahara Prime

### African Names
**Surnames**: Okonkwo, Abebe, Mwangi, Diallo, Toure, Mensah
**Given (M)**: Kwame, Kofi, Ade, Chidi, Sekou, Jelani
**Given (F)**: Amara, Zuri, Nia, Aisha, Fatou, Sanaa
**Places**: Nyota Station, Ubuntu, Kilimanjaro Orbital, Serengeti Base

---

# Part II: Political Factions

Six major political factions dominate the inhabited galaxy. Each represents a distinct governance philosophy, economic model, and cultural blend.

---

## 2. The Six Factions

### 2.1 Faction Overview Table

| ID | Name | Type | Alignment | Cultural Blend | Core Territory |
|----|------|------|-----------|----------------|----------------|
| F1 | **Terran Commonwealth** | Federal Democracy | Centrist-Progressive | Anglo, Sino, Indic | Sol, Alpha Centauri |
| F2 | **Prosperity Syndicate** | Corporate Oligarchy | Libertarian-Capitalist | Anglo, Nihon | Tau Ceti, 82 Eridani |
| F3 | **People's Stellar Union** | Socialist Republic | Collectivist-Authoritarian | Slavic, Sino | Barnard's Star, Lalande |
| F4 | **Frontier Alliance** | Confederacy | Libertarian-Frontier | Hispano, Anglo, African | Epsilon Eridani, Gliese 876 |
| F5 | **Divine Mandate** | Theocratic Monarchy | Conservative-Authoritarian | Arabic, Indic | 61 Cygni, Groombridge |
| F6 | **Technocratic Collective** | Meritocratic Technocracy | Rationalist-Progressive | Nihon, Sino, Anglo | Procyon, Sirius |

---

### 2.2 Faction Profiles

#### F1: Terran Commonwealth

**Government Type**: Federal representative democracy
**Capital**: Earth (Sol system)
**Founding Date**: 2157 CE (Treaty of Geneva)

**Philosophy**: The Commonwealth believes in balanced governance, individual rights protected by collective institutions, and measured expansion. It is the direct descendant of the United Nations Space Agency that launched the first colony ships.

**Strengths**:
- Diplomatic legitimacy (seen as humanity's "original" government)
- Diverse population and cultural resources
- Strong research institutions
- Central galactic position

**Weaknesses**:
- Bureaucratic inertia
- Internal political gridlock
- Aging infrastructure in core systems
- Difficulty projecting power to distant colonies

**Economy**: Mixed economy with regulated markets, strong public services, and significant state investment in research and infrastructure.

**Military Doctrine**: Defensive posture with emphasis on diplomatic resolution. Maintains powerful home fleet but reluctant to project force.

**Relations**:
- Rivalry with Prosperity Syndicate (economic competition)
- Cold war with People's Stellar Union (ideological opposition)
- Protective alliance with Divine Mandate (shared traditionalism)
- Uneasy peace with Frontier Alliance (disputes over outer territories)
- Research partnerships with Technocratic Collective

---

#### F2: Prosperity Syndicate

**Government Type**: Corporate oligarchy with elected advisory council
**Capital**: New Singapore (Tau Ceti system)
**Founding Date**: 2203 CE (Tau Ceti Compact)

**Philosophy**: The Syndicate believes markets, not governments, should allocate resources and drive progress. They see human expansion as fundamentally an economic activity, best managed by those with proven success in commerce.

**Strengths**:
- Enormous wealth and capital reserves
- Efficient administration
- Advanced manufacturing and trade infrastructure
- Attracts ambitious talent

**Weaknesses**:
- Social inequality breeds internal unrest
- Profit motive can override long-term planning
- Dependent on trade routes remaining open
- Minimal social safety net creates desperation

**Economy**: Free market capitalism with minimal regulation. Corporations hold effective sovereignty over many stations and colonies.

**Military Doctrine**: Private security contractors and corporate fleets. Prefers economic pressure to military confrontation.

**Relations**:
- Economic competition with Terran Commonwealth
- Hostile to People's Stellar Union (ideological opposites)
- Exploitative relationship with Frontier Alliance (buys raw materials)
- Distrust of Divine Mandate (unpredictable)
- Funding partnership with Technocratic Collective

---

#### F3: People's Stellar Union

**Government Type**: One-party socialist republic
**Capital**: Novgorod Station (Barnard's Star system)
**Founding Date**: 2189 CE (Stellar Revolution)

**Philosophy**: The Union arose from workers who fled corporate exploitation in early colonies. They believe collective ownership of production and central planning are necessary to prevent the suffering they witnessed.

**Strengths**:
- Unified command structure
- Strong heavy industry
- High social cohesion
- Effective at rapid mobilization

**Weaknesses**:
- Innovation stifled by bureaucracy
- Black markets inevitable
- Brain drain to other factions
- Internal security apparatus creates fear

**Economy**: Centrally planned economy with state ownership of major industries. Private enterprise tolerated in consumer goods.

**Military Doctrine**: Large standing fleet with conscript crews. Emphasizes quantity and redundancy over cutting-edge technology.

**Relations**:
- Ideological cold war with Terran Commonwealth
- Active hostility toward Prosperity Syndicate
- Revolutionary solidarity with some Frontier Alliance elements
- Suspicion of Divine Mandate (competing authoritarian model)
- Technology theft attempts against Technocratic Collective

---

#### F4: Frontier Alliance

**Government Type**: Loose confederacy of independent systems
**Capital**: Libertad Station (Epsilon Eridani system)
**Founding Date**: 2234 CE (Frontier Declaration)

**Philosophy**: The Alliance believes in maximum local autonomy and minimal central authority. Each system governs itself; the Alliance provides mutual defense and trade standards only.

**Strengths**:
- Adaptive and resilient
- Strong local initiative
- Rich in raw materials
- Attracts independent spirits

**Weaknesses**:
- Difficulty coordinating large-scale action
- Vulnerable to internal divisions
- Limited industrial capacity
- Pirates and criminals exploit loose governance

**Economy**: Varies by system. Generally resource extraction and agriculture, with limited manufacturing. Dependent on trade with other factions.

**Military Doctrine**: System defense forces coordinated loosely. Emphasizes guerrilla tactics and local knowledge.

**Relations**:
- Border disputes with Terran Commonwealth
- Economic dependency on Prosperity Syndicate
- Some ideological sympathy with People's Stellar Union
- Indifferent to Divine Mandate
- Trades raw materials to Technocratic Collective

---

#### F5: Divine Mandate

**Government Type**: Theocratic monarchy with appointed councils
**Capital**: Al-Burj Station (61 Cygni system)
**Founding Date**: 2212 CE (Great Pilgrimage)

**Philosophy**: The Mandate believes humanity's expansion into the stars fulfills divine purpose. They seek to build a civilization aligned with sacred principles, offering order and meaning in a chaotic universe.

**Strengths**:
- Fanatical loyalty from true believers
- Strong social cohesion
- Long-term planning horizon
- Excellent cultural institutions

**Weaknesses**:
- Religious doctrine can conflict with pragmatism
- Persecution of dissent
- Limited appeal to outsiders
- Internal schisms between interpretations

**Economy**: Mixed economy guided by religious principles. Prohibitions on certain industries (gambling, some biotech). Strong craft traditions.

**Military Doctrine**: Professional military with religious officers (chaplain-commanders). Fights with conviction but limited resources.

**Relations**:
- Protective alliance with Terran Commonwealth
- Distrusted by Prosperity Syndicate
- Mutual suspicion with People's Stellar Union
- Missionary efforts in Frontier Alliance
- Limited contact with Technocratic Collective (seen as godless)

---

#### F6: Technocratic Collective

**Government Type**: Meritocratic technocracy with AI-assisted governance
**Capital**: Prometheus Station (Procyon system)
**Founding Date**: 2245 CE (Rational Compact)

**Philosophy**: The Collective believes governance should be entrusted to proven experts using evidence-based decision-making. They embrace AI assistance and view emotional politics as a primitive hindrance.

**Strengths**:
- Cutting-edge technology
- Efficient administration
- Attracts top scientific talent
- Advanced AI and automation

**Weaknesses**:
- Cold and alienating to outsiders
- Vulnerable to groupthink among elites
- Small population base
- Over-reliance on technology

**Economy**: High-tech manufacturing, research licensing, and consulting. Limited primary production; dependent on imports.

**Military Doctrine**: Small but extremely advanced fleet. Emphasizes electronic warfare, drones, and precision strikes.

**Relations**:
- Research partnerships with Terran Commonwealth
- Funding arrangements with Prosperity Syndicate
- Target of technology theft by People's Stellar Union
- Supplies technology to Frontier Alliance (for resources)
- Avoided by Divine Mandate

---

## 2.3 Faction Interaction Matrix

| | TC | PS | PSU | FA | DM | TCo |
|---|---|---|---|---|---|---|
| **Terran Commonwealth (TC)** | — | Rivalry | Cold War | Tension | Alliance | Partnership |
| **Prosperity Syndicate (PS)** | Rivalry | — | Hostile | Exploitation | Distrust | Funding |
| **People's Stellar Union (PSU)** | Cold War | Hostile | — | Mixed | Suspicion | Espionage |
| **Frontier Alliance (FA)** | Tension | Dependency | Mixed | — | Indifferent | Trade |
| **Divine Mandate (DM)** | Alliance | Distrust | Suspicion | Mission | — | Avoidance |
| **Technocratic Collective (TCo)** | Partnership | Funding | Target | Trade | Avoidance | — |

---

# Part III: Major Corporations

Ten major corporations shape the galactic economy. Each has a founding date, headquarters, primary business, factional alignment, and historical role.

---

## 3. The Ten Corporations

### 3.1 Corporation Overview Table

| ID | Name | Sector | HQ Faction | Founded | Cultural Origin |
|----|------|--------|-----------|---------|-----------------|
| C1 | **Nakamura Heavy Industries** | Shipbuilding | Technocratic | 2098 | Nihon |
| C2 | **Red Star Mining Consortium** | Mining | People's Union | 2145 | Slavic |
| C3 | **Stellarwind Logistics** | Shipping | Prosperity | 2167 | Anglo |
| C4 | **Huang-Wei Propulsion** | FTL Technology | Commonwealth | 2112 | Sino |
| C5 | **Prometheus Arms** | Weapons | Technocratic | 2189 | Anglo/Nihon |
| C6 | **Luxor Interstellar** | Luxury Goods | Mandate | 2201 | Arabic |
| C7 | **Santos Agricultural** | Food/Biotech | Frontier | 2178 | Hispano |
| C8 | **Okonkwo Fabrication** | Manufacturing | Commonwealth | 2156 | African |
| C9 | **Novak Energy Systems** | Power/Fuel | People's Union | 2134 | Slavic |
| C10 | **Tanaka-Chen Medical** | Medical/Pharma | Commonwealth | 2123 | Nihon/Sino |

---

### 3.2 Corporation Profiles

#### C1: Nakamura Heavy Industries (NHI)

**Sector**: Shipbuilding and aerospace
**Headquarters**: Prometheus Station (Procyon)
**Founded**: 2098 CE
**Founder**: Kenji Nakamura

**History**: Founded on Earth before the expansion era, NHI built the first generation of colony ships. They relocated headquarters to Procyon when the Technocratic Collective offered favorable terms and access to advanced research.

**Products**: Colony ships, military cruisers, mining vessels, orbital stations
**Market Share**: 35% of new construction, 60% of capital ships
**Reputation**: Reliable, conservative designs with excellent longevity

**Notable Events**:
- 2156: Launched the *Hope of Mankind*, first successful interstellar colony ship
- 2234: Controversial contract to build warships for multiple factions
- 2298: Merger with Yamato Aerospace (formerly independent competitor)

---

#### C2: Red Star Mining Consortium (RSMC)

**Sector**: Mining and resource extraction
**Headquarters**: Novgorod Station (Barnard's Star)
**Founded**: 2145 CE
**Founder**: Collective founding (worker cooperative)

**History**: Born from a worker uprising at a corporate mining station, RSMC operates as a worker-owned cooperative within the People's Stellar Union. It is the only major corporation with this structure.

**Products**: Raw ore, refined metals, rare elements, mining equipment
**Market Share**: 25% of galactic ore production, 40% in Union territory
**Reputation**: Solid quality, heavily politicized, unreliable contracts with capitalist entities

**Notable Events**:
- 2145: Mining Station Revolt; workers seize control
- 2198: Expansion into neutral systems creates friction with Prosperity Syndicate
- 2267: Temporary trade agreement with Stellarwind during resource crisis

---

#### C3: Stellarwind Logistics

**Sector**: Shipping, transport, and warehousing
**Headquarters**: New Singapore (Tau Ceti)
**Founded**: 2167 CE
**Founder**: Victoria Chen

**History**: Started as a small courier service, Stellarwind grew to dominate commercial shipping through aggressive acquisition and efficiency innovations. They operate the largest merchant fleet in known space.

**Products**: Cargo transport, passenger service, warehousing, shipping insurance
**Market Share**: 45% of inter-system cargo, 60% in Prosperity Syndicate space
**Reputation**: Fast, reliable, expensive; rumored to smuggle on the side

**Notable Events**:
- 2189: Acquisition of three smaller shipping companies
- 2245: Shipping embargo during Union conflict causes economic crisis
- 2301: Stellarwind offices attacked by pirates; massive security buildup follows

---

#### C4: Huang-Wei Propulsion

**Sector**: FTL technology, propulsion systems
**Headquarters**: Earth (Sol)
**Founded**: 2112 CE
**Founders**: Dr. Huang Mei-Ling, Dr. Wei Jun

**History**: Huang-Wei achieved the breakthrough that made practical FTL travel possible. Their proprietary drive technology remains the standard, though competitors have closed the gap. Close ties to the Commonwealth government.

**Products**: FTL drives, sublight engines, fuel systems, navigation computers
**Market Share**: 55% of FTL drives, 30% of sublight systems
**Reputation**: Cutting-edge but expensive; political strings attached

**Notable Events**:
- 2142: First successful FTL test flight
- 2156: FTL drives enable practical interstellar colonization
- 2234: Technology sharing with Technocratic Collective creates controversy
- 2278: "Huang-Wei Incident" — corporate espionage scandal with Union agents

---

#### C5: Prometheus Arms

**Sector**: Military hardware and weapons
**Headquarters**: Prometheus Station (Procyon)
**Founded**: 2189 CE
**Founder**: James Wright

**History**: Founded during a period of rising inter-faction tensions, Prometheus Arms grew by supplying weapons to all sides. Their headquarters in the neutral Technocratic Collective allows them to sell to any buyer.

**Products**: Ship weapons, personal arms, defense systems, military vehicles
**Market Share**: 40% of military hardware market
**Reputation**: Quality weapons, no questions asked; controversial but essential

**Notable Events**:
- 2212: Arms sales to Divine Mandate during founding conflicts
- 2267: Embargo by Commonwealth after weapons found with pirates
- 2289: Embargo lifted; Prometheus donates to Commonwealth defense fund

---

#### C6: Luxor Interstellar

**Sector**: Luxury goods, entertainment, hospitality
**Headquarters**: Al-Burj Station (61 Cygni)
**Founded**: 2201 CE
**Founder**: Khalid Al-Rashid

**History**: Luxor carved out a niche providing luxury goods to the wealthy across all factions. Their flagship casinos, hotels, and entertainment venues are famously neutral territory.

**Products**: Luxury consumer goods, casinos, hotels, entertainment
**Market Share**: 65% of luxury sector
**Reputation**: Opulent, decadent, politically neutral; excellent information brokers

**Notable Events**:
- 2234: Luxor Hotel becomes unofficial diplomatic meeting ground
- 2256: Gambling ban in People's Union creates smuggling opportunities
- 2298: Expansion into Frontier Alliance with mixed results

---

#### C7: Santos Agricultural

**Sector**: Food production, terraforming, biotech
**Headquarters**: Nueva Esperanza (Epsilon Eridani)
**Founded**: 2178 CE
**Founder**: Maria Santos

**History**: Santos developed the bio-engineered crops that made marginal worlds farmable. Their "Santos Seeds" are found on every agricultural colony, and their terraforming expertise is unmatched.

**Products**: Genetically modified crops, livestock, terraforming services, colony supplies
**Market Share**: 50% of agricultural sector, 70% of terraforming contracts
**Reputation**: Essential, ethical, sometimes stubbornly principled

**Notable Events**:
- 2198: Santos Seeds enable colonization of previously hostile worlds
- 2245: Refuses to provide terraforming to Union due to labor practices dispute
- 2289: Major expansion into food processing and distribution

---

#### C8: Okonkwo Fabrication

**Sector**: Manufacturing, industrial equipment, construction
**Headquarters**: Lagos Orbital (Sol)
**Founded**: 2156 CE
**Founder**: Chidi Okonkwo

**History**: Started building habitation modules for early orbital stations, Okonkwo grew to become the go-to manufacturer for everything from habitat domes to industrial machinery.

**Products**: Habitation modules, industrial equipment, construction materials, robots
**Market Share**: 30% of manufacturing, 50% of construction materials
**Reputation**: Solid, dependable, good value; less innovative than competitors

**Notable Events**:
- 2178: Contract to build Commonwealth's first extrasolar military base
- 2234: Opens factories in multiple factions to avoid trade barriers
- 2267: Labor dispute leads to temporary shutdown; resolved through negotiation

---

#### C9: Novak Energy Systems

**Sector**: Power generation and fuel
**Headquarters**: Zarya Station (Lalande 21185)
**Founded**: 2134 CE
**Founder**: Dmitri Novak

**History**: Originally a state enterprise in the People's Union, Novak Energy was semi-privatized but remains closely tied to Union government. They control critical fuel processing infrastructure.

**Products**: Reactor cores, fuel cells, refined fuel, power grid systems
**Market Share**: 35% of power systems, 25% of fuel (higher in Union)
**Reputation**: Reliable but politically entangled; exports require government approval

**Notable Events**:
- 2167: Fuel embargo creates crisis in early Prosperity Syndicate colonies
- 2212: Technology sharing agreement with Technocratic Collective
- 2278: Price manipulation scandal leads to internal Union investigation

---

#### C10: Tanaka-Chen Medical

**Sector**: Medical equipment, pharmaceuticals, biotechnology
**Headquarters**: Earth (Sol)
**Founded**: 2123 CE
**Founders**: Dr. Hiroshi Tanaka, Dr. Chen Wei

**History**: A merger of Japanese and Chinese medical research firms, Tanaka-Chen pioneered the treatments that made long-duration spaceflight safe. Their products are found in every sickbay.

**Products**: Medical equipment, pharmaceuticals, genetic treatments, prosthetics
**Market Share**: 50% of medical sector
**Reputation**: Essential, expensive, aggressive patent enforcement

**Notable Events**:
- 2142: Anti-radiation treatments enable longer FTL journeys
- 2198: Cloning controversy; banned products still sold on black market
- 2267: Patent dispute with Technocratic Collective researchers

---

## 3.3 Corporation-Faction Alignment Matrix

| Corporation | TC | PS | PSU | FA | DM | TCo |
|-------------|----|----|-----|----|----|-----|
| Nakamura Heavy | Neutral | Contract | Barred | Contract | Contract | HQ |
| Red Star Mining | Embargo | Hostile | HQ | Limited | Barred | Limited |
| Stellarwind | Contract | HQ | Embargo | Contract | Contract | Contract |
| Huang-Wei | HQ | Contract | Barred | Contract | Contract | Partner |
| Prometheus Arms | Contract | Contract | Contract | Contract | Contract | HQ |
| Luxor | Contract | Contract | Limited | Contract | HQ | Contract |
| Santos Agri | Contract | Contract | Barred | HQ | Contract | Contract |
| Okonkwo | HQ | Contract | Contract | Contract | Contract | Contract |
| Novak Energy | Limited | Limited | HQ | Limited | Barred | Partner |
| Tanaka-Chen | HQ | Contract | Limited | Contract | Contract | Contract |

**Legend**: HQ = Headquarters faction | Contract = Normal business | Limited = Restricted | Barred = No business | Embargo = Active trade war | Partner = Special relationship

---

# Part IV: Historical Timeline Framework

The simulation spans approximately 2,500 years from the present to the "game present" era.

---

## 4. The Four Eras

### 4.1 Era Overview

| Era | Years | Name | Character |
|-----|-------|------|-----------|
| **Era 0** | 2025–2140 | Pre-Expansion | Earth-bound, early space colonization |
| **Era 1** | 2140–2250 | First Wave | FTL breakthrough, initial colonization rush |
| **Era 2** | 2250–2400 | Divergence | Factions form, first conflicts, consolidation |
| **Era 3** | 2400–2550 | Maturation | Current era, game present |

---

### 4.2 Era 0: Pre-Expansion (2025–2140)

**Theme**: Humanity confined to Sol system; technological foundations laid

**Key Developments**:
- 2025–2050: Climate crisis drives space investment
- 2045: Permanent Luna base established
- 2067: Mars colony founded (Ares City)
- 2089: Asteroid mining becomes profitable
- 2098: Nakamura Heavy Industries founded
- 2112: Huang-Wei Propulsion founded; sublight drives improved
- 2123: Tanaka-Chen Medical founded; space medicine advances
- 2134: Novak Energy founded; fusion power matures
- 2138: First FTL experiments (failures)

**End Condition**: Practical FTL achieved (2142)

---

### 4.3 Era 1: First Wave (2140–2250)

**Theme**: Expansion explosion; colonies founded; independence movements begin

**Key Developments**:
- 2142: Huang-Wei achieves first successful FTL jump
- 2145: Alpha Centauri colonized; Red Star Mining founded
- 2156: Second wave of colony ships; NHI launches *Hope of Mankind*
- 2157: Terran Commonwealth established (Treaty of Geneva)
- 2167: Tau Ceti colonized; Stellarwind Logistics founded
- 2178: Santos Agricultural founded; marginal worlds become viable
- 2189: Barnard's Star workers revolt; People's Stellar Union founded; Prometheus Arms founded
- 2201: Luxor Interstellar founded
- 2203: Tau Ceti Compact; Prosperity Syndicate established
- 2212: Great Pilgrimage; Divine Mandate founded
- 2234: Frontier Declaration; Frontier Alliance established
- 2245: Rational Compact; Technocratic Collective established

**End Condition**: All six factions established

---

### 4.4 Era 2: Divergence (2250–2400)

**Theme**: Faction consolidation; wars; technological competition; boundaries harden

**Key Developments**:
- 2256–2267: First Faction War (Commonwealth vs. Union)
- 2267: Armistice of Procyon; current borders roughly established
- 2278: Huang-Wei Incident; corporate espionage scandal
- 2289: Second colonial wave; outer systems settled
- 2298: Nakamura-Yamato merger; shipbuilding consolidated
- 2301: Pirate uprisings in Frontier Alliance
- 2312–2334: Second Faction War (Syndicate vs. Alliance; Union intervention)
- 2334: Peace of Epsilon; trade agreements formalized
- 2356: FTL-2 technology deployed (faster, more efficient drives)
- 2378: Artifact Wars (skirmishes over alien ruin sites)
- 2389: Artifact Treaty; ruins designated protected research sites
- 2398: Third colonial wave; frontier expands

**End Condition**: Relative stability achieved; game era begins

---

### 4.5 Era 3: Maturation (2400–2550)

**Theme**: Current era; fragile peace; economic competition; exploration continues

**Key Developments**:
- 2400: "Modern" era begins
- 2412: Player's grandfather born (if desired backstory)
- 2445: Minor border conflict (Mandate vs. Alliance)
- 2478: Economic crisis; Stellarwind embargo
- 2489: Recovery; new trade routes established
- 2501: First alien artifact fully decoded (Rosetta Ruin)
- 2523: FTL-3 technology tested (prototype only)
- 2534: Present day (game start)

---

## 4.3 Technology Milestones

| Year | Technology | Impact |
|------|------------|--------|
| 2045 | Permanent space habitation | Continuous human presence beyond Earth |
| 2089 | Profitable asteroid mining | Economic incentive for space expansion |
| 2112 | Advanced sublight drives | Reduced Sol system travel times |
| 2134 | Practical fusion power | Abundant energy for colonies |
| 2142 | FTL-1 (Huang-Wei Drive) | Interstellar colonization possible |
| 2198 | Santos Seeds (biotech) | Marginal worlds farmable |
| 2267 | Standardized AI systems | Automation of complex tasks |
| 2356 | FTL-2 (Improved drives) | Faster travel, reduced fuel |
| 2501 | Artifact decoding | Limited alien tech integration |
| 2523 | FTL-3 (Prototype) | Future plot hook |

---

# Part V: System Population Model

This section defines how star systems are populated with inhabited places and installations.

---

## 5. Population Parameters

### 5.1 System-Level Constraints

| Parameter | Minimum | Maximum | Notes |
|-----------|---------|---------|-------|
| Star systems | 80 | 120 | Based on real stars within ~50 ly |
| Planets per system | 0 | 8 | Including moons as separate |
| Inhabited places per system | 0 | 5 | Colonies, stations, outposts |
| Abandoned sites per system | 0 | 2 | Derelicts, ruins, ghost towns |

### 5.2 Place Types

| Code | Type | Description |
|------|------|-------------|
| COL | Colony | Permanent settlement on planet/moon |
| STA | Station | Orbital or deep-space installation |
| OUT | Outpost | Small temporary or specialized facility |
| MIN | Mining | Resource extraction site |
| SCI | Science | Research installation |
| MIL | Military | Defense or naval installation |
| ABN | Abandoned | Former installation, now derelict |
| ART | Artifact | Alien ruin site (from Phase 2) |

### 5.3 Population Distribution

Systems fall into categories based on habitability and location:

| Category | Inhabited Places | Abandoned Sites | Examples |
|----------|-----------------|-----------------|----------|
| Core World | 3–5 | 0–1 | Sol, Alpha Centauri, Tau Ceti |
| Developed | 2–4 | 0–1 | Procyon, Epsilon Eridani |
| Frontier | 1–2 | 0–2 | Outer systems |
| Marginal | 0–1 | 0–2 | Harsh or remote systems |
| Uninhabited | 0 | 0–1 | Empty systems with resources |

---

## 5.4 Sol System Special Case

Sol always contains:

| Object | Type | Name | Faction |
|--------|------|------|---------|
| Earth | COL | Earth (capital) | Commonwealth |
| Luna | COL | Armstrong | Commonwealth |
| Mars | COL | Ares City | Commonwealth |
| Ceres | MIN | Ceres Station | Commonwealth |
| Orbit | STA | Lagos Orbital | Commonwealth |
| Orbit | MIL | High Guard Station | Commonwealth |

Additional sites may be generated (abandoned early stations, etc.)

---

## 5.5 Colonization Wave Model

Colonization proceeds in waves from Sol:

**Wave 1 (Era 1 early)**: Alpha Centauri, Barnard's Star, Wolf 359
**Wave 2 (Era 1 late)**: Tau Ceti, Epsilon Eridani, Procyon, Sirius
**Wave 3 (Era 2)**: 61 Cygni, Groombridge, Lalande, 82 Eridani
**Wave 4 (Era 3)**: Outer systems, frontier expansion

Distance from Sol influences:
- Colonization date (earlier for closer systems)
- Development level (more developed closer to Sol)
- Faction control (Commonwealth dominant near Sol)

---

# Part VI: Historical Event Generation

Events are generated deterministically based on faction interactions, corporate activities, and random perturbations.

---

## 6. Event Categories

### 6.1 Political Events

| Type | Frequency | Impact |
|------|-----------|--------|
| Faction founding | Once per faction | Creates new faction |
| War declaration | Rare | Major conflict begins |
| Treaty signing | Follows war | Ends conflict, sets terms |
| Leadership change | Periodic | May shift faction policy |
| Border adjustment | After conflicts | Territory changes hands |
| Rebellion | Rare | Colony changes faction |

### 6.2 Corporate Events

| Type | Frequency | Impact |
|------|-----------|--------|
| Company founding | Once per company | Creates new corporation |
| Merger | Occasional | Combines companies |
| Bankruptcy | Rare | Company fails |
| Major contract | Periodic | Shifts economic power |
| Scandal | Occasional | Damages reputation |
| Innovation | Periodic | New products/services |

### 6.3 Colony Events

| Type | Frequency | Impact |
|------|-----------|--------|
| Founding | During expansion | New settlement |
| Growth | Automatic | Population increase |
| Disaster | Rare | Population loss |
| Abandonment | Rare | Colony becomes derelict |
| Uprising | Rare | Local faction change |
| Specialization | Automatic | Colony develops focus |

### 6.4 Technology Events

| Type | Frequency | Impact |
|------|-----------|--------|
| Breakthrough | Rare | Major new capability |
| Improvement | Periodic | Incremental advance |
| Artifact discovery | Rare | Unique alien tech |
| Artifact decoding | Very rare | Major knowledge gain |

---

## 6.2 Event Generation Algorithm

For each simulated year:

1. **Check faction tensions**: If threshold exceeded, possible war/incident
2. **Check corporate competition**: Possible merger, scandal, innovation
3. **Check colony states**: Growth, disaster chance, uprising chance
4. **Check technology**: Breakthrough chance based on research investment
5. **Apply random perturbation**: Small chance of unexpected events

Events are logged with:
- Date (year, optionally month)
- Event type
- Participants (factions, corporations, systems, individuals)
- Outcome
- Long-term consequences

---

# Part VII: Generation Pipeline Integration

---

## 7. Pipeline Position

Phase 3 follows Phases 0–2 and precedes Phases 4–5:

```
Phase 0: Star catalog (star_catalog.csv)
    ↓
Phase 1: Natural objects (system_objects.csv)
    ↓
Phase 2: Alien artifacts (system_objects.csv augmented)
    ↓
Phase 3: Civilization expansion (THIS PHASE)
    ↓
Phase 4: Economy and trade
    ↓
Phase 5: Mission generation
```

---

## 7.2 Phase 3 Outputs

### Primary Output: `civilization.csv`

| Field | Type | Description |
|-------|------|-------------|
| system_id | int | Star system reference |
| place_id | int | Unique place identifier |
| place_type | str | COL/STA/OUT/MIN/SCI/MIL/ABN/ART |
| name | str | Place name |
| parent_object_id | int | Natural object reference (if on surface) |
| faction_id | str | Controlling faction (F1–F6 or NONE) |
| founded_year | int | Year established |
| abandoned_year | int | Year abandoned (if applicable) |
| population_class | int | 0–5 population scale |
| specialization | str | Industry focus (if any) |
| tech_level | int | 1–10 technology rating |

### Secondary Output: `factions.csv`

| Field | Type | Description |
|-------|------|-------------|
| faction_id | str | F1–F6 |
| name | str | Faction name |
| government_type | str | Government form |
| capital_system | int | Capital system_id |
| founded_year | int | Year established |
| cultural_pillars | str | Comma-separated cultural codes |

### Secondary Output: `corporations.csv`

| Field | Type | Description |
|-------|------|-------------|
| corp_id | str | C1–C10 |
| name | str | Corporation name |
| sector | str | Industry sector |
| hq_system | int | Headquarters system_id |
| founded_year | int | Year established |
| founder_name | str | Founder's name |
| faction_alignment | str | Primary faction |

### Secondary Output: `timeline.csv`

| Field | Type | Description |
|-------|------|-------------|
| year | int | Event year |
| event_type | str | Category code |
| participants | str | Comma-separated IDs |
| description | str | Event description |
| consequence | str | Long-term effect |

---

## 7.3 Determinism Requirements

All Phase 3 generation must be deterministic:

```
rng_seed = hash(global_seed, system_id, "civilization")
```

Same inputs → identical outputs across runs.

---

# Part VIII: Implementation Notes

---

## 8.1 Generation Sequence

1. Load Phase 0–2 outputs
2. Initialize factions (fixed data)
3. Initialize corporations (fixed data)
4. Simulate Era 0 events (pre-expansion)
5. Simulate Era 1 (first wave colonization)
6. Simulate Era 2 (divergence and conflict)
7. Simulate Era 3 (maturation to present)
8. Output all CSV files

---

## 8.2 Colonization Priority Algorithm

When determining which systems to colonize:

```
priority = (habitability × 2) + (ore_richness + fuel_richness) - (risk × 0.5) - (distance × 3) + (artifact_bonus × 5)
```

Higher priority systems are colonized first.
Artifact presence provides significant bonus (attracts research/military).

---

## 8.3 Faction Expansion Rules

Each faction expands from its founding location:

- **Commonwealth**: Sol outward in all directions
- **Prosperity Syndicate**: Tau Ceti toward resource-rich systems
- **People's Union**: Barnard's Star toward industrial targets
- **Frontier Alliance**: Epsilon Eridani toward unclaimed systems
- **Divine Mandate**: 61 Cygni toward habitable worlds
- **Technocratic Collective**: Procyon toward artifact sites

Factions do not expand into systems already claimed unless through war or treaty.

---

## 8.4 Abandonment Triggers

Sites become abandoned when:

- Resource depletion (mining sites)
- Disaster (colony or station)
- War damage (any site)
- Economic collapse (remote sites)
- Strategic withdrawal (military sites)

Abandoned sites remain in data with `abandoned_year` set.

---

# Appendix A: Cultural Name Banks (Extended)

Full name banks for each cultural pillar (100+ entries each) to be provided in separate supplementary file or generated algorithmically from seeds.

---

# Appendix B: Faction Emblems and Colors

| Faction | Primary Color | Secondary | Symbol |
|---------|--------------|-----------|--------|
| Commonwealth | Blue | Gold | Star and olive branch |
| Prosperity | Gold | Black | Rising sun and scales |
| People's Union | Red | Gold | Star and gear |
| Frontier | Green | Brown | Compass rose |
| Divine Mandate | White | Gold | Crescent and star |
| Technocratic | Silver | Blue | Circuit and eye |

---

# Appendix C: Corporate Logos and Slogans

| Corporation | Slogan |
|-------------|--------|
| Nakamura Heavy | "Building Tomorrow's Fleet" |
| Red Star Mining | "Workers' Strength, Universal Resources" |
| Stellarwind | "Your Cargo, Our Priority" |
| Huang-Wei | "The Stars Within Reach" |
| Prometheus Arms | "Peace Through Strength" |
| Luxor | "Excellence in Every Detail" |
| Santos Agricultural | "Feeding the Future" |
| Okonkwo Fabrication | "Built to Last" |
| Novak Energy | "Power for the People" |
| Tanaka-Chen | "Health Across the Stars" |

---

# Document Control

**Version**: 1.0
**Date**: 2534-01-15 (in-universe) / 2025-12-11 (real-world)
**Author**: Universe Generation Team
**Status**: Specification for Phase 3 Implementation

**Dependencies**:
- Phase 0: star_catalog.csv
- Phase 1: system_objects.csv (natural objects)
- Phase 2: system_objects.csv (with artifacts)

**Outputs**:
- civilization.csv
- factions.csv
- corporations.csv
- timeline.csv

---

*End of Phase 3 Specification*
