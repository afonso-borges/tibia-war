import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple, Set
import traceback

class TibiaExpCalculator:
    def __init__(self, world: str, target_guilds: List[str]):
        self.world = world
        self.target_guilds = target_guilds
        self.exp_gained_url = f"https://guildstats.eu/mostexp?world={world}&time=0&type=0"
        self.exp_lost_url = f"https://guildstats.eu/deaths?world={world}&type=0"
        self.tibia_api_url = "https://api.tibiadata.com/v4"
        self.guild_members: Dict[str, Set[str]] = {}
        
    def _get_guild_members(self, guild_name: str) -> Set[str]:
        """Get all members of a guild using TibiaData API"""
        try:
            print(f"\nObtendo membros da guild: {guild_name}")
            response = requests.get(f"{self.tibia_api_url}/guild/{guild_name}")
            if response.status_code == 200:
                data = response.json()
                members = data.get('guild', {}).get('members', [])
                return {member['name'].lower() for member in members}
            print(f"Erro ao consultar API da guild: Status {response.status_code}")
            return set()
        except Exception as e:
            print(f"Error fetching guild members for {guild_name}: {str(e)}")
            return set()

    def _load_all_guild_members(self):
        """Load members of all target guilds"""
        for guild in self.target_guilds:
            self.guild_members[guild.lower()] = self._get_guild_members(guild)
            print(f"Guild {guild}: {len(self.guild_members[guild.lower()])} membros encontrados")

    def _get_player_guild(self, character_name: str) -> str:
        """Get player's guild from pre-loaded guild members"""
        character_name = character_name.lower()
        for guild, members in self.guild_members.items():
            if character_name in members:
                return guild
        return ''

    def _parse_exp_page(self, url: str, is_exp_gain: bool = True) -> List[Tuple[str, int]]:
        """Parse guildstats.eu page and return list of (character_name, exp) tuples"""
        try:
            print(f"\nAcessando URL: {url}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Error accessing URL: {url}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Tenta encontrar a tabela com dados
            table = None
            tables = soup.find_all('table')
            for t in tables:
                if t.find('tr'):  # Procura a primeira tabela que tem linhas
                    table = t
                    break
            
            if not table:
                print("Tabela não encontrada na página")
                return []

            results = []
            rows = table.find_all('tr')
            
            # Debug: mostrar o conteúdo do cabeçalho
            header_row = rows[0] if rows else None
            if header_row:
                headers = [col.text.strip() for col in header_row.find_all(['td', 'th'])]
                print("Colunas encontradas no cabeçalho:")
                for i, h in enumerate(headers):
                    print(f"Coluna {i}: '{h}'")
                
                # Procurar exatamente pela coluna "Daily exp" e "Name"
                name_col_index = -1
                exp_col_index = -1
                
                for i, header in enumerate(headers):
                    if header == "Nick":
                        name_col_index = i
                    elif header == "Daily exp":
                        exp_col_index = i
                
                if name_col_index == -1 or exp_col_index == -1:
                    print("Não foi possível encontrar as colunas necessárias. Procurando por 'Name' e 'Daily exp'")
                    return []
                
                print(f"Índices encontrados - Nome: {name_col_index}, EXP: {exp_col_index}")
                
                # Processar as linhas de dados
                data_rows = rows[1:]  # Skip header row
                print(f"Encontradas {len(data_rows)} linhas na tabela")
                
                for row in data_rows:
                    cols = row.find_all(['td', 'th'])
                    if len(cols) > max(name_col_index, exp_col_index):
                        name = cols[name_col_index].text.strip()
                        exp_text = cols[exp_col_index].text.strip()
                        try:
                            # Remove o sinal e as vírgulas, depois converte para inteiro
                            exp = int(exp_text.replace(',', '').replace('+', '').replace('-', ''))
                            # Se o texto original começava com '-', torna o número negativo
                            if exp_text.startswith('-'):
                                exp = -exp
                            results.append((name, exp))
                            print(f"Processado {name}: {exp_text} -> {exp:,}")
                        except ValueError:
                            print(f"Erro ao converter EXP para {name}: {exp_text}")
                            continue
            
            print(f"Processados {len(results)} jogadores com sucesso")
            return results
        except Exception as e:
            print(f"Error parsing page {url}: {str(e)}")
            print(f"Stack trace: {traceback.format_exc()}")
            return []

    def calculate_guild_exp(self) -> Dict[str, int]:
        """Calculate total exp for target guilds"""
        # Primeiro carrega todos os membros das guilds
        print("Carregando membros das guilds...")
        self._load_all_guild_members()
        
        guild_exp = {guild.lower(): 0 for guild in self.target_guilds}
        
        # Process exp gains
        print("\nBuscando ganhos de exp...")
        exp_gains = self._parse_exp_page(self.exp_gained_url)
        
        # Process exp losses
        print("\nBuscando perdas de exp...")
        exp_losses = self._parse_exp_page(self.exp_lost_url, is_exp_gain=False)
        
        # Combine gains and losses
        all_exp_changes = exp_gains + exp_losses
        
        # Process each player
        print("\nProcessando exp dos jogadores...")
        for character_name, exp in all_exp_changes:
            guild = self._get_player_guild(character_name)
            if guild:
                guild_exp[guild] += exp
                print(f"{character_name} ({guild}): {exp:+,} exp")
        
        return guild_exp

def main():
    # Configuration
    world = "Rasteibra"
    target_guilds = ["Xandebro", "Rasteibra Encore"]
    
    # Create calculator instance
    calculator = TibiaExpCalculator(world, target_guilds)
    
    # Calculate and display results
    print(f"\nCalculando exp para as guilds: {', '.join(target_guilds)}")
    results = calculator.calculate_guild_exp()
    
    print("\nResultados:")
    print("-" * 40)
    for guild, exp in results.items():
        print(f"Guild: {guild}")
        print(f"Total EXP: {exp:,}")
        print("-" * 40)

if __name__ == "__main__":
    main()
