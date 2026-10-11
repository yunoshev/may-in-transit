# MAYA / ARI — SOLO JOVIAN VEHICLE
## 3D Build & Interior Specification — v0.1

**Purpose:** canonical reference for building the spacecraft exterior and the hero interior set in Blender.

**Design goal:** the ship must look functional, explainable, internally consistent, and cheap enough to reuse for a long-running vertical-video series.

**Crew:** 1 — Maya  
**Ship AI:** ARI  
**Nominal habitat gravity:** 0.5 g  
**Primary destination for Season 1:** Jupiter system / Europa  
**Era:** fictional 2050s

---

# 1. Canonical ship architecture

## 1.1 Overall geometry

The ship uses a long central spine aligned with the main thrust axis.

The complete spacecraft rotates around this longitudinal axis during normal cruise / coast operations.

Two radial structures extend from the spine:

- **Habitat pod** — Maya's pressurised living and working module.
- **Counterweight / service pod** — tanks, stores, machinery and other mass used to balance the rotating system.

The habitat floor is approximately **28 m from the rotation axis**.

At approximately **4 rpm**, this produces approximately **0.5 g at the habitat floor**.

Simplified external layout:

```text
                         FORWARD / FLIGHT AXIS
                                  ↑
                                  |
                           sensor / comms
                                  |
                                  |
               HABITAT POD       ||       COUNTERWEIGHT
                    [H]----------||----------[S]
                         ~28 m    ||   ~variable
                                  ||
                                  ||
                             CENTRAL SPINE
                                  ||
                           propellant / power
                                  ||
                              radiators
                                  ||
                           reactor / power
                                  ||
                          axial propulsion
                                  ↓
                                 AFT
```

The habitat and counterweight rotate around the vertical axis shown above.

The main engines are placed close to the spin axis and thrust along that axis.

### Production assumption

For major attitude changes, the vehicle may reduce its spin rate. Axial cruise thrust can be treated as compatible with the spin configuration in our fictional design.

We do **not** need to show this process in early episodes.

---

# 2. Why this architecture was chosen

The design minimizes the need for a giant continuously operating rotary bearing between a stationary ship and a rotating living section.

It also gives the show a persistent **0.5 g interior**, so:

- Maya can sit normally;
- coffee stays in a cup;
- loose objects fall toward a floor;
- clothes hang downward;
- hair behaves broadly like hair in partial gravity;
- the interior can be animated with conventional character tools.

The rotating-vehicle concept is grounded in real artificial-gravity studies, but the exact ship is fictional.

---

# 3. Habitat pressure vessel

## Canonical modelling dimensions

These are **fictional design dimensions**, chosen for visual and production practicality.

### Outer pressure shell

- approximate internal diameter: **2.8 m**
- approximate internal length: **6.0 m**
- gross cylindrical internal volume: roughly **37 m³**
- target usable human volume after racks, tanks, insulation and equipment: roughly **24–28 m³**

The interior should **not** feel like a luxury apartment.

It should feel like:

> a compact camper van + research workstation + aircraft cabin + small submarine compartment.

The module is large enough for one person to live in for extended active periods, but every surface has a purpose.

---

# 4. Coordinate convention for Blender

Recommended canonical coordinates:

```text
+X = forward / direction of main thrust
-X = aft

+Z local habitat = inward toward spacecraft rotation axis
-Z local habitat = floor / artificial-gravity "down"

Y = left / right across cabin
```

For normal interior shots:

```text
Blender scene gravity:
Z = -4.905 m/s²
```

The interior set itself does not need to spin.

The rotating reference frame is approximated as a normal room with 0.5 g for routine production shots.

---

# 5. Interior plan

The habitat is one main multifunctional room with several compact enclosed or semi-enclosed sub-zones.

Do **not** build a separate cinematic bridge, dining room, bedroom and laboratory.

For a one-person ship, that wastes mass and production effort.

Recommended plan:

