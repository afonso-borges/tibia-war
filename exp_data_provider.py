from abc import ABC, abstractmethod
from typing import List, Tuple
import requests
from bs4 import BeautifulSoup
import traceback

class ExpDataProvider(ABC):
    @abstractmethod
    def get_exp_data(self) -> List[Tuple[str, int]]:
        """Get experience data for players"""
        pass

class GuildStatsExpProvider(ExpDataProvider):
    def __init__(self, world: str):
        self.world = world
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def _parse_exp_page(self, url: str) -> List[Tuple[str, int]]:
        """Parse guildstats.eu page and return list of (character_name, exp) tuples"""
        try:
            print(f"\nAcessando URL: {url}")
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                print(f"Error accessing URL: {url}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            table = None
            tables = soup.find_all('table')
            for t in tables:
                if t.find('tr'):
                    table = t
                    break
            
            if not table:
                print("Tabela não encontrada na página")
                return []

            results = []
            rows = table.find_all('tr')
            
            header_row = rows[0] if rows else None
            if header_row:
                headers = [col.text.strip() for col in header_row.find_all(['td', 'th'])]
                print("Colunas encontradas no cabeçalho:")
                for i, h in enumerate(headers):
                    print(f"Coluna {i}: '{h}'")
                
                name_col_index = -1
                exp_col_index = -1
                
                for i, header in enumerate(headers):
                    if header == "Nick":
                        name_col_index = i
                    elif header == "Daily exp":
                        exp_col_index = i
                
                if name_col_index == -1 or exp_col_index == -1:
                    print("Não foi possível encontrar as colunas necessárias. Procurando por 'Nick' e 'Daily exp'")
                    return []
                
                print(f"Índices encontrados - Nome: {name_col_index}, EXP: {exp_col_index}")
                
                data_rows = rows[1:]
                print(f"Encontradas {len(data_rows)} linhas na tabela")
                
                for row in data_rows:
                    cols = row.find_all(['td', 'th'])
                    if len(cols) > max(name_col_index, exp_col_index):
                        name = cols[name_col_index].text.strip()
                        exp_text = cols[exp_col_index].text.strip()
                        try:
                            exp = int(exp_text.replace(',', '').replace('+', '').replace('-', ''))
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

class GuildStatsGainExpProvider(GuildStatsExpProvider):
    def get_exp_data(self) -> List[Tuple[str, int]]:
        url = f"https://guildstats.eu/mostexp?world={self.world}&time=0&type=0"
        return self._parse_exp_page(url)

class GuildStatsLossExpProvider(GuildStatsExpProvider):
    def get_exp_data(self) -> List[Tuple[str, int]]:
        url = f"https://guildstats.eu/deaths?world={self.world}&type=0"
        # Os valores já vêm negativos do site, não precisamos inverter
        return self._parse_exp_page(url)
