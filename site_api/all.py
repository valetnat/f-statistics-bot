import requests

from typing import Optional, Dict, List
from data import config


async def get_all_leagues() -> Optional[List[dict]]:
    url = f"https://api.sportmonks.com/v3/football/leagues?api_token={config.SITE_TOKEN}&include=country&season"
    response = requests.get(url)

    if response.status_code == 200:
        json_res = response.json()

        try:
            return [
                {
                    'league_name': league['name'],
                    'league_id': league['id'],
                    'country_name': league['country']['name'],
                    'country_id': league['country']['id'],
                    'league_type': league['type'],
                    'league_sub_type': league['sub_type']
                }
                for league in json_res['data']
            ]
        except Exception as exp:
            return None


async def get_teams(league_name):
    url = f'https://api.sportmonks.com/v3/football/teams?api_token={config.SITE_TOKEN}&include=seasons.league;country'
    response = requests.get(url)
    if response.status_code == 200:
        json_res = response.json()

        league_teams = dict()

        for team, data in enumerate(json_res['data']):
            if data['seasons']:
                for season in data['seasons']:
                    if season['league']['name'] == league_name:
                        league_teams.update({team:
                                                 {'team_id': data['id'],
                                                  'team_name': data['name'],
                                                  'country_id': data['country']['id'],
                                                  'country_name': data['country']['name']
                                                    }
                                             }
                                            )
        return league_teams


async def get_all_teams():
    url = f'https://api.sportmonks.com/v3/football/teams?api_token={config.SITE_TOKEN}&include=seasons.league;country'
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        json_res = response.json()

        all_teams = dict()

        for team, data in enumerate(json_res['data']):
            all_teams.update({team:
                                     {'team_id': data['id'],
                                      'team_name': data['name'],
                                      'country_id': data['country']['id'],
                                      'country_name': data['country']['name']}}
                                )
        return all_teams


async def api_get_teams_example(country_id: str) -> Optional[Dict]:
    url: str = f""" https://api.sportmonks.com/v3/football/teams/countries/{country_id}?api_token={config.SITE_TOKEN}&include=country """
    response = requests.get(url)
    if response.status_code == 200:
        json_res = response.json()

        try:
            league_teams = dict()

            for team, data in enumerate(json_res['data']):
                league_teams.update({team:
                                         {'team_id': data['id'],
                                          'team_name': data['name'],
                                          'country_id': data['country']['id'],
                                          'country_name': data['country']['name']
                                          }
                                     })
            return league_teams

        except Exception as exp:
            return None


async def get_upcoming_event():
    url = f"https://api.sportmonks.com/v3/football/fixtures/upcoming/markets/1?api_token={config.SITE_TOKEN}&include=league;venue"
    response = requests.get(url)
    if response.status_code == 200:
        json_res = response.json()

        upcoming_matches = dict()

        try:
            for data in json_res['data']:
                if data['league']['name'] in upcoming_matches.keys():
                    upcoming_matches[data['league']['name']].append({'league_id': data['league']['id'], 'league_name': data['league']['name'], 'starting_at': data['starting_at'], 'match_name': data['name'], 'venue_id': data['venue']['id'], 'venue_name': data['venue']['name']})
                else:
                    upcoming_matches[data['league']['name']] = [{'league_id': data['league']['id'], 'league_name': data['league']['name'], 'starting_at': data['starting_at'], 'match_name': data['name'], 'venue_id': data['venue']['id'], 'venue_name': data['venue']['name']}]

            return upcoming_matches

        except Exception as exp:
            return None