```text
                FORWARD
        ┌───────────────────────┐
        │  AXIAL VIEW WINDOW    │
        │     + SHUTTER         │
        ├───────────────────────┤
        │                       │
        │  A       MAIN       B │
        │      WORK / VLOG      │
        │        CABIN          │
        │                       │
        │ GALLEY       STORAGE  │
        │                       │
        ├──────────┬────────────┤
        │ HYGIENE  │ STASIS /   │
        │  WC      │ SLEEP /    │
        │          │ SHELTER    │
        ├──────────┴────────────┤
        │ ECLSS / SERVICE WALL  │
        ├───────────────────────┤
        │ HATCH TO BOOM / SPINE │
        └───────────────────────┘
                 AFT
```

The exact left/right placement can change for composition, but the functional relationships should remain.

---

# 6. Zone A — Main command / work / vlog station

This is the **hero set**.

It appears in most episodes.

## Furniture

- one fixed / semi-adjustable chair;
- compact desk / console;
- one fold-out work surface;
- footrest;
- handhold / structural rail;
- small personal shelf.

At 0.5 g the chair does not need microgravity restraints for routine use, but a light lap restraint can exist for high-thrust manoeuvres.

## Displays

Avoid giant fantasy holograms.

Use:

### Primary display
Approximately 32–40 inch equivalent.

Functions:

- trajectory;
- navigation;
- scientific data;
- exterior camera views;
- communications;
- ARI visual output.

### Secondary display
Approximately 20–27 inch equivalent.

Functions:

- ship status;
- checklists;
- telemetry;
- life support;
- timers.

### Thin status strip
Always visible.

Suggested data:

- ship time;
- acceleration state;
- spin / gravity status;
- cabin pressure;
- oxygen status;
- CO2 status;
- water reserve;
- next manoeuvre;
- communications delay.

## Physical controls

Most interaction can be touch / voice, but the model should contain a small group of clearly physical controls for:

- emergency power;
- communications;
- fire isolation;
- hatch control;
- manual propulsion inhibit;
- life-support override.

These should look guarded and difficult to activate accidentally.

---

# 7. ARI — AI interface

ARI has **no humanoid body and no permanent face**.

ARI exists through the ship.

## Visible ARI elements

- microphones integrated into ceiling / console;
- small speaker grilles;
- subtle status light;
- waveform or icon on displays;
- highlighted UI elements;
- text captions when useful.

## Normal interaction

Maya speaks naturally:

> "ARI, put the Europa trajectory on the main screen."

ARI answers through cabin speakers.

Maya can interrupt ARI.

ARI can change what is displayed without Maya touching the console.

This should feel like a very advanced operating system rather than a second physical character.

---

# 8. Forward observation window

The window is important for the series but should not dominate the pressure vessel.

## Canonical design

One **axial forward-facing window**.

Suggested visible opening:

- around **0.8–1.0 m wide**
- around **0.45–0.65 m high**

The window looks along the spacecraft's rotation axis.

Therefore Jupiter / Europa does not rotate around the cabin view as the ship spins.

## Exterior shutter

The window has a heavy motorised external or internal protective shutter.

Possible uses:

- radiation protection;
- micrometeoroid protection;
- thermal control;
- sleeping / blackout;
- cinematic reveal.

Most navigation can still rely on exterior cameras rather than the window.

---

# 9. Galley

The galley occupies one wall beside the main work station.

It is small.

## Model these elements

- potable-water dispenser;
- hot-water outlet;
- food warmer;
- compact refrigeration drawer;
- sealed food storage drawers;
- utensil drawer;
- mug slot / cup holder;
- small wipe-clean worktop;
- waste bag / organic waste drawer;
- cleaning cloth / wipes storage.

## Do not model

- open flame;
- domestic gas stove;
- giant refrigerator;
- full kitchen sink;
- large dishwasher.

Maya should be able to make:

- coffee;
- tea;
- rehydrated meals;
- heated packaged food;
- simple fresh-food items during early mission phases.

