# Python Game Suite

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A collection of classic command-line and GUI games built with Python, showcasing modern development practices and professional packaging standards. This project demonstrates a pluggable architecture where games are dynamically discovered at runtime, making it easy to add new games without modifying the core launcher.

## ✨ Features

- **🔌 Pluggable Architecture**: Games are self-contained modules that register themselves automatically
- **⚡ Modern Tooling**: Lightning-fast dependency management with `uv`
- **🎯 Code Quality**: Consistent formatting and linting with `Ruff`
- **📦 Professional Packaging**: Follows Python packaging best practices with `src` layout and `pyproject.toml`
- **🚀 Easy Installation**: Install once, run anywhere with the `run-games` command
- **🎮 Variety**: Mix of terminal-based classics and modern GUI games

## 🎮 Game Collection

| Game | Type | Description |
|------|------|-------------|
| **Rock, Paper, Scissors** | Terminal | Classic hand game with score tracking |
| **Number Guessing** | Terminal | Guess the computer's number with hints |
| **Hangman** | Terminal | Word guessing game with ASCII art |
| **Mastermind** | Terminal | Code-breaking logic puzzle |
| **Lucky 9** | Terminal/GUI | Card game available in both formats |

## 🏗️ Architecture

The project uses a clean, modular architecture that makes adding new games straightforward:

```
python-game-suite/
├── pyproject.toml              # Project configuration and dependencies
├── src/
│   └── python_game_suite/
│       ├── __init__.py         # Package initialization
│       ├── main.py             # Game launcher and menu system
│       ├── common/             # Shared utilities and base classes
│       │   ├── __init__.py
│       │   └── game_template.py    # Abstract base class for games
│       ├── hangman/            # Individual game packages
│       ├── lucky9/
│       ├── mastermind/
│       ├── number_guessing/
│       └── rock_paper_scissors/
└── uv.lock                     # Locked dependencies for reproducibility
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **uv** (recommended) or pip

Install `uv` for the best experience:
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Alternative: via pip
pip install uv
```

### Installation

1. **Clone and navigate to the project:**
   ```bash
   git clone https://github.com/Onehand-Coding/python-game-suite.git
   cd python-game-suite
   ```

2. **Set up the environment and install:**
   ```bash
   # Create virtual environment and install dependencies
   uv sync

   # Activate the environment
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Launch the games:**
   ```bash
   run-games
   ```

## 🎯 Usage

After installation, simply run:
```bash
run-games
```

This opens an interactive menu where you can:
- Browse available games
- Select and launch games
- View game descriptions
- Exit gracefully

## 🛠️ Development

### Code Quality Tools

The project maintains high code quality with automated tools:

```bash
# Format code
ruff format .

# Check for issues
ruff check .

# Fix auto-fixable issues
ruff check --fix .
```

### Adding New Games

1. Create a new package in `src/python_game_suite/`
2. Implement the `GameBase` interface from `common.game_base`
3. The game will be automatically discovered and added to the menu

Example structure:
```python
from python_game_suite.common.game_template import Game

class MyNewGame(Game):
    def get_name(self) -> str:
        return "My New Game"

    def run(self) -> None:
        # Game implementation
        pass
```

### Project Configuration

The project uses modern Python packaging standards:

- **pyproject.toml**: Central configuration for dependencies, tools, and metadata
- **src/ layout**: Separates source code from configuration files
- **uv.lock**: Ensures reproducible builds across environments

## 📋 Requirements

- Python 3.9 or higher
- Dependencies managed automatically via `uv sync`:
  - `pygame` (for GUI games)
  - `ruff` (for code quality)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and ensure tests pass
4. Run code quality checks: `ruff format . && ruff check .`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Repository](https://github.com/Onehand-Coding/python-game-suite)
- [Issue Tracker](https://github.com/Onehand-Coding/python-game-suite/issues)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
