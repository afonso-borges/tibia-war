from tibia_api_client import TibiaApiClient
from exp_data_provider import GuildStatsGainExpProvider, GuildStatsLossExpProvider
from guild_exp_calculator import GuildExpCalculator
import json
from datetime import datetime, timedelta
import os
from typing import List


def main(world: str, target_guilds: List[str]):
    # Configuration
    
    # Data do dia anterior (dois formatos: um para exibição e outro para nome do arquivo)
    previous_date_display = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
    previous_date_file = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Create providers
    guild_provider = TibiaApiClient()
    exp_providers = [GuildStatsGainExpProvider(world), GuildStatsLossExpProvider(world)]

    # Create calculator instance
    calculator = GuildExpCalculator(guild_provider, exp_providers, target_guilds)

    # Calculate and display results
    print(f"\nCalculando exp para as guilds: {', '.join(target_guilds)}")
    results = calculator.calculate_guild_exp()

    # Prepare data for JSON
    data_to_save = {
        "date": previous_date_display,
        "world": world,
        "guilds": {guild: exp for guild, exp in results.items()}
    }

    # Save results to JSON file
    results_dir = "resultados"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    json_file = os.path.join(results_dir, f"exp_results_{previous_date_file}.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)

    print(f"\nResultados para {previous_date_display}:")
    print("-" * 40)
    for guild, exp in results.items():
        print(f"Guild: {guild}")
        print(f"Total EXP: {exp:,}")
        print("-" * 40)
    
    print(f"\nResultados salvos em: {json_file}")


if __name__ == "__main__":
    main("Rasteibra", ["Rasteibra Encore", "Xandebro"])
    # main("Ourobra", ["Ourobra Encore", "Bombro"]) 
