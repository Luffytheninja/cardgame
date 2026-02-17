# Ìrìn Àṣẹ: Descent to Ilé-Ifẹ̀

A lightweight card game inspired by Yoruba mythology.

This repo now contains:
- A **terminal prototype** (`game.py`) with the original 10-floor tutorial flow.
- A **deployable web app prototype** (`index.html` + `static/`) for browser testing.

## Run (terminal build)

```bash
python3 game.py
```

## Run (web build, local preview)

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Web deployment

This web app is static and can be deployed to Vercel/Netlify/GitHub Pages.

### Vercel quick deploy

1. Push this repo to GitHub.
2. Import the repo into Vercel.
3. Framework preset: **Other** (no build command required).
4. Deploy.

## Web gameplay status

- **Webapp-ready:** Yes (playable browser prototype included in this repo).
- **Android-ready:** Not yet (no Android packaging pipeline yet).

## Controls

### Terminal
- Enter card number to play.
- `end` ends turn.
- `art` shows card art references.
- `link` shows configured external prototype URL.

### Web
- Click **Start New Run**.
- Click **Play** on cards to act each turn.

## Card art references

Terminal card-art links are open-license Wikimedia Commons URLs embedded in `game.py` (`CARD_ART`).
