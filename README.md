# Dino Game — Dino Jump

> A Chrome-dino-style jump game in two flavors: a pygame desktop version and a Flask-served web version with a score leaderboard — hobby project, functional but minimal.

Dodge procedurally spawned obstacles (cacti, birds, rocks) as the speed ramps up. Scores are tallied locally (desktop) or posted to a small REST API (web). Includes settings persistence, synthetic sound effects, day/night/sunset themes, and a committed PyInstaller build.

---

## 📜 Table of Contents

- [✨ Features](#-features)
- [🚀 Installation](#-installation)
- [📖 Usage](#-usage)
- [🏗️ Architecture](#-architecture)
- [🛠️ Technologies Used](#-technologies-used)
- [⚠️ Limitations](#-limitations)
- [📜 License](#-license)
- [📧 Contact](#-contact)

---

## ✨ Features

### Desktop version (`backend/game.py`, ~550 lines)
- **Jump-and-dodge gameplay** — space/up-arrow to jump, `P` to pause, `R`/`C` to restart/continue, mouse click also starts from the menu.
- **Procedural obstacles** — cactus, bird, and rock types spawn on a randomized interval (80–150 frames); each cleared obstacle adds 10 points.
- **Difficulty ramp** — scroll speed increases every 150 points; background theme cycles day → night → sunset every 500 points.
- **Settings** — volume, difficulty, and fullscreen toggles persisted to `data/settings.json` (keys: `V`, `D`, `F` in the settings screen).
- **High scores** — top-10 local leaderboard in `data/scores.json`; enter a name (≤20 chars) at game over to submit.
- **Synthetic audio** — jump/score/game-over sounds are generated beep waveforms at runtime; volume scales them.
- **Logging** — events appended to `logs/game.log`.

### Web version (`backend/server.py` + `frontend/`)
- **Flask server** — serves `frontend/game.html` at `/`, static files, and a JSON leaderboard API (`GET`/`POST /api/scores`, top 10 by score).
- **Canvas game** — `frontend/script.js` implements the same jump/dodge loop in JavaScript (800×400 canvas), with start/pause/game-over screens and a save-score form that POSTs to the API.
- **CORS enabled** — the API accepts cross-origin requests (`flask_cors`).

### Packaging
- **PyInstaller build** — `backend/build_exe.py` and `backend/DinoGame.spec` build `dist/DinoGame.exe` (a built copy is committed under `backend/dist/` and `backend/build/`).

---

## 🚀 Installation

### Prerequisites
- Python 3.x (desktop version); any modern browser (web version)
- For the web version: Flask + flask-cors

### Steps
1. Desktop: `pip install -r backend/requirements.txt` (pins `pygame==2.5.2`, `pyinstaller==6.3.0`), then run `launch_game.bat` or `python backend/game.py`.
2. Web: `pip install flask flask-cors`, then `python backend/server.py` and open `http://localhost:5000`.
3. Executable: `python backend/build_exe.py` produces `backend/dist/DinoGame.exe`.

---

## 📖 Usage

### Desktop controls
- **SPACE / ↑** — jump (or start/restart)
- **P** — pause · **C** — continue · **R** — restart · **ESC** — back/quit
- **S** — settings · **H** — high scores
- In settings: **V** volume, **D** cycle difficulty, **F** toggle fullscreen
- At game over: type a name, **ENTER** saves the score

### Web version
- Open the served page, press **Space** or click start; **P/Esc** pauses; game-over screen offers replay and a player-name field that POSTs to `/api/scores`.

---

## 🏗️ Architecture

```
dino game/
├── launch_game.bat        # installs backend/requirements.txt, runs game.py
├── backend/
│   ├── game.py            # pygame desktop game (DinoGame class)
│   ├── server.py          # Flask app: static frontend + /api/scores
│   ├── build_exe.py       # PyInstaller wrapper script
│   ├── DinoGame.spec      # PyInstaller spec
│   ├── requirements.txt   # pygame, pyinstaller
│   ├── build/, dist/      # committed PyInstaller artifacts (DinoGame.exe)
│   └── __pycache__/
├── frontend/
│   ├── game.html          # page shell + screens
│   ├── script.js          # canvas game loop + leaderboard calls
│   └── style.css
├── api/                   # empty directory
├── data/                  # runtime: settings.json, scores.json (created on run)
└── logs/game.log          # runtime log
```

### Data Flow
- **Desktop**: `game.py` reads/writes `data/settings.json` and `data/scores.json` directly; logs to `logs/game.log`.
- **Web**: browser canvas game → `POST /api/scores` → `server.py` appends `{player_name, score, date}` to `data/scores.json`; `GET /api/scores` returns the top 10 sorted descending. Server logs to `logs/server.log`.

---

## 🛠️ Technologies Used

### Desktop
- **Python + pygame 2.5.2** - game loop, rendering, input, generated audio
- **PyInstaller 6.3.0** - `DinoGame.exe` packaging

### Web
- **Flask + Flask-CORS** - static file serving and REST leaderboard API
- **Vanilla HTML/CSS/JavaScript** - canvas rendering, no framework

---

## ⚠️ Limitations

### Feature gaps / correctness
- **"Difficulty" setting is cosmetic** — the settings screen cycles easy/normal/hard and persists it, but no code path reads it; actual speed is driven solely by score (`speed_increase_score = 150`).
- **Score = obstacles cleared × 10** — there is no time/distance bonus; high scores only reflect survival count.
- **Web and desktop versions are separate implementations** — they don't share code or saves; the web leaderboard is server-side JSON while the desktop one is a local file.
- **`api/` and root `data/` directories are empty** in the repo — runtime data is created under `data/` only when the app runs.

### Technical / security
- **Leaderboard has no validation** — `POST /api/scores` accepts any positive score and any name; scores are trivially spoofable.
- **Server binds `0.0.0.0:5000` with CORS open to all origins** — fine on a LAN, unsafe to expose.
- **Committed build artifacts** — `backend/dist/DinoGame.exe`, `backend/build/`, and `.rar` archives are checked into the repo, bloating it.
- **`backend/game.py` logs via plain file append** — no rotation; `logs/game.log` grows unbounded.

### Testing Limitations
- **What a clone can re-check**: both entry points run standalone (`python backend/game.py`, `python backend/server.py`); the API can be exercised with curl.
- **What a clone cannot re-check**: the committed `.exe` was built on the author's machine; actual frame-rate/gameplay feel and the web version's behavior under real browsers were not verified here.

---

## 📜 License

Dino Game is proprietary software — see [LICENSE](LICENSE) for the full terms.

**Copyright © 2026 AliesterEroan. All rights reserved.**

This software is provided for personal, non-commercial use only. Commercial use, redistribution, modification, and sublicensing are prohibited without explicit written permission. The copyright holder may distribute copies through the project's official GitHub Releases page; third parties may not host, mirror, or redistribute this software.

For licensing inquiries, open an issue at <https://github.com/AliesterEroan/dino-game/issues>.

---

## 📧 Contact

- **GitHub**: [AliesterEroan/dino-game](https://github.com/AliesterEroan/dino-game)
- **Issues**: [Create an issue](https://github.com/AliesterEroan/dino-game/issues)

---

*Built with ❤️ by AliesterEroan*
