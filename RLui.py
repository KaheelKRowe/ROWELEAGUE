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

# Displays a table of players, used for displaying free agents and rookies.
def print_player_table(players):
    print(f"\n{'Player ID':<10} {'Name':<22} {'Position':<15} {'Age':<15} {'OVR':<10} {'Pot':<10}")
    print("-" * 80)
    for player in players:
        name = f"{player.player_first} {player.player_last}"
        print(f"{player.player_id:<10} | {name:<20} | {player.position:<10} | Age: {player.age:<10} | OVR: {player.overall:<10} | Pot: {player.get_potential_grade():<10}")

# Displays a list of free agents in the league, comes with several sort options.
def display_free_agents(league):
    league.free_agents.sort(key=lambda p: p.overall, reverse=True)
    print_player_table(league.free_agents)
    choice = None
    while choice != '2':
        print("| 1. Sort | 2. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            choice_2 = None
            while choice_2 != '6':
                print("| 1. OVR | 2. Pos | 3. Salary | 4. Age | 5. Pot")
                print("6. Exit")
                choice_2 = input("Enter sort choice: ")
                if choice_2 == '1':
                    league.free_agents.sort(key=lambda p: p.overall, reverse=True)
                    print_player_table(league.free_agents)
                elif choice_2 == '2':
                    position_map = {'1': 'PG', '2': 'SG', '3': 'SF', '4': 'PF', '5': 'C'}
                    print("1. PG | 2. SG | 3. SF | 4. PF | 5. C")
                    choice_3 = input("Enter position choice: ")
                    if choice_3 in position_map:
                        league.free_agents.sort(key=lambda p: p.overall, reverse=True)
                        filtered = [p for p in league.free_agents if p.position == position_map[choice_3]]
                        print_player_table(filtered)
                    else:
                        print("Invalid position choice. Please try again.")
                elif choice_2 == '3':
                    league.free_agents.sort(key=lambda p: p.salary, reverse=True)
                    print_player_table(league.free_agents)
                elif choice_2 == '4':
                    league.free_agents.sort(key=lambda p: p.age)
                    print_player_table(league.free_agents)
                elif choice_2 == '5':
                    league.free_agents.sort(key=lambda p: p.potential, reverse=True)
                    print_player_table(league.free_agents)
                elif choice_2 == '6':
                    return
                else:
                    print("Invalid choice. Please enter a valid choice")
        elif choice == '2':
            return
        else:
            print("Invalid choice. Please enter a valid choice")

# Allows the user to sign a free agent.
def sign_free_agent(league):
    while True:
        agent_choice = input("\nEnter a Player ID to sign: ")
        found = False
        for player in league.free_agents:
            if player.player_id == agent_choice:
                found = True
                if league.user_team.add_player(player):
                    league.free_agents.remove(player)
                    print(f"\nSigned {player.player_first} {player.player_last} | {player.position} | OVR: {player.overall} | Age: {player.age} | Salary: ${player.salary:,}")
                    confirm = input("Would you like to sign another player? (y/n): ")
                    if confirm.lower() == 'n':
                        return
                else:
                    print("Not enough cap space or roster space to sign this player.")
                    return
                break
        if not found:
            print("Player ID invalid. Please try again.")

# Runs the free agency period, letting the user compete with CPU teams for free agents day by day.
def free_agency_day(league):
    while True:
        league.calendar.display_date()
        print("\nFree Agency")
        print("1. View Free Agents")
        print("2. Sign Free Agents")
        print("3. Advance Day")
        print("4. Exit Free Agency")
        choice = input("Enter your choice: ")
        if choice == '1':
            display_free_agents(league)
        elif choice == '2':
            sign_free_agent(league)
        elif choice == '3':
            league.cpu_free_agency_day()
            league.calendar.advance_day()
            print(f"\n--- Day Advanced ---")
            if league.calendar.phase != "Free Agency":
                print(f"\nFree Agency has ended!")
                league.end_of_season()
                return
        elif choice == '4':
            return
        else:
            print("Invalid choice. Please enter a valid choice")

# Displays the main menu and handles user input for all game actions.
def main_menu(league):
    while True:
        league.calendar.display_date()
        print(f"\nMain Menu: | Phase: {league.calendar.phase}")
        print("1. View Team Roster")
        print("2. View Free Agents")
        print("3. View League Standings")
        print("4. Trades")
        print("5. Simulate Season")
        print("6. Advance Phase")
        print("7. Draft")
        print("8. Free Agency")
        print("9. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            league.get_team_roster(league.user_team.team_name)
        elif choice == '2':
            display_free_agents(league)
        elif choice == '3':
            league.display_standings()
        elif choice == '4':
            print("\nUnder Development: Trades")
        elif choice == '5':
            if league.calendar.phase != "Regular Season":
                print(f"\nSimulation is only available during the Regular Season.")
                print(f"Current phase: {league.calendar.phase}")
            else:
                confirm = input("\nAre you sure you want to simulate the season? (y/n): ")
                if confirm.lower() == 'y':
                    league.simulate_season()
                    league.display_standings()
                    print(f"\nSeason simulated! Current phase: {league.calendar.phase}")
        elif choice == '6':
            current = league.calendar.phase
            if current == "Regular Season":
                print("\nYou must simulate the season first!")
            elif current in ["Playoffs", "Trade Deadline"]:
                print(f"\nAdvancing through {current}...")
                while league.calendar.phase not in ["Draft", "Free Agency"]:
                    league.calendar.advance_day()
                print(f"\nPhase advanced to: {league.calendar.phase}")
            elif current == "Draft":
                print("\nThe draft is open — use option 7 to run the draft!")
            elif current == "Free Agency":
                print("\nFree agency is open — use option 8 to manage free agency!")
            else:
                league.calendar.advance_day()
                print(f"\nAdvanced to: {league.calendar.phase}")
        elif choice == '7':
            if league.calendar.phase != "Draft":
                print(f"\nThe draft is not currently open.")
                print(f"Current phase: {league.calendar.phase}")
            else:
                league.run_draft()
                # advance calendar to free agency after draft
                while league.calendar.phase == "Draft":
                    league.calendar.advance_day()
                print(f"\nDraft complete! Phase advanced to: {league.calendar.phase}")
        elif choice == '8':
            if league.calendar.phase != "Free Agency":
                print(f"\nFree agency is not currently open.")
                print(f"Current phase: {league.calendar.phase}")
            else:
                free_agency_day(league)
        elif choice == '9':
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-9.")