# Session handoff — October 5, 2026

This is a navigation and continuity aid, not a replacement specification. Read the current phase contracts for full detail. Older entries in DECISIONS.md preserve history and can be superseded by later decisions.

## Resume here

We are discussing **M2 / Phase 3 initial conditions**, not implementing the simulator. After extensive qualitative economics and politics discussion, the user explicitly wanted to return to finishing the starting scenario. Continue one meaningful question at a time; avoid repeatedly asking about settled decisions or expanding into more Phase 4 rules.

The latest accepted decision assigns **Atlantic Union, Eurasian Directorate and West Asian League** as the former Ceres consortium's backers, contributing aerospace expertise, heavy engineering and finance respectively. Under the accepted mixed-recognition arrangement, these former backers dispute Commonwealth independence but continue trading.

Ceres broke away from this multinational mining consortium and took control of its facilities, leaving ownership, compensation and mineral-contract disputes. Consortium name and secession date remain open. **Do not assume that consortium is KVI.**

Next decide the recognition positions of the other five blocs, one meaningful question at a time. Do not invent a secession date or a war.

## Read first

1. [Repository instructions](../AGENTS.md).
2. [Project specification](PROJECT.md) and [roadmap](ROADMAP.md).
3. [Phase 2 closeout](PHASE_2_CLOSEOUT.md).
4. [Phase 3 current contract](phases/03-initial-scenario.md), especially opening diplomacy, accepted freight/passenger baselines and remaining initial-state work.
5. Relevant parts of [Phase 4](phases/04-history-simulation.md) and the latest [decision log](DECISIONS.md).

Archived documents are historical inputs, not authoritative requirements. Future-phase specifications do not imply working code.

## Repository state and verification

- Workspace: `/Users/hogsett/Documents/REPOS/CX16_Space_Game`.
- The user requested committing and pushing the accumulated design documentation on October 5. Check current git status and history for the outcome; preserve any subsequent uncommitted work.
- No Phase 3 initialization, Phase 4 history simulation or full game/export implementation was created in this design conversation. No generated datasets were changed.
- Recent checks are `git diff --check` and Python arithmetic for capacity proposals. These are **not** simulation, scheduling, economic-balance or emulator validation.
- Physical Phase 2 closeout records 63 passing tests from that earlier work. Do not report them as newly run.
- Do not commit, push, publish, regenerate physical data or implement new simulation behavior without a current request. Historical commit/push requests are not authorization for these new changes.
- No agent delegation is requested or required.

## How the user wants to work

- Keep abstractions simple. No individual-person simulation, detailed chemistry, city grids or hundreds of individual company agents.
- Ask material design questions one at a time, usually with a concise recommendation. Package related numerical choices into a table rather than querying every parameter.
- Record accepted choices in DECISIONS.md and the current contract; distinguish proposals from approvals. Use the actual session date for new log entries.
- Explain briefly what was recorded and checked. Do not call a phase complete based on documentation or arithmetic checks.
- Interacting simple rules should produce indirect consequences. The user's SimCity analogy was illustrative, not a request to add a property market or a direct pollution-to-crime rule.

## Accepted physical foundation and chronology

- Preserve `universe_builder/results/physical-phase2-v1/` and all earlier runs, baseline and HYG data. Accepted world: 170 connected systems, 274 natural objects, eight technology sites including Mars, 32 archaeology sites. Artifact map is omniscient developer output, never initial actor knowledge.
- Natural Sol objects are only Earth `(0,0)`, Luna `(0,1)`, Mars `(0,2)`, Ceres `(0,3)`. Preserve composite identities. Artificial stations require separate scenario identities. More natural Sol bodies require explicit extension, not silent edits.
- Simulation starts **April 5, 2148**, the Mars discovery date. This supersedes the preserved physical handoff's pre-epoch discovery premise without changing that dataset.
- Atlantic Union, Sino Cooperative Sphere and Indo-Pacific Compact jointly discover the artifact and sponsor Luna/Mars. Each sponsor has one vote in each joint authority, with separately owned assets possible.
- Discovery is secret. All three develop propulsion; Atlantic announces the first working prototype as a domestic breakthrough, concealing the artifact. First operational ships targeted around 2153; propulsion knowledge broadly diffuses around 2168 through research, personnel movement, espionage and licensing. Knowledge does not create ships or factories.
- Propulsion starts at 0.5 c and doubles each level, including FTL; no relativity/time dilation. Reach remains fixed at 9 ly. Upgrades require construction/refits.
- Early probe first, six-month initial survey, then ordinary light-speed radio report; colony launch follows receipt of viable findings. Later probes can establish power, communications, landing area and basic shelters. No automatic inhabited colony or FTL communications.
- The earlier 2162 colony target is superseded by actual travel/report/preparation delays. Approximately 2175 was only an illustration at 4.32 ly and 0.5 c, not a new fixed deadline.

