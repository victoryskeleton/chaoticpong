# Enhanced Pong Game

A modern take on the classic Pong game, featuring power-ups, abilities, and advanced AI opponents. Built with Python and Pygame.

## 🎮 Features

### Game Modes
- **Single Player**: Face off against an AI opponent with adjustable difficulty
- **Two Players**: Local multiplayer mode for head-to-head matches

### Customization Options
- **Ball Speed**: 5 different speed settings
  - Super Slow
  - Slow
  - Medium
  - Fast
  - Super Fast
- **Paddle Shrink**: Enable/disable paddle shrinking on points
- **Bot Difficulty** (Single Player):
  - Easy: Slower reactions, basic strategy
  - Medium: Balanced AI with moderate skill
  - Hard: Quick reactions, strategic ability usage
  - Ultra: Lightning-fast reactions, advanced strategy
- **Winning Score**: Multiple options from 1 to infinite points

### Special Abilities
Each player can select 3 abilities from the following options:

1. **Size-up**: Increase paddle size by 50% (Duration: 5s, Cooldown: 10s)
2. **Speed-up**: Double paddle speed (Duration: 3s, Cooldown: 15s)
3. **Reverse**: Reverse ball direction (Instant, Cooldown: 30s)
4. **Slow-down**: Slow opponent by 30% (Duration: 5s, Cooldown: 20s)
5. **Chaos**: Make opponent 400% faster but 25% smaller (Duration: 3s, Cooldown: 30s)
6. **Powershot**: Triple ball speed on next paddle hit (Until hit, Cooldown: 15s)
7. **Stealth**: Turn ball black for 2 seconds (Duration: 2s, Cooldown: 15s)
8. **Pinpoint**: Instantly align paddle with ball position (Instant, Cooldown: 10s)

### Visual Effects
- Dynamic fire trail behind fast-moving balls
- Explosion effects on powershot impacts
- Ability cooldown indicators
- Color-changing paddles
- Center line divider

## 🎯 How to Play

### Controls
- **Player 1**:
  - W: Move Up
  - S: Move Down
  - Custom keybinds for abilities (selected at start)

- **Player 2**:
  - ↑: Move Up
  - ↓: Move Down
  - Custom keybinds for abilities (selected at start)

### Menu Navigation
- Number keys (1-8): Make selections
- Minus key (-): Go back to previous menu
- ESC: Quit current game
- SPACE: Play again after match ends

### Gameplay Tips
- Ball speed increases with each paddle hit
- Paddles can shrink after points (if enabled)
- Strategic ability usage is key to winning
- Watch the cooldown indicators for ability timing
- Use powershots carefully as they can backfire

## 🤖 Bot AI Features

### Easy Difficulty
- Slower reaction time
- Basic ability usage
- Moderate prediction error

### Medium Difficulty
- Balanced reaction time
- Strategic ability usage
- Reduced prediction error

### Hard Difficulty
- Quick reactions
- Advanced ability strategy
- Minimal prediction error
- Adaptive gameplay

### Ultra Difficulty
- Lightning-fast reactions
- Expert ability combinations
- Precise ball prediction
- Dynamic strategy adaptation
- Situational awareness

## 🛠️ Technical Requirements

### Dependencies
- Python 3.x
- Pygame 2.x

### Installation
1. Ensure Python is installed on your system
2. Install Pygame: `pip install pygame`
3. Run the game: `python pong.py`

## 🎨 Customization

The game includes several customizable constants in the code:
- Window dimensions
- Paddle sizes
- Ball speed
- Power-up durations
- Colors and visual effects
- Bot difficulty parameters

## 🏆 Scoring

- Points are scored when the ball passes the opponent's paddle
- First to reach the selected winning score wins
- Infinite score option available for endless matches

## 🐛 Troubleshooting

If you encounter any issues:
1. Ensure all dependencies are properly installed
2. Check if Python and Pygame versions are compatible
3. Verify the game file has proper permissions
4. Make sure your system meets the minimum requirements

## 📝 Credits

This enhanced version of Pong was created as a modern reimagining of the classic game, featuring additional gameplay mechanics and visual improvements while maintaining the core essence of the original Pong. 