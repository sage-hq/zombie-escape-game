# 🧟 Zombie Escape Game | ゾンビから逃げるゲーム

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.6.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

A fast-paced survival game built with Pygame where you need to escape from pursuing zombies while collecting power-ups and navigating through obstacles. The game features both English and Japanese language support.

![Game Screenshot](https://raw.githubusercontent.com/sage-hq/zombie-escape-game/main/assets/images/Player.png)

## 🎮 Features

- **Dynamic Difficulty**: Zombies get faster as time progresses
- **Power-up System**:
  - 🟢 Speed Boost (Green)
  - 🟡 Temporary Invincibility (Yellow)
  - 🔵 Zombie Freeze (Cyan)
- **Obstacle System**: Strategic barriers for tactical gameplay
- **High Score System**: Track your best survival times
- **Precise Collision Detection**: Using mask-based collision for accurate hit detection
- **Full Japanese Language Support**: Using system fonts (Hiragino on macOS)

## 🎯 Game Mechanics

- Survive as long as possible while avoiding zombies
- Collect power-ups to gain advantages:
  - Green orbs increase your speed
  - Yellow orbs make you temporarily invincible
  - Cyan orbs freeze all zombies temporarily
- Use obstacles strategically to escape from zombies
- Your score is based on survival time
- Zombies become faster as time progresses

## 🎹 Controls

- **Arrow Keys**: Move the player
- **Enter**: Start game (on title screen)
- **R**: Restart (after game over)
- **ESC**: Quit game

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/sage-hq/zombie-escape-game.git
cd zombie-escape-game
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Generate game assets:
```bash
python create_assets.py
```

5. Run the game:
```bash
python main.py
```

## 🛠️ Requirements

- Python 3.x
- Pygame 2.6.1 or higher

## 🗺️ Development Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features and improvements, including:
- Sound effects and BGM
- Different types of zombies
- Complete Japanese localization
- Difficulty settings
- Mobile compatibility
- Multiplayer mode

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Credits

- Game Development: sage
- Framework: Pygame
- Special thanks to the Pygame community

## 🌐 Language Support

- 🇯🇵 Japanese (日本語)
