# 🔷 Football Statistics Bot
️Here you can get comprehensive statistics from chosen football teams and its games.

## Navigation
  * [What can it do?](#what-can-it-do?)
      * [Add a league to database](#add-a-league-to-the-database)
      * [Delete a league from the database](#delete-a-league-from-the-database)
      * [Get a retrospective match score](#get-a-retrospective-match-score)
      * [Get the current season league table](#get-the-current-season-league-table)
      * [Get the upcoming matches](#get-the-upcoming-matches)
      * [Get livescore](#get-livescore)
      * [Adjust the timezone](#adjust-the-timezone)
  * [Getting started](#getting-started)
  * [Simple use template](#simple-use-template)
  * [Configure environment variables](#configure-environment-variables)
      * [Bot settings](#bot-settings)
      * [Database](#database)
  * [Bot structure](#bot-structure)

<hr>

# What can it do?

```# Commands that are available for all users including admins```
```/start``` start bot <br>
```/help``` how to use<br>
```/head_to_head``` get a football match scores between some teams<br>
```/livescore``` get livescore matches information<br>
```/upcoming``` get information about upcoming matches<br>
```/get_table``` get a league table<br>
```/settings``` set your timezone to display valid time<br>
```# Commands that are available only for admins```
```/add_league``` add a league to the database<br>
```/del_league``` delete a league from the database<br>

## Add a league to the database
The command ```/add_league``` is used to add chosen league to the database. After selection ```/add_league``` the bot will send all available leagues in your plan in [sportmonks.com](https://sportmonks.com/). 
In essence, admins can adjust leagues which will be available for users. 

**Warning**: Make sure that the database has league(s) that user will be able to request.

![add](https://github.com/valetnat/f-statistics-bot/blob/0f8aa0da409580663d2410c03c7d68ba62c993e0/add_league.PNG)


## Delete a league from the database
The command ```/del_league``` is used to delete chosen league from the database. If admins delete league it will be hidden for users.

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


## Get livescore
After selection ```/livescore``` the bot will ask you to choose a league. 
Livescore information contains match status(1st, 2n half, extra times, breaks etc.), match score and time elapsed.

![livescore](https://github.com/valetnat/f-statistics-bot/blob/0f8aa0da409580663d2410c03c7d68ba62c993e0/livescore.PNG)


## Adjust the timezone
After selection ```/settings``` the bot will ask you to share the location. 
**Warning**: Be aware that if user denies to share the location the time will be displayed as CET.

![timezone](https://github.com/valetnat/f-statistics-bot/blob/083056ceccdb6192fbd0e3535259495a4e45c73b/timezone.PNG)

# Getting started

## Simple use template

<a href="https://github.com/valetnat/f-statistics-bot/generate">Click here to create repository from this template</a> or: 
```zhs
$ git clone https://github.com/valetnat/f-statistics-bot <your project name>
$ cd <your project name>
$ pip install -r requirements.txt

# run pooling
$ python main.py
```

## Configure environment variables
Copy file `.env.exm` and rename it to `.env`
```
$ cp .env.exm .env
```
Than configure variables
```bash
$ vim .env
# or 
$ nano .env
```

# Bot settings:

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

`SITE_TOKEN` - get site token from [Sportmonks](https://docs.sportmonks.com/cricket/getting-started/getting-started)
```zhs
# example
SITE_TOKEN=fdsfjsh3^YTFDkdkfhdddsyffg
```

`SITE_HOST` - bot token from [Sportmonks](https://docs.sportmonks.com/cricket/getting-started/getting-started)
```zhs
# example
SITE_HOST=api.sportmonks.com/v3/
```

# Database
mySQL is using as database

```zhs
DB_USER=<some username>
DB_PASSWORD=<some password>
DB_HOST=<some host>

DB_NAME=<some database name>
```

# Bot structure
```zhs

├───data               # bot configuration
├───database           # interaction with database
├───filters            # some aiogram filters
├───handlers   
│   ├───admins         # admins message handlers 
│   └───users 
├───keyboards   
│   ├───default        # aiogram markups 
│   └───inline         # aiogram inline markups 
├───models             # database models
├───site_api           # interaction with api
├───states             # aiogram states
└───utils              # some helpful things
```


#### Installation  
1. Go to [@BotFather](https://t.me/telegram), create a new bot, write down its token, add it to your existing group 
and **make bot an admin**. You also need to give it "Delete messages" permission.  
2. Create a separate group where report messages will be sent and add all group admins there. 
**Remember**: anyone who is in that group may perform actions like "Delete", "Ban" and so on, so be careful.  
3. Use some bot like [@my_id_bot](https://t.me/my_id_bot) to get IDs of these two groups;  
4. Clone this repo and `cd` into it;  
5. Copy `env_dist` to `.env` (with dot). **Warning**: files starting with dot may be hidden in Linux, 
so don't worry if you stop seeing this file, it's still here!  
6. Replace default values with your own;  
7. Now choose installation method: **systemd** or **Docker**