import py
import pytest
from program import Player, EloCalculator

@pytest.fixture
def player_stats():
    pla = Player()
    pla.kills = 12
    pla.deaths = 10
    pla.assists = 2
    pla.objs = 4
    return pla

@pytest.fixture()
def team_one_stats():
    pass

@pytest.fixture()
def team_two_stats():
    pass

def test_relative_elo(player_stats):
    e = EloCalculator()
    elo = e.CalculateElo(player_stats, 1, True)
    assert elo == 36