---

# 10. Hygiene / WC compartment

A small closable cubicle.

It should have a real door or sliding privacy panel.

## Contents

- toilet;
- compact handwash basin;
- hygiene-water nozzle;
- mirror;
- towel / drying cloth;
- toothbrush / personal-care drawer;
- medical / hygiene consumables;
- ventilation grille;
- waste service access.

## Canonical fictional choice

Because the habitat has 0.5 g, the toilet can visually resemble a compact terrestrial marine / aircraft toilet more than an ISS microgravity toilet.

However, it still uses controlled airflow / vacuum assistance and closed waste handling.

## Shower

Do **not** build a large shower.

If desired, include:

- seated / standing wash area;
- retractable spray wand;
- water capture lip;
- air-drying system.

This is future-tech extrapolation.

---

# 11. Stasis / sleep / radiation shelter

This is one compartment serving **three functions**.

It is positioned in the most shielded part of the habitat.

## Stasis pod

The pod is a fixed enclosed berth.

It should look medical / aerospace rather than magical.

Visible elements:

- padded interior;
- transparent or partially opaque lid;
- physiological sensor connectors;
- IV / fluid interface points;
- air circulation;
- emergency mechanical release;
- local screen;
- ARI camera / microphone;
- small service panel.

The pod itself does not need to appear in the first episodes.

A closed hatch labelled something like:

`SLEEP / MED / SAFE`

is enough until needed.

## Radiation shelter concept

Dense mission supplies are arranged around this compartment.

Useful surrounding masses:

- water;
- food;
- hygiene supplies;
- waste-water tanks;
- equipment;
- polyethylene-rich materials.

The shelter is therefore not a separate giant bunker.

The ship uses material that already has to be carried.

This is grounded in real spacecraft radiation-protection thinking, but the exact effectiveness of our fictional arrangement is not specified.

---

# 12. ECLSS / life-support service wall

This wall makes the ship believable.

Do not hide all life support behind magical panels.

At least some filters, access doors, labels and maintenance points should be visible.

## Functional blocks

### Air circulation
- circulation fans;
- return-air grille;
- particulate filters;
- replaceable filter cartridges.

### CO2 removal
- regenerable CO2 scrubber unit;
- emergency backup cartridges.

### Trace contaminant control
- filter / catalytic treatment section.

### Oxygen management
- oxygen-generation unit;
- emergency high-pressure oxygen reserve.

### Humidity control
- condenser;
- condensate collection.

### Water recovery
- greywater collection;
- humidity condensate recovery;
- urine-processing connection;
- water purification;
- potable-water tank.

### Cabin monitoring
Sensors for:

- pressure;
- oxygen;
- carbon dioxide;
- humidity;
- temperature;
- smoke / combustion products.

## Visual design rule

The life-support system should look like:

> several maintainable appliance-sized modules,

not one unexplained glowing box.

Give Maya removable filters, cartridges and inspection covers she can interact with in future episodes.

---

# 13. Water architecture

Water is one of the most useful masses on the ship.

## Tanks

Do not place all water in one tank.

Distribute water around:

- stasis / shelter area;
- aft equipment wall;
- floor / structural cavities where practical.

Reasons in our fictional design:

- balance;
- redundancy;
- radiation shielding;
- easier packaging.

## Visible plumbing

Only a little plumbing should be exposed.

Use:

- labelled access panels;
- colour-coded service lines;
- inspection ports;
- small transparent diagnostic section if desired.

Avoid steampunk pipe forests.

---

# 14. Food storage

For an interplanetary mission, storage should occupy a surprisingly large fraction of the cabin.

Use wall-depth lockers everywhere.

## Storage categories

- daily food;
- reserve food;
- beverages;
- medical consumables;
- clothing;
- replacement filters;
- repair parts;
- personal items.

Many wall panels that look decorative should actually be doors.

This gives the set visual density without making it random.

---

