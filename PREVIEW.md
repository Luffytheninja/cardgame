# Game Preview (Terminal Prototype)

This is a short captured run from the current CLI build.

```bash
python3 game.py
```

## Sample output excerpt

```text
Welcome to Ìrìn Àṣẹ: Descent from Òrún

Card art sources (license-free/open-license web images):
- Strike (Ogun): https://upload.wikimedia.org/wikipedia/commons/8/87/Ogun_shrine%2C_Lagos%2C_Nigeria.jpg [Wikimedia Commons (CC BY-SA)]
...
Web prototype reference:
- Not configured. Set WEB_PROTOTYPE_URL to display a live link.

========================================================================
Floor 1 The Descent: Learn basic attack and Àṣẹ use.
========================================================================

Enemies:
- Spirit Foe F1 (22 HP) intent ⚔ attack

HP 60/60 | Àṣẹ 3 | Block 0
Ifá Signature (4x2):
  . .
  . .
  . .
  . .
1. Strike (Ogun) [1] - Deal 6 damage. (art)
2. Defend (Obatala) [1] - Gain 5 Block. (art)
...
Play card #, 'art', 'link', or 'end':
```

## Readiness status

- **Android ready?** Not yet. Current codebase is a Python terminal game with stdin/stdout input. No Android packaging, touch UI, or mobile deployment pipeline exists.
- **Webapp ready?** Not yet. There is no frontend framework app in this repository (no React/Vue/Svelte app structure or web server routes), and gameplay is currently CLI-driven.

To make it Android- or web-ready, the next step is to separate game rules/state from CLI I/O and expose the game engine to a UI layer.
