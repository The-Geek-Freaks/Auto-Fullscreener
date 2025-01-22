<div align="center">
  <h1>🎥 Auto-Fullscreener</h1>
  <p>A powerful OBS Studio script for automated multi-monitor projector management.</p>
  <p>Perfect for streamers, content creators, and professional broadcasters.</p>

  ![Downloads](https://img.shields.io/github/downloads/The-Geek-Freaks/OBS-Auto-Fullscreener/total)
  ![Version](https://img.shields.io/badge/Version-1.0.0-blue)
  ![Python](https://img.shields.io/badge/python-3.9+-green.svg)
  ![OBS](https://img.shields.io/badge/OBS-30.0+-purple.svg)
  ![Windows](https://img.shields.io/badge/Windows-10%2F11-blue)
  ![macOS](https://img.shields.io/badge/macOS-11.0+-silver)
  ![Linux](https://img.shields.io/badge/Linux-Compatible-orange)
  ![License](https://img.shields.io/badge/License-GPLv3-blue.svg)
  [![Discord](https://img.shields.io/discord/397127284114325504?label=Discord&logo=discord)](https://tgf.click/discord)
</div>

<div align="center">
  <img src="Auto Fullscreener.png" alt="OBS Auto Fullscreener Interface" width="800"/>
</div>

## 📑 Table of Contents
- [✨ Key Features](#-key-features)
- [🎯 Use Cases](#-use-cases)
- [💻 Installation](#-installation)
- [🛠️ Configuration](#️-configuration)
- [🎮 Usage](#-usage)
- [🔧 Troubleshooting](#-troubleshooting)
- [📄 License](#-license)

## ✨ Key Features

### 🖥️ Advanced Monitor Support
- **Multi-Monitor Detection**: 
  - Automatic detection of all connected displays
  - Support for multiple graphics cards
  - USB monitor compatibility
  - Resolution and position information
- **Smart Monitor Selection**:
  - Primary monitor identification
  - Detailed monitor information
  - Test projection feature
  - Monitor position awareness

### 🎬 Flexible Projection Options
- **Multiple Projection Modes**:
  - Preview projector
  - Scene projector
  - Dynamic scene selection
  - Real-time scene switching
- **Automated Control**:
  - Auto-start with OBS
  - Configurable startup delay
  - Hotkey support
  - Scene refresh functionality

### ⚙️ Professional Features
- **Reliability**:
  - Crash protection
  - Resource cleanup
  - Error logging
  - Automatic recovery
- **User Experience**:
  - Intuitive settings interface
  - Grouped configuration options


## 🎯 Use Cases

### Streaming Setup
- Project your stream preview on a secondary monitor
- Display different scenes on multiple monitors
- Quick switching between preview and scene modes
- Professional multi-display management

### Event Production
- Control multiple display outputs
- Dedicated preview monitors
- Scene distribution across displays
- Automated display management

### Content Creation
- Multi-monitor recording setup
- Preview while recording
- Flexible scene distribution
- Automated display configuration

## 💻 Installation

1. Download the latest release from the releases page
2. Place the script in your OBS scripts folder:
   - Windows: `%APPDATA%\obs-studio\scripts`
   - macOS: `~/Library/Application Support/obs-studio/scripts`
   - Linux: `~/.config/obs-studio/scripts`
3. In OBS Studio:
   - Go to Tools → Scripts
   - Click the + button
   - Select the downloaded script
   - Configure your settings

### Platform-Specific Requirements

#### Windows
- Python 3.9 or higher
- Windows 10/11

#### macOS
- Python 3.9 or higher
- macOS 11.0 (Big Sur) or higher
- XCode Command Line Tools (for Python)

#### Linux
- Python 3.9 or higher
- X11 or Wayland
- Required packages:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-pip python3-tk
  
  # Fedora
  sudo dnf install python3-pip python3-tkinter
  
  # Arch Linux
  sudo pacman -S python-pip python-tk
  ```

## 🛠️ Configuration

### Basic Settings
1. **Startup Options**:
   - Enable/disable automatic start
   - Set startup delay time
   - Configure default behavior

2. **Display Options**:
   - Select target monitor
   - Test monitor configuration
   - View monitor details

3. **Projector Options**:
   - Choose projection mode
   - Select scene (if applicable)
   - Configure refresh behavior

### Advanced Features
- **Hotkey Configuration**:
  1. Go to Settings → Hotkeys
  2. Find "Start Projector" under Scripts
  3. Set your preferred key combination

## 🎮 Usage

1. **Quick Start**:
   - Select your target monitor
   - Choose projection mode
   - Click "Test" to verify
   - Apply settings

2. **Automated Setup**:
   - Enable "Start with OBS"
   - Set appropriate delay
   - Configure projection options
   - Restart OBS to activate

## 🔧 Troubleshooting

### Common Issues
1. **Monitor Not Detected**:
   - Ensure monitor is connected
   - Try reconnecting the display
   - Check display settings:
     - Windows: Windows display settings
     - macOS: System Settings → Displays
     - Linux: Check display settings in your desktop environment

2. **Projection Issues**:
   - Verify monitor selection
   - Check OBS Studio version
   - Ensure sufficient system resources
   - For Linux: Verify X11/Wayland compatibility

3. **Performance Problems**:
   - Lower projection resolution
   - Update graphics drivers
   - Check system resources
   - For macOS: Check Energy Saver settings
   - For Linux: Verify compositor settings

### Platform-Specific Solutions

#### Windows
- Update Windows display drivers
- Check Windows HDR settings
- Verify Windows scaling settings

#### macOS
- Check System Integrity Protection (SIP) settings
- Verify screen recording permissions
- Update macOS and OBS to latest versions

#### Linux
- Check display server (X11/Wayland) compatibility
- Verify desktop environment permissions
- Update graphics drivers and compositor

### Support
- Check the [Issues](https://github.com/The-Geek-Freaks/OBS-Auto-Fullscreener/issues) page
- Join our [Discord](https://tgf.click/discord) for help
- Submit bug reports with logs

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <p> TheGeekFreaks 2025</p>
  <p>
    <a href="https://tgf.click/discord">Discord</a> •
    <a href="https://github.com/The-Geek-Freaks">GitHub</a> •
    <a href="https://www.youtube.com/TheGeekFreaks">YouTube</a>
  </p>
</div>
