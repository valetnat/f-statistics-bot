# 📈 Football Statistics Bot
️This is a [Telegram Bot](https://core.telegram.org/bots/api/) that provides users with match schedules, retrospective match data, 
livescores, standings and other comprehensive Football statistics from [sportmonks.com](https://docs.sportmonks.com/football/welcome/getting-started/).
The Bot is written in [Python v3.10](https://docs.python.org/3.10/) using [aiogram](https://docs.aiogram.dev/en/latest/) and  [mySQL](https://dev.mysql.com/doc/).

## Navigation
  * [What can it do?](#what-can-it-do?)
      * [Add a league to database](#add-a-league-to-the-database)
      * [Delete a league from the database](#delete-a-league-from-the-database)
      * [Get a retrospective match score](#get-a-retrospective-match-score)
      * [Get the current season league table](#get-the-current-season-league-table)
      * [Get the upcoming matches](#get-the-upcoming-matches)
      * [Get livescores](#get-livescores)
      * [Adjust the timezone](#adjust-the-timezone)
  * [Getting started](#getting-started)
      * [Installation](#installation)
      * [Bot settings](#bot-settings)
      * [Database settings](#database-settings)
  * [Bot structure](#bot-structure)


# What can it do?

**Commands that are available for all users including admins**

```/start``` - start the bot <br>
```/help``` - how to use<br>
```/head_to_head``` - get a football match scores between some teams<br>
```/livescore``` - get livescore matches information<br>
```/upcoming``` - get information about upcoming matches<br>
```/get_table``` - get a league table<br>
```/settings``` - set your timezone to display valid time<br>

**Commands that are available only for admins**

```/add_league``` add a league to the database<br>
```/del_league``` delete a league from the database<br>

## Add a league to the database
The command ```/add_league``` is used to add chosen league to the database. After selection ```/add_league``` the bot will send all available leagues in your [sportmonks.com](https://sportmonks.com/) plan. In essence, admins can adjust leagues which will be available for users. 

**Warning**: Make sure that the database has league(s) that user will be able to request.

![add](https://github.com/valetnat/f-statistics-bot/blob/0f8aa0da409580663d2410c03c7d68ba62c993e0/add_league.PNG)


## Delete a league from the database
The command ```/del_league``` is used to delete chosen league from the database. 
If admins delete league it will be hidden for users.

![delete](https://github.com/valetnat/f-statistics-bot/blob/0f8aa0da409580663d2410c03c7d68ba62c993e0/del_league.PNG)


## Get a retrospective match score
After selection ```/head_to_head``` the bot will ask you to choose a league, a season and rivals. 
All messages are provided with markup buttons to simplify selection and also to ensure correct data input.

![head to head](https://github.com/valetnat/f-statistics-bot/blob/0f8aa0da409580663d2410c03c7d68ba62c993e0/head_to_head.PNG)


## Get the current season league table
After selection ```/get_table``` the bot will ask you to choose a league by selecting the league button. 
Data will be represented as a table below:

![table](https://github.com/valetnat/f-statistics-bot/blob/0f8aa0da409580663d2410c03c7d68ba62c993e0/get_table.PNG)


## Get the upcoming matches
After selection ```/upcoming``` the bot will ask you to choose a league by selecting the league button. 
Bot will send you a message about upcoming match(es) 5 days ahead.

![upcoming](https://github.com/valetnat/f-statistics-bot/blob/0f8aa0da409580663d2410c03c7d68ba62c993e0/upcoming.PNG)


## Get livescores
After selection ```/livescore``` the bot will ask you to choose a league. 
Livescore information contains match status(1st, 2n half, extra times, breaks etc.), match score and time elapsed.

![livescore](https://github.com/valetnat/f-statistics-bot/blob/0f8aa0da409580663d2410c03c7d68ba62c993e0/livescore.PNG)


## Adjust the timezone
After selection ```/settings``` the bot will ask you to share the location. 

**Warning**: Be aware that if user denies to share the location the time will be displayed as CET.

![timezone](https://github.com/valetnat/f-statistics-bot/blob/42499ee8f0d465f03cd9b1fa472d2e9cd1ad2604/timezone.PNG)

# Getting started

## Installation  
1. Go to [@BotFather](https://t.me/telegram), create a new bot, write down its token;
2. Go to [Sportmonks.com](https://docs.sportmonks.com/football/welcome/getting-started/), register and get API token;
3. Clone this repo and `cd` into it;  
4. Copy `env_dist` to `.env` (with dot); 
5. Install requirements ```pip install -r requirements.txt```;
6. Configure default variables as shown in [Bot settings](#bot-settings) and [Database settings](#database-settings);  
7. Run pooling ```python main.py```
8. Add leagues to the database using ```/add_league``` command.

## Bot settings:

`ADMINS` - administrators Ids divided by ,
```zhs
# example
ADMINS=12345643,42345677,123676
# or one admin
ADMINS=12345678
```

`BOT_TOKEN` - bot token from [@BotFather](https://t.me/BotFather)
```zhs
# example
BOT_TOKEN=123452345243:AAfdfdh3fdssk23ofds
```

`SITE_TOKEN` - site token from [Sportmonks](https://docs.sportmonks.com/cricket/getting-started/getting-started)
```zhs
# example
SITE_TOKEN=fdsfjsh3^YTFDkdkfhdddsyffg
```

`SITE_HOST` - host from [Sportmonks](https://docs.sportmonks.com/cricket/getting-started/getting-started)
```zhs
# example
SITE_HOST=api.sportmonks.com/v3/
```

## Database settings
```zhs
# mySQL database 
DB_USER=<some username>
DB_PASSWORD=<some password>
DB_HOST=<some host>

DB_NAME=<some database name>
```

# Bot structure

```zhs
├───data               # bot configuration
├───database           # interaction with database
├───filters            # aiogram filters
├───handlers   
│   ├───admins         # admins message handlers 
│   └───users          # users message handlers 
├───keyboards   
│   ├───default        # aiogram markups 
│   └───inline         # aiogram inline markups 
├───models             # database models
├───site_api           # interaction with api
├───states             # aiogram states
└───utils              # miscellaneous features
```