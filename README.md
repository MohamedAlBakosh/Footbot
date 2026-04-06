
# Discord Fußball-Bot

Ein Discord-Bot in Python, der täglich eine Übersicht der Fußballspiele liefert und es ermöglicht, Teams auszuwählen, für die man detaillierte Spielinfos erhalten möchte.

## Funktionen

- Tagesübersicht: Mit `!spiele` erhältst du eine Liste aller heutigen Fußballspiele.
- Team-Auswahl: Mit `!teams` siehst du alle verfügbaren Teams und kannst mit `!team <Teamname>` dein Lieblingsteam wählen.
- Team-Info: Mit `!meinteam` siehst du dein aktuelles Lieblingsteam.
- Automatische Benachrichtigung: Der Bot verschickt jeden Tag die Spiele deiner gewählten Teams per Direktnachricht.
- API-Limit-Überwachung: Der Bot warnt dich, wenn du das Minuten- oder Monatslimit fast erreichst oder überschreitest.
- Hilfe: Mit `!hilfe` bekommst du eine Übersicht aller Befehle.

## Installation & Einrichtung

1. **Python 3.8+ installieren**
2. Repository/Projekt herunterladen oder klonen
3. Abhängigkeiten installieren:
	```
	pip install -r requirements.txt
	```
4. `.env`-Datei anlegen (siehe `.env.example`) und folgende Werte eintragen:
	- `DISCORD_TOKEN=...` (Dein Discord-Bot-Token)
	- `FOOTBALL_API_KEY=...` (Dein Sportmonks API-Key)
5. Bot starten:
	```
	python bot.py
	```

## Nutzung

Lade den Bot auf deinen Discord-Server ein und nutze folgende Befehle im Chat:

| Befehl                | Beschreibung                                              |
|-----------------------|----------------------------------------------------------|
| `!hilfe`              | Zeigt diese Übersicht                                    |
| `!spiele`             | Zeigt die heutigen Fußballspiele                         |
| `!teams`              | Zeigt eine Liste verfügbarer Teams                       |
| `!team <Teamname>`    | Wähle dein Lieblingsteam                                 |
| `!meinteam`           | Zeigt dein aktuelles Lieblingsteam                       |

**Hinweis:**
Das API-Limit für kostenlose Sportmonks-Keys beträgt 10 Anfragen/Minute und 2.500/Monat. Der Bot warnt dich automatisch, wenn du das Limit fast erreichst.

## Beispiel

```
!hilfe
!teams
!team Bayern München
!spiele
!meinteam
```

Viel Spaß beim Ausprobieren!