# 15. Exercise equipment

Even with 0.5 g, the ship carries compact exercise hardware as a conservative mission-design choice.

Do not dedicate a whole gym.

Use fold-away systems.

## Suggested hardware

### Fold-out resistance station
- cable resistance;
- handles;
- foot plate;
- shoulder harness / bar attachment.

### Compact cycle
Either:
- fold-down pedals and seat;
or
- under-desk / wall-mounted cycle system.

Everything folds flat against the wall when not used.

This provides future vlog scenes without requiring a new room.

---

# 16. Medical equipment

One compact medical locker beside the stasis / shelter area.

## Visible items

- first-aid modules;
- medications;
- diagnostic scanner / ultrasound-like device;
- blood-pressure / vital-sign equipment;
- wound-care materials;
- injectors;
- splints;
- emergency oxygen mask;
- portable defibrillator-like unit;
- sterilisation pouch / cabinet.

Most advanced diagnosis can be mediated by ARI.

Avoid a full hospital bed.

The stasis berth doubles as the medical bed.

---

# 17. Clothing / personal storage

Maya needs very little dedicated wardrobe space.

Model:

- two or three shallow drawers;
- hanging rail / hooks;
- laundry bag;
- shoe / slipper pocket;
- folded clothing bins.

Clothes should appear repeatedly across episodes.

Continuity is more important than variety.

---

# 18. Laundry

Do not model a full domestic washing machine.

Canonical solution:

- most daily clothing is designed for extended wear;
- spot cleaning;
- wipe / steam cleaning;
- small sealed fabric-cleaning drawer for occasional cycles.

The exact technology is fictional.

This system can remain mostly hidden.

---

# 19. Cleaning

Model a small cleaning locker containing:

- wipes;
- compact vacuum;
- surface cleaner;
- brush;
- waste bags;
- filter masks;
- gloves.

This creates ordinary maintenance scenes.

---

# 20. Waste management

Waste is divided into:

- biological waste;
- dry trash;
- packaging;
- recyclable / processable material;
- hazardous waste.

Use compact sealed drawers / canisters.

Do not have random garbage floating or piled around the cabin.

The ship is small enough that Maya must remain organised.

---

# 21. Fire safety

Visible safety hardware should include:

- smoke / combustion sensors;
- portable extinguisher;
- fire mask / emergency breathing mask;
- isolation controls;
- labelled electrical cut-offs.

ARI continuously monitors the cabin.

This is not intended as a disaster plot device.

It simply makes the ship look designed by engineers.

---

# 22. Emergency / survival equipment

One clearly labelled emergency locker.

Contents implied or partially visible:

- emergency breathing mask;
- pressure hood / emergency suit;
- portable oxygen;
- medical kit;
- emergency food / water;
- flashlight;
- manual tools;
- thermal layer;
- locator / communication device.

No need for a full EVA suit in Season 1 unless later scripts require it.

---

# 23. Tool and repair storage

Maya should plausibly be able to replace modules.

Model one technical drawer system containing:

- screwdrivers / powered driver;
- torque tools;
- multimeter;
- diagnostic tablet;
- cable ties;
- connectors;
- sealant patches;
- spare valves;
- spare fan;
- filters;
- fuses / power modules.

Most spacecraft maintenance in the series should be:

> remove panel → diagnose replaceable module → swap module → run ARI test.

This is far easier to animate than complex mechanical repair.

---

# 24. Lighting

The cabin uses layered lighting.

## A. General cabin light
Soft ceiling / wall strips.

## B. Task lighting
At desk, galley, hygiene area and service wall.

## C. Night mode
Very dim low-level lighting.

## D. Camera / vlog light
A small adjustable panel near Camera A.

Do not make the entire ship blue.

Most surfaces should be neutral white / warm grey, with colour coming from displays, status lights and occasional night modes.

---

# 25. Acoustic / ventilation cues

The ship should not be silent.

Persistent background sound can include:

