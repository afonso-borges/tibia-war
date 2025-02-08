from typing import List, Dict, Set
from tibia_api_client import GuildMemberProvider
from exp_data_provider import ExpDataProvider

class GuildExpCalculator:
    def __init__(
        self,
        guild_member_provider: GuildMemberProvider,
        exp_providers: List[ExpDataProvider],
        target_guilds: List[str]
    ):
        self.guild_member_provider = guild_member_provider
        self.exp_providers = exp_providers
        self.target_guilds = target_guilds
        self.guild_members: Dict[str, Set[str]] = {}
    
    def _load_all_guild_members(self):
        """Load members of all target guilds"""
        for guild in self.target_guilds:
            self.guild_members[guild.lower()] = self.guild_member_provider.get_guild_members(guild)
            print(f"Guild {guild}: {len(self.guild_members[guild.lower()])} membros encontrados")

    def _get_player_guild(self, character_name: str) -> str:
        """Get player's guild from pre-loaded guild members"""
        character_name = character_name.lower()
        for guild, members in self.guild_members.items():
            if character_name in members:
                return guild
        return ''

    def calculate_guild_exp(self) -> Dict[str, int]:
        """Calculate total exp for target guilds"""
        print("Carregando membros das guilds...")
        self._load_all_guild_members()
        
        guild_exp = {guild.lower(): 0 for guild in self.target_guilds}
        
        # Process exp from all providers
        print("\nBuscando dados de exp...")
        all_exp_changes = []
        for provider in self.exp_providers:
            all_exp_changes.extend(provider.get_exp_data())
        
        # Process each player
        print("\nProcessando exp dos jogadores...")
        for character_name, exp in all_exp_changes:
            guild = self._get_player_guild(character_name)
            if guild:
                guild_exp[guild] += exp
                print(f"{character_name} ({guild}): {exp:+,} exp")
        
        return guild_exp
