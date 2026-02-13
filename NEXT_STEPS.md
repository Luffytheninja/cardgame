# What we need next

This project has a good narrative skeleton, but it now needs a focused "vertical slice" polish pass.

## 1) Core gameplay correctness (highest priority)

- **Implement status effects fully**
  - `weakened` is set by enemy debuffs but currently does not reduce outgoing player damage.
  - Add turn duration tracking and effect resolution.
- **Fix Curse behavior**
  - Curse cards should typically be unplayable and mostly exist as deck-cloggers.
  - Current implementation treats Curse as a normal playable cost-1 card.
- **Make combo rules explicit**
  - Addition Mod 2 currently checks if both card names appear in a turn and then applies flat damage.
  - Add deterministic transformation rules (order, timing window, and exact outcome).

## 2) Floor tutorial fidelity (requested design alignment)

- **Floor-gate node types**
  - Enforce node-level tutorial rails: guaranteed Monster on Floor 1, no Elites before Floor 6, guaranteed Treasure on Floor 9.
- **Teach each floor with constrained card pools**
  - Introduce mechanics one by one (e.g., no Ifá combo before Floor 7).
- **Intent puzzle readability**
  - Show current and next intent cycles in a clearer HUD line.

## 3) World structure and navigation

- **Build the 7x15 irregular isometric map layer**
  - Current game is linear floor progression only.
  - Add branching path choices that affect risk/reward and spiritual alignment.
- **Alignment system**
  - Track Ire/Osogbo and Ori affinity as persistent run-state modifiers.

## 4) Content expansion and balance

- Add distinct enemy kits for each floor band.
- Add 20-30 more cards across Ogun/Ọbatala/Ọṣun/Ṣàngó archetypes.
- Add relic pool with rarity and synergy tags.
- Introduce score/multiplier system tied to Odù completion and efficient turns.

## 5) Engineering quality

- **Refactor into modules**
  - Suggested split: `cards.py`, `combat.py`, `map.py`, `events.py`, `data/*.json`.
- **Automated tests**
  - Unit tests for damage math, block decay, draw/discard reshuffle, combo resolution, and floor constraints.
- **Seeded runs**
  - Add optional RNG seed CLI argument for reproducibility and balancing.

## Suggested immediate milestone (next PR)

Deliver a "Tutorial Vertical Slice v2" that includes:
1. Correct status/curse/combo rules,
2. Floor constraints enforcement,
3. A minimal 7x15 node map with branching,
4. 10-15 deterministic tests.

This would move the project from prototype to reliable playable foundation.