- low ventilation noise;
- quiet pump / fan tones;
- occasional relay clicks;
- distant structural creaks;
- ARI notification tones.

These sounds imply systems we do not need to render.

---

# 26. Cameras

The ship has three canonical interior cameras.

## Camera A — main vlog camera
Position:
- forward quarter of main cabin;
- near eye level;
- good view of Maya + workstation + axial window.

This is the primary 9:16 shot.

## Camera B — wide cabin camera
Position:
- upper aft corner;
- wider view of work area + galley + some service wall.

Used for:
- casual work;
- cooking;
- exercise;
- cleaning.

## Camera C — workstation / close camera
Position:
- close to main display;
- slightly off-axis.

Used for:
- personal diary;
- ARI conversations;
- science / trajectory explanations.

### Exterior cameras

The ship also has exterior feeds:

- forward navigation;
- aft propulsion;
- habitat exterior;
- boom / structural inspection;
- wide Jupiter-facing science camera.

These can be rendered separately.

---

# 27. Interior materials

The interior should feel industrial but lived-in.

## Main palette

- off-white structural panels;
- warm grey;
- dark graphite equipment faces;
- brushed aluminium details;
- black seals / joints;
- occasional yellow or orange safety markings.

## Soft materials

Use limited textiles:

- seat upholstery;
- stasis padding;
- curtain / privacy panel;
- small rug-like anti-slip deck section if desired.

Avoid luxury leather and glossy sci-fi plastic.

---

# 28. Surface details that make the set believable

Add:

- serial numbers;
- maintenance dates;
- fasteners;
- removable panel seams;
- handles;
- vents;
- cable pass-throughs;
- Velcro-like attachment zones;
- emergency labels;
- small scratches;
- hand-written note;
- one or two stickers;
- Maya's personal objects.

Do not cover every surface with meaningless futuristic glyphs.

Most labels should be boring.

Examples:

```text
AIR RETURN
FILTER A
POTABLE H2O
SERVICE ACCESS
EMERGENCY O2
BUS B
CABIN FAN 2
WASTE PROC
MANUAL RELEASE
```

---

# 29. The "hero wall"

One side of the main cabin should become the recognisable visual identity of the series.

It contains:

- primary display;
- ARI status indicator;
- physical emergency switches;
- a few exposed structural ribs;
- shallow storage;
- small personal shelf;
- part of the axial window in frame.

This wall should appear in thumbnails repeatedly.

The audience should recognise the show before seeing Maya's face.

---

# 30. Exterior-to-interior continuity

The 3D model must make it possible to understand where the room exists inside the exterior vehicle.

For every visible interior feature, define an exterior counterpart where appropriate:

- window;
- pressure shell;
- hatch;
- boom attachment;
- radiator / thermal lines;
- camera housing;
- antennas.

Avoid impossible TARDIS geometry.

---

# 31. What is NOT inside the habitat

To keep the set minimal, the following systems are mostly outside the pressure cabin:

- main reactor;
- main propulsion;
- large propellant tanks;
- large radiators;
- high-power converters;
- main communications antenna;
- heavy science instruments;
- most spare machinery.

The habitat contains interfaces and monitoring hardware, not the whole spacecraft.

---

# 32. Service / counterweight pod

The opposite radial pod does not need an interior set initially.

It can contain:

- water reserve;
- propellant or inert consumables;
- dry stores;
- replaceable hardware;
- batteries / power electronics;
- science payloads;
- waste storage.

Its mass can be adjusted in the fictional design to keep the rotating vehicle balanced as consumables move.

ARI manages balance automatically.

Exact balancing hardware is a design assumption.

---

# 33. Minimum assets for Season 1

## Must model at high fidelity

1. Maya character.
2. Main habitat shell.
3. Main workstation.
4. Chair.
5. Forward axial window + shutter.
6. Primary and secondary displays.
7. Galley wall.
8. Hygiene/WC door and visible interior.
9. Stasis/sleep/shelter hatch.
10. ECLSS service wall.
11. Storage doors.
12. Fold-out exercise system.
13. Medical locker.
14. Hero props.
15. Three cameras.
16. Lighting fixtures.