## Starting actors and control

- Eight Earth blocs: Atlantic Union; Eurasian Directorate; Sino Cooperative Sphere; Indo-Pacific Compact; Indian Confederation; West Asian League; African Union; Southern Commonwealth. Detailed memberships and governments are in Phase 3; do not reopen them wholesale.
- Switzerland is neutral, outside the eight active blocs, has no space ambitions and continues providing security to Vatican City. No initial religious faction.
- Ceres: Belt Workers' Commonwealth, Commonwealth or slang **the 'wealth**; people are **'wealthers**. Strong local identity, elected councils/assembly. Independent but vulnerable to imported machinery/spares and a maintenance backlog.
- Named companies: **Meridian Shipping** and **Kessler-Voss Interstellar (KVI)**. Meridian emphasizes scheduled freight/passengers. KVI is a somewhat shady diversified conglomerate with freight at its core plus mining, shipbuilding and security.
- The user chiefly envisages the named firms as recognizable actors in the eventual game; modeling them during history generation is acceptable. There are also **hundreds of independent operators, abstracted**. Exactly two companies in the whole economy is superseded.
- Independent fleet pools are sized from local demand, counting named-company capacity first. They are not one centrally controlled faction or instant global spare capacity.
- The Mesh, also called the Null Collective, is decentralized, noisy and politically partisan; leaks can undermine opponents or assist technology diffusion. Three loose criminal networks: Ceres smuggling/spares, Luna dock theft/protection, mobile piracy. Names/assets unspecified.
- Every visitable body/station has one controller or is unclaimed. Other factions may have residents, offices, businesses and assets there. Multiple separately controlled settlements at one destination was superseded.
- Earth and its separate orbital port/shipyard use the **same shared port authority**. Luna and Mars each use a joint colonial administration as a single controller. Smaller Luna/Mars/Ceres facilities are included in their destinations.
- Earth orbital station: **100,000 permanent residents**, separate aggregate population. Whether allocated from or additional to the previous Earth total is still unresolved; do not silently change bloc totals. Station name and facility ownership allocations remain open.
- Opening April 2148: no major Earth-bloc war, but rivalry, espionage, commercial disputes, uneasy cooperation, Ceres tension and piracy.

## Population, industrial shares and supplies

Earth residents total 6.5 billion: Atlantic 1,000 million; Eurasian 300; Sino 1,200; Indo-Pacific 700; Indian 1,300; West Asian 400; African 1,100; Southern 490; neutral Switzerland 10.

Luna: 20 million. Mars: 50 million. On each, the three sponsors account for 30% each and the other five blocs 2% each. Ceres: 250,000, primarily 'wealthers. The orbital station is a separate population as above.

- Track aggregate communities/age cohorts, never billions of individual people. Routine crews are abstracted out of demographic transfers. Temporary travel uses seats without changing permanent populations. Relocation moves explicit aggregate counts through departure, transit and arrival.
- General industrial shares: Earth 80%, Luna 8%, Mars 11%, Ceres 1%. Ship assembly separately: Luna 47%, Mars 36%, Earth orbit 15%, belt 2%. Absolute capacity and orbital/belt attribution remain open; do not double count them.
- Standard food accounting: 2 kg per awake resident/day. Abstract water/ice/gases within broad materials categories; resource profile and facilities determine feasible production. Recycling/purification belong to life support, not separate substance inventories.
- Default stations import food/industrial supplies, maintain life support and hold six months of essential reserves. Future stocks must actually be delivered, not conjured by a template.

