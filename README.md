# 🦖 Dino Game

> Classic dinosaur runner game with Python backend and web frontend! 🎮

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Game](https://img.shields.io/badge/Game-Dino%20Runner-green?style=for-the-badge)
![Web](https://img.shields.io/badge/Web-HTML%2FJS-orange?style=for-the-badge)

---

## ✨ Features

- 🦖 Classic dinosaur runner gameplay
- 🎮 Web-based frontend with HTML/CSS/JS
- 🐍 Python backend server
- 🚀 Easy to launch and play
- 🎨 Responsive design
- ⚡ Real-time game synchronization

## 🛠️ Requirements

### Backend
- **Python 3.8+**
- **PyInstaller** (for building executables)
- Dependencies in requirements.txt

### Frontend
- Modern web browser
- JavaScript enabled

## 📋 Project Structure

```
dino-game/
├── backend/
│   ├── game.py              # Main game logic
│   ├── server.py            # Web server
│   ├── build_exe.py         # Build script
│   ├── DinoGame.spec        # PyInstaller spec
│   ├── requirements.txt     # Python dependencies
│   ├── build/              # Build output
│   └── dist/               # Distribution files
├── frontend/
│   ├── game.html           # Game interface
│   ├── script.js           # Game logic (JavaScript)
│   └── style.css           # Styling
└── launch_game.bat         # Quick launch script
```

## 🚀 Getting Started

### Quick Start

1. **Launch the game**
   ```bash
   # Windows
   launch_game.bat
   ```

2. **Open in browser**
   - Navigate to the provided URL
   - Start playing!

### Manual Setup

**Backend Setup:**
```bash
cd backend
pip install -r requirements.txt
python server.py
```

**Frontend:**
- Open `frontend/game.html` in your browser
- The game will connect to the backend server

## 🎮 How to Play

**Controls:**
- **Space** or **Up Arrow** - Jump
- **Down Arrow** - Duck
- Avoid obstacles and survive as long as possible!

**Gameplay:**
- The dinosaur runs automatically
- Jump over cacti and duck under flying obstacles
- Score increases over time
- Game speed increases as you progress

## 🔧 Configuration

**Server Settings (backend/server.py):**
```python
# Modify server configuration
HOST = 'localhost'
PORT = 8000
```

**Game Settings (frontend/script.js):**
```javascript
// Adjust game parameters
const GRAVITY = 0.6;
const GAME_SPEED = 6;
const SPAWN_RATE = 100;
```

## 🎨 Customization

**Appearance:**
- Modify `frontend/style.css` for visual changes
- Edit colors, fonts, and layout

**Game Mechanics:**
- Adjust game parameters in `frontend/script.js`
- Modify obstacle generation and collision detection

**Backend Logic:**
- Change game rules in `backend/game.py`
- Add new features or scoring systems

## 📊 Technical Details

**Backend (Python):**
- Game server using Python
- Real-time game state management
- Client-server communication

**Frontend (HTML/CSS/JS):**
- Canvas-based rendering
- Responsive design
- Keyboard event handling

**Build System:**
- PyInstaller for executable creation
- Cross-platform support

## 🎯 Typical Applications

- 🎮 Game development learning
- 🎓 Web game programming
- 🏃 Endless runner game concepts
- 🎨 Frontend-backend integration
- 🐍 Python web development

## ⚠️ Notes

- Requires Python for backend functionality
- JavaScript must be enabled in browser
- Server must be running for multiplayer features
- Build executable for standalone use

## 🎓 Learning Objectives

- Python web server development
- Frontend-backend communication
- Game development fundamentals
- Canvas-based rendering
- Real-time web applications

---

**Made with ❤️ by AliesterEroan**