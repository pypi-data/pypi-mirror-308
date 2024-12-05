# player_data.py
import os
import pandas as pd
import numpy as np
from typing import Dict, Any
from datetime import datetime


class PlayerData:
    def __init__(self, row):
        """Initialize player data from a DataFrame row"""
        self.name = str(row['Player'])
        self.weekly_salary_gbp_eur = self._safe_float(row['Gross P/W (GBP/EUR)'])
        self.weekly_salary_usd = self._safe_float(row['Gross P/W (USD)'])
        self.per_minute_usd = self._safe_float(row['Gross P/Min(USD)'])
        self.yearly_salary_gbp_eur = self._safe_float(row['Gross P/Y  (GBP/EUR)'])
        self.yearly_salary_usd = self._safe_float(row['Gross P/Y (USD)'])
        self.yearly_bonus_gbp_eur = self._safe_float(row['Gross P/Y  (GBP/EUR) BONUS'])

        # Handle dates
        self.signed_date = pd.to_datetime(row['Signed']).date() if pd.notna(row['Signed']) else None
        self.expiration_date = pd.to_datetime(row['Expiration']).date() if pd.notna(row['Expiration']) else None

        self.years_remaining = self._safe_int(row['Years Remaining'])
        self.gross_remaining_usd = self._safe_float(row['Gross Remaining (USD)'])
        self.age = self._safe_int(row['Age'])
        self.nationality = str(row['Nationality'])
        self.club = str(row['Club'])
        self.competition = str(row['Competition'])

    @staticmethod
    def _safe_float(value) -> float:
        """Safely convert value to float, return 0.0 if conversion fails"""
        try:
            if pd.isna(value) or value == '':
                return 0.0
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def _safe_int(value) -> int:
        """Safely convert value to int, return 0 if conversion fails"""
        try:
            if pd.isna(value) or value == '':
                return 0
            return int(float(value))
        except (ValueError, TypeError):
            return 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert player data to dictionary"""
        return {
            'name': self.name,
            'weekly_salary': {
                'gbp_eur': self.weekly_salary_gbp_eur,
                'usd': self.weekly_salary_usd,
                'per_minute_usd': self.per_minute_usd
            },
            'yearly_salary': {
                'gbp_eur': self.yearly_salary_gbp_eur,
                'usd': self.yearly_salary_usd,
                'bonus_gbp_eur': self.yearly_bonus_gbp_eur
            },
            'contract': {
                'signed': self.signed_date.isoformat() if self.signed_date else None,
                'expiration': self.expiration_date.isoformat() if self.expiration_date else None,
                'years_remaining': self.years_remaining,
                'gross_remaining_usd': self.gross_remaining_usd
            },
            'personal': {
                'age': self.age,
                'nationality': self.nationality
            },
            'club': {
                'name': self.club,
                'competition': self.competition
            }
        }


def load_data() -> Dict[str, PlayerData]:
    """Load the player salary data and return it as a dictionary"""
    try:
        # Get the absolute path to the data directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, 'data', 'player_salaries.xlsx')

        # Read the Excel file
        df = pd.read_excel(
            data_path,
            dtype={
                'Player': str,
                'Nationality': str,
                'Club': str,
                'Competition': str
            },
            na_values=['', 'NA', 'N/A', '#N/A'],
            keep_default_na=True
        )

        # Convert DataFrame to dictionary of PlayerData objects
        players = {}
        for _, row in df.iterrows():
            try:
                player = PlayerData(row)
                players[player.name] = player
            except Exception as e:
                print(f"Error processing player {row['Player']}: {str(e)}")
                continue

        if not players:
            raise ValueError("No players were successfully loaded from the Excel file")

        return players

    except Exception as e:
        print(f"Error loading player data: {str(e)}")
        return None  # Return None instead of empty dict to trigger error handling