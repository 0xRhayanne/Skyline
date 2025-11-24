# 🌆 Skyline: Terminal-based Weather and News Dashboard.

Built in Python, designed to keep you informed about the latest weather conditions and trending news headlines, all in one sleek command-line interface.

Powered by wttr.in for weather data and reliable RSS feeds from global and Brazilian news sources, Skyline brings a colorful, interactive experience to your terminal using the Rich library.

---
# ✨ Features

✅ Real-time Weather Data

- Displays current weather conditions for any city and country;
- Shows a 3-day forecast with temperature ranges and condition icons;
- Uses color-coded styling to visualize weather conditions;

✅ News Headlines by Category

- Fetches top headlines from trusted global and Brazilian sources;
- Categories: ```General```, ```Technology```, ```Sports```, and ```Health```;
- Optional keyword filtering to narrow down topics;
- Displays news in organized, color-rich tables;

✅ Interactive CLI Dashboard

- Simple prompts to choose location, news region, category, and filters;
- Beautiful, formatted output using the ```rich``` library.

---

# 🖥️ Demo

```
🌤 Weather & 📰 News Dashboard
Enter your city and country (e.g., London,UK or Paraná,BR):
> Paraná,BR

Current Weather:
🌤 Temp: 27°C (Feels like 29°C)
💧 Humidity: 65%
☁ Condition: Partly Cloudy

3-Day Forecast:
Date         | Min°C | Max°C | Condition
------------------------------------------
2025-11-04   | 19    | 29    | 🌤 Partly Cloudy
2025-11-05   | 18    | 28    | 🌦 Light Rain
2025-11-06   | 20    | 30    | 🌞 Sunny

```

```
Top Global News (Technology)
--------------------------------
Source          | Title
--------------------------------
BBC Tech        | AI revolution reshapes global economy
CNN Tech        | New smartphone sets record for camera performance

```
# 🚀 Installation

1. Clone this repository:

```
git clone https://github.com/0xRhayanne/skyline.git
cd skyline
```
2. Set up a Python virtual environment (optional but recommended):

```
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install the required dependencies:

```
pip install -r requirements.txt
```
4. Run the application:

```
python skyline.py
```

# ⚙️ Configuration

- Weather API: The weather data is fetched from wttr.in
- The default city is set, but you can change it based on your preferences;
- News Feeds: Skyline pulls news from trusted global and Brazilian sources via RSS feeds. You can modify or add new sources in the ```NEWS_FEEDS_GLOBAL``` and ```NEWS_FEEDS_BRAZIL``` dictionaries in the code.
---

# 👀 Acknowledgements

- wttr.in for providing the weather data API;
- Rich for the beautiful terminal output;
- Various global and Brazilian RSS feed sources for news data.