async def get_livescore() -> Optional[Dict]:
    url: str = f"https://api.sportmonks.com/v3/football/livescores/inplay?api_token={config.SITE_TOKEN}&include=state;league;events;scores;participants;season;periods"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        json_res = response.json()

        try:
            match_dict = dict()

            for match, data in enumerate(json_res['data']):
                match_dict.update({match: {
                    'descr': data['name'],
                    # 'result_info': data['result_info'],
                    'played_at': data['starting_at'],
                    # 'season_id': data['season']['id'],
                    # 'season_name': data['season']['name'],
                    # 'country_id': data['league']['country']['id'],
                    # 'country_name': data['league']['country']['name'],
                    'league_id': data['league']['id'],
                    'league_name': data['league']['name'],
                    # 'stage_type': data['stage']['type_id'],
                    # 'stage_name': data['stage']['name'],
                    # 'venue_id': data['venue']['id'],
                    # 'venue_name': data['venue']['name'],
                    # 'city_id': data['venue']['city']['id'],
                    # 'city_name': data['venue']['city']['name']
                }})

                if data['scores']:
                    for elem in data['scores']:
                        if elem['description'] == "CURRENT" and elem['score']['participant'] == 'home':
                            match_dict[match].update({'score_home': elem['score']['goals']})
                        if elem['description'] == "CURRENT" and elem['score']['participant'] == 'away':
                            match_dict[match].update({'score_away': elem['score']['goals']})

                if data['participants']:
                    for elem in data['participants']:
                        if elem['meta']['location'] == 'home':
                            match_dict[match].update({'home_team_id': elem['id'], 'home_team_name': elem['name'], 'home_team_image': elem['image_path']})
                        if elem['meta']['location'] == 'away':
                            match_dict[match].update({'away_team_id': elem['id'], 'away_team_name': elem['name'], 'home_team_image': elem['image_path']})

                if data['periods']:

                    for elem in data['periods']:

                        if data['state']['name'] == '1st Half':
                            match_dict[match].update({'cur_period': elem['description'], 'cur_minute': elem['minutes']})

                        elif data['state']['name'] == 'Half Time':
                            match_dict[match].update({'cur_period': 'halftime', 'cur_minute': None})

                        elif data['state']['name'] == '2nd Half':
                            match_dict[match].update({'cur_period': elem['description'], 'cur_minute': elem['minutes']})

                        elif data['state']['name'] == 'Extra Time':
                            match_dict[match].update({'cur_period': elem['description'], 'cur_minute': elem['minutes']})

                        elif data['state']['name'] == 'Extra Time - Break':
                            match_dict[match].update({'cur_period': 'extra time break', 'cur_minute': None})

                        elif data['state']['name'] == 'ET - 2nd Half':
                            match_dict[match].update({'cur_period': elem['description'], 'cur_minute': elem['minutes']})

                        elif data['state']['name'] == 'Regular time finished':
                            match_dict[match].update({'cur_period': elem['description'], 'cur_minute': elem['minutes']})

                        elif data['state']['name'] == 'Penalties - Break':
                            match_dict[match].update({'cur_period': 'penalties break', 'cur_minute': None})

                        elif data['state']['name'] == 'Penalty Shootout':
                            match_dict[match].update({'cur_period': elem['description'], 'cur_minute': elem['minutes']})

                        else:
                            match_dict[match].update({'cur_period': data['state']['name'], 'cur_minute': None})

            return match_dict

        except Exception as exp:
            return None


async def get_standings(league_id: int, current_season_id: int):
    url = f"https://api.sportmonks.com/v3/football/standings?api_token={config.SITE_TOKEN}&include=details.type;participant&filters=standingdetailTypes:129,130,131,132,133,134"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        json_res = response.json()

    try:
        teams_standings = dict()
        for team in json_res['data']:
            if team['league_id'] == league_id and team['season_id'] == current_season_id:
                team_stds = {'team_name': team['participant']['name'], 'points': team['points']}
                for standing in team['details']:
                    if standing['type']['name'] == 'Overall Matched Played':
                        team_stds.update({'games_played': standing['value']})
                    if standing['type']['name'] == 'Overall Won':
                        team_stds.update({'games_won': standing['value']})
                    if standing['type']['name'] == 'Overall Draw':
                        team_stds.update({'games_draw': standing['value']})
                    if standing['type']['name'] == 'Overall Lost':
                        team_stds.update({'games_lost': standing['value']})
                    if standing['type']['name'] == 'Overal Goals Scored':
                        team_stds.update({'goals_scored': standing['value']})
                    if standing['type']['name'] == 'Overall Goals Conceded':
                        team_stds.update({'goals_conceded': standing['value']})
                teams_standings.update({team['position']: team_stds})

        return teams_standings

    except Exception as exp:
        return None


async def get_current_season_id(league_id: int):
    url = f"https://api.sportmonks.com/v3/football/leagues?api_token={config.SITE_TOKEN}&include=currentSeason;country"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        json_res = response.json()

    try:
        for league in json_res['data']:
            if league["id"] == league_id:
                return league['currentseason']["id"]

    except Exception as exp:
        return None