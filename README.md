# Discord-Rare-Username-Gen

🦆 AI-assisted asynchronous username scanner with live statistics, webhook notifications, and customizable generation settings.

---

# 🦆 VOTDuck v2.1

> Rare Username Hunter

## 🤖 AI Generated Project

This project was developed with the assistance of Artificial Intelligence.

The source code, application structure, optimization ideas, terminal interface, configuration system, and this README file were generated and refined using AI tools. Final testing, customization, and project management were performed by the repository owner.

---

## 📖 About

VOTDuck is a high-performance asynchronous username generation and scanning tool written in Python.

The project focuses on generating short and uncommon username combinations while providing a fast, configurable, and user-friendly terminal interface. It includes support for live statistics, configurable generation settings, webhook notifications, persistent storage, and automatic rate-limit handling.

Designed with performance in mind, VOTDuck uses asynchronous requests and batch processing to maximize throughput while maintaining stability.

---

## 🖼 Preview

![VOTDuck Screenshot](75588fc4-4381-4292-ad0f-a1fd8cd17812.png)

---

## ✨ Features

### 🚀 Performance

- Fully asynchronous architecture
- Multi-request batch processing
- Configurable concurrency limits
- Optimized request handling
- Automatic rate-limit recovery

### 🎯 Username Generation

- Random username generation
- Configurable minimum and maximum lengths
- Rare character prioritization
- Optional special character insertion
- Custom blacklist filtering

### 📊 Statistics

- Real-time statistics display
- Total usernames checked
- Available usernames found
- Unavailable usernames tracked
- Requests-per-minute calculation

### 🔔 Notifications

- Discord webhook integration
- User mention support
- Role mention support
- Instant alerts when matches are found

### 💾 Data Management

- Persistent username database
- Automatic duplicate prevention
- Separate result files
- Session recovery support

### ⚙️ Configuration

- Easy `.env` configuration
- Adjustable speed settings
- Custom output files
- Fully customizable behavior

---

## 📦 Requirements

- Python 3.10+
- aiohttp
- python-dotenv

Install dependencies:

```bash
pip install aiohttp python-dotenv
```

---

## ⚙️ Configuration

Example `.env` configuration:

```env
# BASIC SETTINGS
MIN_LENGTH=4
MAX_LENGTH=5
TOTAL_TO_CHECK=300

# PERFORMANCE
BATCH_SIZE=10
BATCH_DELAY=2.2
MAX_CONCURRENT=25
RARE_LETTER_BIAS=0.12

# FILTER
BLACKLIST_WORDS=lol,xd,bot,noob,pro,god,xxx,420,69

# WEBHOOK
WEBHOOK_URL=
PING_USER_ID=
PING_ROLE_ID=

# FILES
CHECKED_FILE=checked.txt
AVAILABLE_FILE=available.txt
UNAVAILABLE_FILE=unavailable.txt
```

---

## 🚀 Usage

Launch the application:

```bash
python votduck.py
```

---

## 📋 Main Menu

```text
[1] Start Checker
[2] View Settings
[3] Statistics
[4] Exit
```

---

## 📊 Example Output

```text
Checked: 11,802 | Available: 3 🦆 | Unavailable: 11,799 | RPM: 5,295
```

---

## 📁 Project Structure

```text
VOTDuck/
│
├── votduck.py
├── .env
├── checked.txt
├── available.txt
├── unavailable.txt
├── README.md
└── screenshot.png
```

---

## 🛠 Customization

VOTDuck can be customized to fit different workflows:

- Username length ranges
- Batch sizes
- Concurrency limits
- Generation patterns
- Rare character probability
- Blacklisted words
- Notification settings
- Output destinations

---

## 🔒 Privacy

The application does not collect, store, or transmit personal user data beyond the optional webhook configuration provided by the user.

All generated and processed data remains local unless a webhook is explicitly configured.

---

## ⚠️ Disclaimer

This project is intended for educational, experimental, and research purposes only.

The repository owner and contributors are not responsible for misuse of this software. Users are responsible for ensuring that their use of the software complies with all applicable platform rules, terms, and local laws.

External services may change over time, which can affect functionality.

---

## 📈 Future Plans

- Better generation algorithms
- Additional filtering options
- Improved terminal interface
- Extended statistics tracking
- Export functionality
- More notification providers

---

## ❤️ Credits

### Creator

**Aby377**

### AI Assistance

This project was created with significant AI assistance.

AI contributed to:

- Source code generation
- Architecture planning
- Feature implementation
- Optimization suggestions
- Documentation writing
- README generation

---

## ⭐ Support

If you like this project, consider giving it a star.

It helps the project grow and motivates future updates.

---

Made with ❤️, ☕ and AI 🤖
