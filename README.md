# K-in-a-Row Game Framework

A Python-based framework for playing various K-in-a-Row games with AI agents, including Tic-Tac-Toe, Five-in-a-Row, and Cassini variants.

## Overview

This project implements a flexible game framework for K-in-a-Row style games where two AI agents compete to get K pieces in a row (horizontally, vertically, or diagonally). The framework supports:

- **Multiple game variants**: Tic-Tac-Toe (3x3), Five-in-a-Row (7x7), and Cassini (7x8 with obstacles)
- **AI agent framework**: Base classes for creating intelligent game-playing agents
- **Game visualization**: HTML output with visual board representation
- **Extensible design**: Easy to add new game variants and agent strategies

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- No external dependencies required for basic functionality

### Basic Setup

1. Clone or download the repository:
```bash
git clone <repository-url>
cd K-in-a-Row
```

2. The framework works out of the box with Python's standard library. For the advanced AI agent example, you'll need:
```bash
pip install google-generativeai
```

### Verify Installation

Test the setup by running a simple game:
```bash
python3 RandomPlayer.py
```

## Quick Start

### Running a Basic Game

The simplest way to start a game is by running the main game master:

```bash
python3 GameMasterOffline.py
```

This will start a Five-in-a-Row game between the Yoda agent and Randy (random player).

### Customizing the Game

Edit the `test()` function in `GameMasterOffline.py` to change game settings:

```python
def test():
    # Choose game type
    set_game(TTT)     # Tic-Tac-Toe
    # set_game(FIAR)  # Five-in-a-Row  
    # set_game(Cassini) # Cassini variant
    
    # Import and set up agents
    import RandomPlayer as h1
    import RandomPlayer as h2
    px = h1.OurAgent()
    po = h2.OurAgent(twin=True)
    set_players(px, po)
    
    runGame()
```

## Game Variants

### 1. Tic-Tac-Toe (TTT)
- **Board size**: 3x3
- **Goal**: Get 3 in a row
- **Turn limit**: 9 moves
- **Features**: Classic tic-tac-toe rules

### 2. Five-in-a-Row (FIAR)
- **Board size**: 7x7
- **Goal**: Get 5 in a row
- **Turn limit**: 45 moves
- **Features**: Corner squares are forbidden (marked with `-`)

### 3. Cassini
- **Board size**: 7x8
- **Goal**: Get 5 in a row without hitting "Saturn" (obstacles)
- **Turn limit**: 44 moves
- **Features**: Pre-placed obstacles and pieces create strategic challenges

## Project Structure

```
K-in-a-Row/
├── GameMasterOffline.py    # Main game controller and runner
├── game_types.py          # Game variant definitions (TTT, FIAR, Cassini)
├── agent_base.py          # Base class for creating AI agents
├── winTesterForK.py       # Win condition checker
├── gameToHTML.py          # HTML visualization generator
├── RandomPlayer.py        # Example random agent implementation
├── cchen025_KInARow.py    # Advanced AI agent with minimax
└── *.png                  # Game piece images for HTML output
```

### Key Components

- **GameMasterOffline.py**: Orchestrates games between two agents, handles turn management, and generates output
- **game_types.py**: Defines the `State` class and game configurations for different variants
- **agent_base.py**: Provides the `KAgent` base class that all agents must inherit from
- **winTesterForK.py**: Checks for winning conditions after each move

## Authors

- **Framework**: University of Washington, S. Tanimoto (2024)
- **Example Agents**: 
  - RandomPlayer: Basic random strategy implementation
  - cchen025_KInARow: Tony Wu and Castor Chen - Advanced AI agent with minimax, alpha-beta pruning, and LLM API integration.
