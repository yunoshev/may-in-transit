# Maya / ARI Space Vlog — Engineering Wiki Index

## Purpose

This wiki is the canonical technical and creative reference for the Maya / ARI space-vlog project.

The workflow is:

IDEA → TECHNICAL WIKI → ANATOMY DIAGRAMS → DESIGN REVIEW → CANON FREEZE → BLENDER BLOCKOUT → HIGH-FIDELITY MODELLING → PHYSICS / CHARACTER / CAMERA SETUP → RENDER → VIDEO-TO-VIDEO REALISM PASS

## Canon hierarchy

When documents disagree, use this order:

1. newest explicit design decision;
2. ship technical specification;
3. mission / physics documentation;
4. series concept;
5. episode-specific notes.

## Documentation rules

Every technical document should distinguish:

### Verified
Information supported by reliable real-world sources.

### Fictional assumption
Technology or mission capability accepted as part of the 2050s setting.

### Production decision
A choice made for visual consistency, renderability, or production cost.

## Current wiki files

### 00_project_wiki_index.md
This index.

### space_vlog_series_concept_v2.md
Primary creative series bible.

### maya_ari_ship_3d_build_spec.md
Primary spacecraft and interior build specification.

### anatomy_prompts.md
Prompt library for Anatomy technical visualizations.

## Proposed future wiki files

- 01_mission_architecture.md
- 02_spacecraft_exterior.md
- 03_habitat_interior.md
- 04_artificial_gravity.md
- 05_life_support.md
- 06_ari_system.md
- 07_visual_language.md
- 08_asset_register.md
- 09_science_reference.md

## Design workflow

### Phase A — Concept
Define what a system does, why it exists, and whether Maya interacts with it.

### Phase B — Technical note
Document function, dimensions, interfaces, maintenance, verified basis, fictional assumptions, and production decisions.

### Phase C — Anatomy diagram
Generate overview, cutaway, exploded view, or subsystem schematic.

### Phase D — Review
Check:
1. component purpose;
2. maintenance access;
3. exterior/interior consistency;
4. unnecessary complexity;
5. production cost;
6. contradictions with other wiki pages.

### Phase E — Canon freeze
Update the wiki, assign canonical dimensions, and freeze the accepted design.

### Phase F — Blender
Blockout → human-scale check → cameras → exterior/interior alignment → final geometry → materials → physics → lighting → render tests.

## Initial diagram roadmap

1. Full spacecraft overview
2. Full spacecraft exploded view
3. Habitat cutaway
4. Artificial-gravity geometry
5. Life-support schematic
6. Water / radiation layout
7. ARI system architecture
8. Camera plan
9. Jupiter arrival / Jovian tour

## Before Blender — minimum freeze checklist

- [ ] habitat diameter
- [ ] habitat length
- [ ] rotation radius
- [ ] target rpm
- [ ] 0.5 g reference location
- [ ] exterior window location
- [ ] workstation location
- [ ] galley location
- [ ] hygiene compartment location
- [ ] stasis / shelter location
- [ ] ECLSS wall
- [ ] storage depth
- [ ] camera A / B / C positions
- [ ] main display size
- [ ] service hatch positions
- [ ] exterior habitat geometry
- [ ] boom attachment geometry
- [ ] counterweight concept
- [ ] central-spine diameter
- [ ] radiator concept
- [ ] propulsion concept
- [ ] reactor / power placement

## Production north star

The purpose of the wiki is not endless documentation.

The purpose is to make Blender modelling boring and deterministic.

By the time modelling starts, the artist should not be inventing the spacecraft. They should be building an already-defined machine.
