# __init__.py
from .player_data import PlayerData, load_data

# Pre-load the data
_loaded_data = load_data()

def load() -> dict:
    """Load the player salary data and return it as a dictionary."""
    return _loaded_data.copy()

def get_player(name: str) -> PlayerData:
    """Get data for a specific player"""
    return _loaded_data.get(name)

def get_players_by_club(club: str) -> list:
    """Get all players from a specific club"""
    return [p for p in _loaded_data.values() if p.club.lower() == club.lower()]

def get_players_by_competition(competition: str) -> list:
    """Get all players from a specific competition"""
    return [p for p in _loaded_data.values() if p.competition.lower() == competition.lower()]

def get_players_by_nationality(nationality: str) -> list:
    """Get all players of a specific nationality"""
    return [p for p in _loaded_data.values() if p.nationality.lower() == nationality.lower()]

# Make the data accessible directly from the package
data = _loaded_data