## Hero props

- mug;
- spoon;
- tablet;
- headset / earbuds;
- water bottle;
- one notebook;
- pen;
- small tool;
- towel;
- food package;
- small plant or personal decorative object.

These should persist between episodes.

---

# 34. Can be implied rather than fully modelled

Initially, do **not** spend production time fully modelling:

- reactor internals;
- electric propulsion internals;
- plumbing behind every panel;
- full stasis machinery;
- service pod interior;
- entire boom interior;
- complete waste processor;
- every tank;
- every medical device.

Use access panels, labels and occasional cutaway graphics.

If an episode later needs a system, build that system then.

---

# 35. Suggested Blender collection structure

```text
SHIP
├── EXT_SPINE
├── EXT_HAB_POD
├── EXT_SERVICE_POD
├── EXT_BOOMS
├── EXT_PROPULSION
├── EXT_RADIATORS
├── EXT_ANTENNAS
├── EXT_CAMERAS
│
├── INT_HAB_SHELL
├── INT_STRUCTURE
├── INT_WORKSTATION
├── INT_GALLEY
├── INT_HYGIENE
├── INT_STASIS
├── INT_ECLSS
├── INT_STORAGE
├── INT_MEDICAL
├── INT_EXERCISE
├── INT_LIGHTING
│
├── PROPS_STATIC
├── PROPS_RIGIDBODY
├── CHARACTER_MAYA
├── CHARACTER_CLOTH
├── CHARACTER_HAIR
│
├── CAMERA_A_VLOG
├── CAMERA_B_WIDE
├── CAMERA_C_CLOSE
└── CAMERA_EXTERNAL
```

Recommended working scale:

**1 Blender unit = 1 metre**

---

# 36. ARI interaction surfaces

Every screen should be controllable by ARI.

Useful reusable screen templates:

1. orbital map;
2. system schematic;
3. Europa / Jupiter camera feed;
4. science image;
5. life-support status;
6. communications message;
7. checklist;
8. maintenance diagram;
9. timeline;
10. simplified "viewer explanation" diagram.

This is important because it lets dialogue create visual variety without rebuilding the set.

---

# 37. Canonical everyday blocking

Most shots should use a small set of repeatable positions.

## Position 1 — chair
Maya at command station.

## Position 2 — lean
Maya leaning against desk / galley.

## Position 3 — standing at window
Maya beside axial window.

## Position 4 — galley
Maya making coffee / food.

## Position 5 — service wall
Maya replacing filter / checking system.

## Position 6 — floor exercise
Maya using resistance system.

These six positions can support dozens of episodes.

---

# 38. Reality basis — VERIFIED

The following design principles are grounded in current crewed-spacecraft practice or active human-spaceflight design work.

## Multifunctional compact habitat

NASA describes Gateway HALO as a compact environment where exercise, hygiene and storage functions share the same limited space.

ESA describes Lunar I-Hab as a roughly 10 m³ living module serving sleeping, dining, exercise and medical functions for visiting crew.

**Sources:**
- NASA — Gateway: The Lunar Space Station  
  https://www.nasa.gov/podcasts/houston-we-have-a-podcast/gateway-the-lunar-space-station/
- ESA — Gateway: Lunar I-Hab  
  https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/Gateway_Lunar_I-Hab

## Regenerative life support

NASA ECLSS documentation describes air revitalisation, oxygen generation, water recovery, waste handling and cabin-environment monitoring as core spacecraft life-support functions.

ESA independently describes air revitalisation systems removing CO2 and trace contaminants, and water-recovery systems processing urine, perspiration and hygiene water.

**Sources:**
- NASA — Environmental Control and Life Support Systems (ECLSS)  
  https://www.nasa.gov/reference/environmental-control-and-life-support-systems-eclss/
