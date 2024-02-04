from aiogram.dispatcher.filters.state import State, StatesGroup


class HeadToHead(StatesGroup):
    league_name = State()  # Will be represented in storage as 'HeadToHead:league_name' and so on
    season = State()
    team_1 = State()
    team_2 = State()
    result_number = State()


class LiveScore(StatesGroup):
    league_name = State()  # Will be represented in storage as 'HeadToHead:league_name' and so on


class UpComing(StatesGroup):
    league_name = State()  # Will be represented in storage as 'HeadToHead:league_name' and so on


class GetTable(StatesGroup):
    league_name = State()  # Will be represented in storage as 'HeadToHead:league_name' and so on