| Location | Daily food use | Local food production | Imported food |
|---|---:|---:|---:|
| Luna | 40,000 t | 4,000 t (10%) | 36,000 t |
| Mars | 100,000 t | 101,000 t (101%) | No baseline need; 1,000 t surplus before reserves/losses |
| Ceres | 500 t | 100 t (20%) | 400 t |
| Earth orbital station | 200 t | None allocated | 200 t |

Earth is the principal food supplier. Mars is only beginning to export. Luna reserves cover six months of normal essential imports; Ceres one year; Mars six months of basic consumption against production failures. Proposed day conventions 180/365 are not yet finalized. Earth reserves remain open.

## Transport baselines already accepted

- Cargo payloads: small 10,000 t; medium 50,000; large 100,000; heavy 450,000; super-heavy 1,000,000. Naval sizes exist but forces/capabilities remain deferred.
- Passenger sizes: 10 at the small end, accepted 100-seat intermediate transport, 1,000-seat standard liner, 50,000-settler colony transport. Small Serenity-like mixed ships are a qualitative reference; exact mixed payloads unassigned.
- Pre-discovery one-way travel: Earth–Luna 1 day, Earth–station 1, Earth–Mars 21, Earth–Ceres 35, Mars–Ceres 21. Travel halves per propulsion level to a one-day floor. Other routes unassigned.
- Two-day port turnaround at each call, independent of technology. Repeated round trip = twice one-way travel + four days. Do not count both arrival and departure handling twice at the same recurring call. Repairs are additional.
- Planning availability: 80% committed, 15% maintenance, 5% serviceable/uncommitted. Local, over time; not fractional physical ships or cargo-fill percentages. Initial integer schedules and locations remain unvalidated.

| Cargo service | Accepted hulls | Owner | Food + non-food outward per day | Non-food return per day |
|---|---|---|---:|---:|
| Earth–Luna | 6 medium | Meridian | 36,000 + 3,000 t | 2,000 t |
| Earth–Ceres | 4 small | KVI | 400 + 25 t | 400 t |
| Earth–station | 1 small | Meridian | 200 + 100 t | Unassigned |
| Earth–Mars | 2 medium | Meridian | 0 + 1,500 t | 1,000 t |

Thirteen assigned cargo ships are a limited baseline, **not all commercial traffic**. Figures are net trade/saleable-surplus targets, not gross industrial output or fixed manifests. Production, consumption, finance and scheduling still require reconciliation. Cargo mix follows known supply/demand and expected profit. Ceres exports mostly refined materials **on supply ships' return legs**, not an automatically separate fleet. Main final markets are Earth/Luna, smaller Mars; the detailed 240/120/40 onward split in the contract remains illustrative, not accepted. Mars food exports compete for return space; two medium ships allow about 1,739 t/day per direction, leaving about 739 t/day after the non-food return target.

| Routine passenger service | Typical passengers/day each direction | Ships | Meridian / independent |
|---|---:|---|---|
| Earth–Luna | 1,000 | 8 × 1,000 seats | 6 / 2 |
| Earth–station | 500 | 4 × 1,000 seats | 3 / 1 |
| Earth–Mars | 100 | 6 × 1,000 seats | 4 / 2 |
| Earth–Ceres | 10 | 10 × 100 seats | 0 / 10 |

Twenty-eight passenger ships are separate from cargo hulls. **These are typical initial flows, not fixed quotas**; the user explicitly clarified they rise/fall with circumstances. Relocation is additional demand using available capacity, not automatic extra seats. Charter/other independent services remain unassigned.

## Economy and later-history direction

