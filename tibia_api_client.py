from abc import ABC, abstractmethod
import requests
from typing import Set, Dict

class GuildMemberProvider(ABC):
    @abstractmethod
    def get_guild_members(self, guild_name: str) -> Set[str]:
        """Get all members of a guild"""
        pass

class TibiaApiClient(GuildMemberProvider):
    def __init__(self):
        self.base_url = "https://api.tibiadata.com/v4"
    
    def get_guild_members(self, guild_name: str) -> Set[str]:
        """Get all members of a guild using TibiaData API"""
        try:
            print(f"\nObtendo membros da guild: {guild_name}")
            response = requests.get(f"{self.base_url}/guild/{guild_name}")
            if response.status_code == 200:
                data = response.json()
                members = data.get('guild', {}).get('members', [])
                return {member['name'].lower() for member in members}
            print(f"Erro ao consultar API da guild: Status {response.status_code}")
            return set()
        except Exception as e:
            print(f"Error fetching guild members for {guild_name}: {str(e)}")
            return set()
