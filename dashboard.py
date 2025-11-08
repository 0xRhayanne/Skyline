import requests
import xml.etree.ElementTree as ET
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

# ========= CONFIG =========
FORECAST_DAYS = 3
NEWS_LIMIT = 5

# --- Global news RSS sources (verified) ---
NEWS_FEEDS_GLOBAL = {
    "General": [
        ("BBC News", "http://feeds.bbci.co.uk/news/rss.xml"),
        ("CNN", "http://rss.cnn.com/rss/edition.rss"),
        ("Reuters", "http://feeds.reuters.com/reuters/topNews"),
    ],
    "Technology": [
        ("BBC Tech", "http://feeds.bbci.co.uk/news/technology/rss.xml"),
        ("CNN Tech", "http://rss.cnn.com/rss/edition_technology.rss"),
    ],
    "Sports": [
        ("BBC Sport", "http://feeds.bbci.co.uk/sport/rss.xml"),
        ("CNN Sports", "http://rss.cnn.com/rss/edition_sport.rss"),
    ],
    "Health": [
        ("BBC Health", "http://feeds.bbci.co.uk/news/health/rss.xml"),
    ]
}

# --- Brazil news RSS sources (verified) ---
NEWS_FEEDS_BRAZIL = {
    "General": [
        ("G1", "https://g1.globo.com/dynamo/rss2.xml"),
        ("Folha Em Cima da Hora", "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml")
    ],
    "Technology": [
        ("Olhar Digital", "https://olhardigital.com.br/feed/"),
        ("Tecnoblog", "https://tecnoblog.net/feed")
    ],
    "Sports": [

        ("Futebol Interior", "https://futebolinterior.com.br/feed")

    ],
    "Health": [
        ("G1 Saúde", "https://g1.globo.com/rss/g1/saude/")
    ]
}



# ==========================

# --- WEATHER FUNCTIONS ---
def get_weather(city_country="São Paulo,BR"):
    """Fetch current weather and 3-day forecast from wttr.in"""
    try:
        url = f"https://wttr.in/{city_country}?format=j1"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        current = data['current_condition'][0]
        temp_c = int(current['temp_C'])
        weather_data = {
            "location": city_country,
            "temperature": temp_c,
            "feels_like": current['FeelsLikeC'],
            "humidity": current['humidity'],
            "description": current['weatherDesc'][0]['value'],
            "forecast": []
        }

        for day in data['weather'][:FORECAST_DAYS]:
            midday = day['hourly'][4]
            avg_temp = (int(day['maxtempC']) + int(day['mintempC'])) // 2
            weather_data["forecast"].append({
                "date": day['date'],
                "maxtempC": int(day['maxtempC']),
                "mintempC": int(day['mintempC']),
                "description": midday['weatherDesc'][0]['value'],
                "avg_temp": avg_temp
            })
        return weather_data

    except Exception as e:
        console.print(f"[red]Failed to fetch weather for {city_country}: {e}[/red]")
        return None


def temperature_style(temp):
    """Return color and icon based on temperature"""
    if temp <= 10:
        return "cyan", "❄️"
    elif temp <= 20:
        return "green", "☁"
    elif temp <= 30:
        return "yellow", "🌤"
    else:
        return "red", "🔥"


# --- NEWS FUNCTIONS ---
def get_news(feeds_dict, category="General", keyword=None, limit=NEWS_LIMIT):
    """Fetch news headlines safely from multiple RSS feeds with optional keyword filtering"""
    feeds = feeds_dict.get(category, [])
    # fallback to General if category has no feeds
    if not feeds:
        feeds = feeds_dict.get("General", [])

    all_news = []
    for name, feed_url in feeds:
        try:
            response = requests.get(feed_url, timeout=5)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            items = root.findall(".//item")
            for item in items:
                title = item.find("title").text
                if keyword is None or keyword.lower() in title.lower():
                    all_news.append({"source": name, "title": title})
                if len(all_news) >= limit:
                    break
        except Exception as e:
            console.print(f"[red]Failed to fetch {name} feed: {e}[/red]")
    return all_news[:limit]


def display_news(title, news_list, border_color):
    """Display news in a table"""
    if news_list:
        table = Table(title=title, border_style=border_color)
        table.add_column("Source", style="cyan")
        table.add_column("Title", style="magenta", overflow="fold")
        for article in news_list:
            table.add_row(article["source"], article["title"])
        console.print(table)
    else:
        console.print(f"[red]{title} not available[/red]")


# --- DASHBOARD ---
def display_dashboard():
    # User input: City + Country
    console.print("[bold blue]Enter your city and country in the format:[/bold blue] City,CountryCode")
    console.print("Example: London,UK or São Paulo,BR")
    city_country = console.input("[bold green]City + Country: [/bold green] ").strip()

    console.rule("[bold blue]🌤 Weather & 📰 News Dashboard")

    # Weather
    weather = get_weather(city_country)
    if weather:
        color, icon = temperature_style(weather["temperature"])
        weather_text = Text(
            f"{weather['location']}\n"
            f"{icon} Temp: {weather['temperature']}°C (Feels like {weather['feels_like']}°C)\n"
            f"💧 Humidity: {weather['humidity']}%\n"
            f"☁ Condition: {weather['description']}",
            style=color
        )
        weather_panel = Panel.fit(weather_text, title="Current Weather", border_style="cyan")
        console.print(weather_panel)

        # Forecast Table with icons
        forecast_table = Table(title=f"{FORECAST_DAYS}-Day Forecast", border_style="magenta")
        forecast_table.add_column("Date", style="cyan")
        forecast_table.add_column("Min°C", style="blue")
        forecast_table.add_column("Max°C", style="red")
        forecast_table.add_column("Condition", style="yellow")

        for day in weather["forecast"]:
            _, day_icon = temperature_style(day["avg_temp"])
            forecast_table.add_row(
                day["date"],
                str(day["mintempC"]),
                str(day["maxtempC"]),
                f"{day_icon} {day['description']}"
            )
        console.print(forecast_table)

    else:
        console.print("[red]Weather data not available[/red]")

    # News input
    console.print("\n[bold yellow]News Options[/bold yellow]")
    console.print("1: Global News")
    console.print("2: Brazil News")
    console.print("3: Both")
    news_choice = console.input("[bold green]Enter 1, 2, or 3: [/bold green]").strip()

    category = console.input("Category (General, Technology, Sports, Health): ").strip().title()
    keyword = console.input("Optional keyword to filter news: ").strip() or None

    if news_choice in ["1", "3"]:
        news_global = get_news(NEWS_FEEDS_GLOBAL, category, keyword)
        display_news(f"🌍 Top Global News ({category})", news_global, "yellow")
    if news_choice in ["2", "3"]:
        news_brazil = get_news(NEWS_FEEDS_BRAZIL, category, keyword)
        display_news(f"🇧🇷 Top Brazil News ({category})", news_brazil, "green")


if __name__ == "__main__":
    display_dashboard()