- ESA — Air Revitalization System  
  https://www.esa.int/content/view/full/194826
- ESA — Water Recovery System Racks  
  https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/Node-3_Cupola/Water_Recovery_System_Racks

## Crew functions: food, hygiene, waste, exercise and sleep

NASA's Orion crew accommodations include drinking water, food warming, a compact toilet and exercise hardware.

ESA's Lunar I-Hab explicitly includes sleeping, dining, exercise and medical areas.

**Sources:**
- NASA — Meet NASA's Orion Spacecraft  
  https://www.nasa.gov/missions/meet-nasas-orion-spacecraft/
- ESA — Gateway: Lunar I-Hab  
  https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/Gateway_Lunar_I-Hab

## Using carried material for radiation sheltering

NASA describes Orion crew using stowage areas and dense onboard material as shelter during a solar-radiation event.

ESA has studied water as radiation shielding and has also studied placing life-support / water-containing material around protected crew areas.

**Sources:**
- NASA — Meet NASA's Orion Spacecraft  
  https://www.nasa.gov/missions/meet-nasas-orion-spacecraft/
- ESA — For astronaut radiation protection, just add water  
  https://www.esa.int/Enabling_Support/Space_Engineering_Technology/For_astronaut_radiation_protection_just_add_water
- ESA — ESA engineers assess Moon Village habitat  
  https://www.esa.int/Enabling_Support/Space_Engineering_Technology/CDF/ESA_engineers_assess_Moon_Village_habitat

## Rotating artificial gravity

NASA technical work and peer-reviewed literature both use the relation:

`a = ω²r`

for rotational artificial gravity.

A radius near 28 m at approximately 4 rpm therefore gives approximately 0.5 g at the floor.

**Sources:**
- NASA NTRS — Development and Comparison of an Artificial Gravity Concept for Human Spaceflight  
  https://ntrs.nasa.gov/citations/20205004959
- Frontiers in Systems Neuroscience — Artificial gravity as a countermeasure for mitigating physiological deconditioning during long-duration space missions  
  https://www.frontiersin.org/journals/systems-neuroscience/articles/10.3389/fnsys.2015.00092/full

---

# 39. NOT CONFIRMED / FICTIONAL TECHNOLOGY

The following are not established present-day capabilities:

- human stasis for multi-year interplanetary travel;
- a crewed Jupiter mission;
- this exact rotating one-person spacecraft;
- continuous 0.5 g as an operational human-spaceflight standard;
- ARI-level general-purpose autonomous ship AI;
- the proposed compact shower / laundry systems;
- the exact radiation shielding performance of our layout;
- the exact reactor and propulsion package;
- a 2050s Starship launch / assembly chain for this vehicle.

These are worldbuilding assumptions.

---

# 40. DESIGN ASSUMPTIONS

These are choices made for the show, not claims about real spacecraft:

- Maya has around 24–28 m³ of usable habitat volume.
- The habitat floor radius is ~28 m.
- Normal spin is ~4 rpm.
- Floor gravity is fixed at 0.5 g.
- The whole gravity-producing structure rotates.
- The main forward window looks along the spin axis.
- The stasis berth doubles as a medical berth and radiation shelter.
- Most propulsion and high-power equipment is outside the pressure cabin.
- ARI controls almost all routine ship functions by voice.
- Maya can manually override safety-critical systems.
- The opposite pod serves as service mass / counterweight.
- Major attitude changes may be performed at reduced spin.

---

# 41. Visual north star

The interior should pass this test:

> If Maya disappeared from the frame, would the room still look like a machine designed to keep one human alive for years?

Every visible object should have one of four reasons to exist:

1. keep Maya alive;
2. operate the spacecraft;
3. perform the mission;
4. make long isolation psychologically tolerable.

If an object has no reason to exist, remove it.

The ship should feel dense, practical and lived in — not futuristic for the sake of looking futuristic.
