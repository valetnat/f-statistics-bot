import requests

from data import config
from typing import Optional, Dict, List


async def api_head_to_head(team_id_1: int, team_id_2: int, league_id: int, season_name: str) -> Optional[Dict]:
    url: str = f'https://api.sportmonks.com/v3/football/fixtures/head-to-head/{team_id_1}/{team_id_2}?api_token={config.SITE_TOKEN}&include=scores;participants;season;stage;league.country;venue.city'
    response = requests.get(url)
    if response.status_code == 200:
        json_res = response.json()

        try:
            match_dict = dict()

            for match, data in enumerate(json_res['data']):
                if league_id == data['league']['id'] and season_name == data['season']['name']:
                    match_dict.update({match: {
                        'descr': data['name'],
                        'result_info': data['result_info'],
                        'played_at': data['starting_at'],
                        'season_id': data['season']['id'],
                        'season_name': data['season']['name'],
                        'country_id': data['league']['country']['id'],
                        'country_name': data['league']['country']['name'],
                        'league_id': data['league']['id'],
                        'league_name': data['league']['name'],
                        'stage_type': data['stage']['type_id'],
                        'stage_name': data['stage']['name'],
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
            return match_dict
        except Exception as exp:

            return None


async def api_get_available_season(league_name) -> Optional[Dict]:
    url: str = f'https://api.sportmonks.com/v3/football/leagues/search/{league_name}?api_token={config.SITE_TOKEN}&include=seasons'
    response = requests.get(url)
    if response.status_code == 200:
        json_res = response.json()

        try:
            season_dict = dict()

            for league in json_res['data']:
                if league['name'] == league_name:
                    if league['seasons']:
                        for season, data in enumerate(league['seasons']):
                            season_dict.update({season: {
                                'season_id': data['id'],
                                'season_name': data['name']
                            }}
                            )
            return season_dict

        except Exception as exp:
            return None


async def api_get_teams(country_id: int, season_name: str, league_id: int) -> Optional[List]:
    url = f'https://api.sportmonks.com/v3/football/teams/countries/{country_id}?api_token={config.SITE_TOKEN}&include=seasons'
    response = requests.get(url)
    if response.status_code == 200:
        json_res = response.json()

        try:
            teams_list = list()

            for team in json_res['data']:
                if team['seasons']:
                    for season in team['seasons']:
                        if season['name'] == season_name and season['league_id'] == league_id:
                            teams_list.append(team['name'])
            return teams_list

        except Exception as exp:
            return None