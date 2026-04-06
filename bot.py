import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_TOKEN = os.getenv('FOOTBALL_API_KEY')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Beispielhafte API (z.B. api.football-data.org)
API_URL = 'https://api.football-data.org/v4/matches?dateFrom={date}&dateTo={date}'

user_teams = {}

# API-Limit-Überwachung
import threading
API_MINUTE_LIMIT = 10
API_MONTH_LIMIT = 2500
api_request_count_minute = 0
api_request_count_month = 0
api_limit_lock = threading.Lock()

def reset_minute_counter():
    global api_request_count_minute
    with api_limit_lock:
        api_request_count_minute = 0

def reset_month_counter():
    global api_request_count_month
    with api_limit_lock:
        api_request_count_month = 0

def start_minute_timer():
    threading.Timer(60, minute_timer_tick).start()

def minute_timer_tick():
    reset_minute_counter()
    start_minute_timer()

start_minute_timer()

@bot.event
def on_ready():
    print(f'Bot ist eingeloggt als {bot.user}')
    daily_matches.start()

@bot.command()
async def spiele(ctx):
    """Zeigt die heutigen Fußballspiele an."""
    matches = get_matches(ctx)
    if not matches:
        await ctx.send('Heute finden keine Spiele statt oder es gab ein Problem mit der API oder das Limit ist erreicht.')
        return
    msg = '**Fußballspiele heute:**\n'
    for match in matches:
        msg += f"{match['home']} vs {match['away']} ({match['time']})\n"
    await ctx.send(msg)


# Beispielhafte Teamliste (kann durch API ersetzt werden)
TEAMS = [
    "Bayern München", "Borussia Dortmund", "RB Leipzig", "SC Freiburg", "VfB Stuttgart",
    "Eintracht Frankfurt", "1. FC Köln", "Werder Bremen", "FC Augsburg", "VfL Wolfsburg"
]

@bot.command()
async def teams(ctx):
    """Zeigt eine Liste verfügbarer Teams zur Auswahl an."""
    msg = '**Verfügbare Teams:**\n'
    for t in TEAMS:
        msg += f'- {t}\n'
    msg += '\nWähle dein Team mit: !team <Teamname>'
    await ctx.send(msg)

@bot.command()
async def team(ctx, *, teamname):
    """Wähle dein Lieblingsteam für Benachrichtigungen."""
    if teamname not in TEAMS:
        await ctx.send('Team nicht gefunden. Nutze `!teams` für eine Liste aller Teams.')
        return
    user_teams[ctx.author.id] = teamname
    await ctx.send(f'Du erhältst nun Infos zu Spielen von **{teamname}**.')

@bot.command()
async def meinteam(ctx):
    """Zeigt dein aktuelles Lieblingsteam an."""
    team = user_teams.get(ctx.author.id)
    if team:
        await ctx.send(f'Dein aktuelles Lieblingsteam ist: **{team}**')
    else:
        await ctx.send('Du hast noch kein Lieblingsteam gewählt. Nutze `!teams` und dann `!team <Teamname>`.')

@bot.command()
async def hilfe(ctx):
    """Zeigt eine Übersicht der Bot-Befehle und Nutzung."""
    msg = (
        '**Fußball-Bot Befehle:**\n'
        '`!hilfe` – Diese Übersicht\n'
        '`!spiele` – Zeigt die heutigen Fußballspiele\n'
        '`!teams` – Zeigt eine Liste verfügbarer Teams\n'
        '`!team <Teamname>` – Wähle dein Lieblingsteam\n'
        '`!meinteam` – Zeigt dein aktuelles Lieblingsteam\n'
    )
    await ctx.send(msg)

@tasks.loop(hours=24)
async def daily_matches():
    await bot.wait_until_ready()
    today = datetime.now().strftime('%Y-%m-%d')
    matches = get_matches()
    if not matches:
        return
    for user_id, team in user_teams.items():
        user = bot.get_user(user_id)
        if user:
            team_matches = [m for m in matches if team.lower() in (m['home'].lower(), m['away'].lower())]
            if team_matches:
                msg = f'**Spiele für {team} heute:**\n'
                for match in team_matches:
                    msg += f"{match['home']} vs {match['away']} ({match['time']})\n"
                try:
                    await user.send(msg)
                except:
                    pass

def get_matches(ctx=None):
    global api_request_count_minute, api_request_count_month
    today = datetime.now().strftime('%Y-%m-%d')
    headers = {'X-Auth-Token': API_TOKEN}
    # API-Limit prüfen
    with api_limit_lock:
        if api_request_count_minute >= API_MINUTE_LIMIT:
            if ctx:
                import asyncio
                asyncio.create_task(ctx.send(':warning: API-Minutenlimit erreicht. Bitte warte eine Minute.'))
            print('API-Minutenlimit erreicht.')
            return []
        if api_request_count_month >= API_MONTH_LIMIT:
            if ctx:
                import asyncio
                asyncio.create_task(ctx.send(':warning: API-Monatslimit erreicht.'))
            print('API-Monatslimit erreicht.')
            return []
        api_request_count_minute += 1
        api_request_count_month += 1
        # Warnung bei 80% Auslastung
        if api_request_count_minute == int(API_MINUTE_LIMIT*0.8) and ctx:
            import asyncio
            asyncio.create_task(ctx.send(':warning: Achtung, du hast 80% des Minutenlimits erreicht!'))
        if api_request_count_month == int(API_MONTH_LIMIT*0.8) and ctx:
            import asyncio
            asyncio.create_task(ctx.send(':warning: Achtung, du hast 80% des Monatslimits erreicht!'))
    try:
        resp = requests.get(API_URL.format(date=today), headers=headers)
        data = resp.json()
        matches = []
        for m in data.get('matches', []):
            matches.append({
                'home': m['homeTeam']['name'],
                'away': m['awayTeam']['name'],
                'time': m['utcDate'][11:16]
            })
        return matches
    except Exception as e:
        print('Fehler beim Abrufen der Spiele:', e)
        return []

if __name__ == '__main__':
    bot.run(TOKEN)