Working twelve-category list: Raw Materials, Refined Materials, Industrial Goods, High-Tech Goods, Agricultural Goods, Consumer Goods (proposed consolidation includes luxuries), Medical Supplies, Fuel, Weapons, Narcotics, Black-Market Data, Alien Artifacts. The detailed capability table is still a proposal; do not treat every recipe or the full consolidation as separately approved numerical mechanics.

- Artifacts and Black-Market Data trade through black markets, not ordinary markets. Narcotics legality varies; weapons require authorization. Other goods normally legal, subject to embargoes/emergency restrictions. Black markets need contacts or criminal reputation and can be disrupted.
- Supply/demand and transport cost drive trade and carrier allocation. Settlements may pay high freight prices, acquire fleets or attract new entrants. Reassignment takes time and honors commitments; no free ships or instant knowledge.
- Production follows resources, facilities, technology, inputs, labor/automation and population conditions. Natural suitability affects viability; imports can support industry. No automatic illicit output because a community has technical/agricultural skills.
- Accessible resources deplete; technology can improve extraction and accelerate depletion. New deposits can be opened. Economic roles can shift from mining to manufacturing/services, without a mandatory ladder.
- Governments and corporations invest for survival, strategy, profit and influence. Corporate concessions, covert support for opposition, nationalization, new breakaway factions, alliances, unions and mergers are accepted possibilities, not scripted outcomes.
- Migration responds to opportunity and hardship, including war/refugees. Funding can be personal, employer or government. Admission policy differs from public acceptance. Integration can be uneven; segregation possible. Community conditions and trust differ within a settlement. Poverty can raise crime risk without making it automatic or inherent to ancestry.
- Governments can offer relief/services/jobs, adjust migration policy or increase security. Unrest may escalate or subside; rebellion needs organization/resources as well as dissatisfaction.
- Foreign peaceful trade is normally admitted; hostility/low disposition may deny access and extreme hostility may provoke security attacks. Separate signed faction/local visitor dispositions are accepted direction. The suggested −100 to +100 addition formula was not conclusively incorporated into the specs; thresholds remain open. Visitor disposition is not residents' trust in government.
- Cryosleep, embryo/livestock cargo and artificial gestation are accepted abstractions; normal maturation around 18. Small routine losses/occasional severe failures. Five years of colony food after arrival, additional transit supplies; favorable colony food self-sufficiency target about three years.

## Remaining Phase 3 work and cautions

Continue initial-state decisions, not endless new qualitative rules:

1. Recognition positions of the five blocs outside the former Ceres consortium; any other necessary opening relationships. Dates and incidents need explicit authorship.
2. Station population-total relationship, facility asset ownership/capacity attribution, and any genuinely needed extra starting locations.
3. Gross commodity production/consumption, construction capacity, starting reserves and funds sufficient to support accepted net trade. Existing fleet ceilings do not prove economic viability.
4. Remaining government research/support assets and other independent/charter capacity, sized to actual needs. Heavy/super-heavy initial allocations are unassigned. Military detail is deferred until needed.
5. Aggregate community/age profiles, initial conditions and research/knowledge records, naming/language sources. The small set of high-level identities already accepted is not a complete dataset.
6. Concrete schema/units and meaningful initializer validation before implementation can be called complete.

The roadmap and remaining-work table contain some broad/stale wording. Read later accepted sections before treating a value as unknown. In particular, initial passenger sizes/counts, net trade volumes and the station population count are now accepted. The very long Phase 3 document also contains later-history direction duplicated into Phase 4; do not mistake it for a requirement to implement every mechanism in the initializer.

Do not equate aggregate trade categories with fungible chemistry or invent missing physical deposits. Do not treat speculative archived wars, factions, commodity prices or legality details as current canon. The separately accepted political/naming history must not be lost when restructuring documents.

## Game presentation reminder

Text-only vintage terminal appearance, 7-bit ASCII content, proposed 8 colors plus bright bit; X16 glyphs may decorate borders. No sprites. Simple eventual port menu: goods market, ship services, mission board, with possible trade union, faction and black-market interfaces. No interface implementation requested now.
