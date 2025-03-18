# Tibia Guild EXP Calculator

This script calculates the total experience (EXP) gained and lost by specific guilds in Tibia, using data from guildstats.eu and the official Tibia API.

## Features

- Collects EXP gain data from guildstats.eu
- Collects EXP loss data (deaths) from guildstats.eu
- Uses the Tibia API to identify guild members
- Calculates the total EXP for selected guilds

## Project Structure

The project follows SOLID principles and is organized into the following files:

- `main.py`: Entry point of the program
- `tibia_api_client.py`: Client for the Tibia API
- `exp_data_provider.py`: EXP data providers from guildstats.eu
- `guild_exp_calculator.py`: Guild EXP calculator

## Requirements

```bash
pip install -r requirements.txt
```

## How to Use

1. Edit the `main.py` file and modify the following variables:
   ```python
   world = "World"  # Name of the Tibia world
   target_guilds = ["Guild 1", "Guild 2"]  # List of guilds to monitor
   ```

2. Run the script:
   ```bash
   python main.py
   ```

## Extensibility

The project was developed following SOLID principles, allowing for easy extension:

1. To add a new source of EXP data:
   - Implement the `ExpDataProvider` interface
   - Add the new implementation to the `exp_providers` list in `main.py`

2. To use a different source of guild data:
   - Implement the `GuildMemberProvider` interface
   - Use the new implementation when creating the `GuildExpCalculator` in `main.py`

## Notes

- The script considers both gained and lost EXP
- The results show the total balance (gains - losses) for each monitored guild
- Results are displayed in the terminal output
