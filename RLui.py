from RLleague import League

# Displays a list of the teams in the league to the user and prompts them to choose one, will provide an error if an invalid name or id is entered and prompts the user to try again until a valid team is selected.
def display_teams(league):
    league.teams.sort(key=lambda t: t.team_id)
    print(f"{'Team ID':<10} {'Team Name':<20} {'Conference':<10}")
    print("-" * 60)
    for team in league.teams:
        print(f"{team.team_id:<10} {team.team_name:<20} {team.conference:<10}")
    while True:
        team_choice = input("\nEnter a Team ID or Name to choose it: ")
        for team in league.teams:
            if team.team_name == team_choice or team.team_id == team_choice:
                league.get_team_roster(team_choice)
                league.user_team = team
                break
        if league.user_team:
            print(f"\nYou have selected the {league.user_team.team_name}!")
            break
        else:
            print(f"Invalid choice. Please enter a valid Team ID or Name.")

# Displays a list of free agents in the league.
def display_free_agents(league):
    print(f"\n{'Player ID':<10} {'Name':<22} {'Position':<15} {'Age':<15} {'OVR':<10} {'Pot':<10}")
    print("-" * 80)
    for player in league.free_agents:
        name = f"{player.player_first} {player.player_last}"
        print(f"{player.player_id:<10} | {name:<20} | {player.position:<10} | Age: {player.age:<10} | OVR: {player.overall:<10} | Pot: {player.get_potential_grade():<10}")

def main_menu(league):
    choice = None
    while choice != '6':
        print("\nMain Menu:")
        print("1. View Team Roster")
        print("2. View Free Agents")
        print("3. View League Standings")
        print("4. Trades")
        print("5. Simulation")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            league.get_team_roster(league.user_team.team_name)
        elif choice == '2':
            display_free_agents(league)
        elif choice == '3':
            league.display_standings()
        elif choice == '4':
            print("\n Under Development: Trades")
        elif choice == '5':
            confirm = input("\nAre you sure you want to simulate the season? (y/n): ")
            if confirm.lower() == 'y':
                league.simulate_season()
                league.display_standings()
                league.end_of_season()
        elif choice == '6':
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")