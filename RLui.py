from RLtrades import Trade, calculate_trade_value

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

# Displays the rosters for every team in the league
def display_all_rosters(league):
    for team in sorted(league.teams, key=lambda t: t.team_name):
        league.get_team_roster(team.team_name)

# Displays a table of players, used for displaying free agents and rookies.
def print_player_table(players):
    print(f"\n{'Player ID':<10} {'Name':<22} {'Position':<15} {'Age':<15} {'OVR':<10} {'Pot':<10}")
    print("-" * 80)
    for player in players:
        name = f"{player.player_first} {player.player_last}"
        print(f"{player.player_id:<10} | {name:<20} | {player.position:<10} | Age: {player.age:<10} | OVR: {player.overall:<10} | Pot: {player.get_potential_grade():<10}")

# Handles the sort options for viewing players.
def sort_and_display(player_list, label="Players"):
    player_list.sort(key=lambda p: p.overall, reverse=True)
    print_player_table(player_list)
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
                    player_list.sort(key=lambda p: p.overall, reverse=True)
                    print_player_table(player_list)
                elif choice_2 == '2':
                    position_map = {'1': 'PG', '2': 'SG', '3': 'SF', '4': 'PF', '5': 'C'}
                    print("1. PG | 2. SG | 3. SF | 4. PF | 5. C")
                    choice_3 = input("Enter position choice: ")
                    if choice_3 in position_map:
                        player_list.sort(key=lambda p: p.overall, reverse=True)
                        filtered = [p for p in player_list if p.position == position_map[choice_3]]
                        print_player_table(filtered)
                    else:
                        print("Invalid position choice. Please try again.")
                elif choice_2 == '3':
                    player_list.sort(key=lambda p: p.salary, reverse=True)
                    print_player_table(player_list)
                elif choice_2 == '4':
                    player_list.sort(key=lambda p: p.age)
                    print_player_table(player_list)
                elif choice_2 == '5':
                    player_list.sort(key=lambda p: p.potential, reverse=True)
                    print_player_table(player_list)
                elif choice_2 == '6':
                    return
                else:
                    print("Invalid choice. Please enter a valid choice")
        elif choice == '2':
            return
        else:
            print("Invalid choice. Please enter a valid choice")

# Displays the free agents in the league
def display_free_agents(league):
    sort_and_display(league.free_agents)

# Displays all players in the league
def display_all_players(league):
    sort_and_display(league.all_players)

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
                    player.acquired_date = league.calendar.current_date
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
        print("4. End Free Agency")
        print("5. Exit Free Agency")
        choice = input("Enter your choice: ")
        if choice == '1':
            display_free_agents(league)
        elif choice == '2':
            sign_free_agent(league)
        elif choice == '3':
            league.cpu_free_agency_day()
            prev_label = league.calendar.get_season_label()
            league.calendar.advance_day()
            print(f"\n--- Day Advanced ---")
            if league.calendar.phase != "Free Agency":
                print(f"\nFree Agency has ended!")
                league.end_of_season(prev_label)
                return
        elif choice == '4':
            skip_free_agency(league)
        elif choice == '5':
            return
        else:
            print("Invalid choice. Please enter a valid choice")

# Handles the trade menu
def trade_menu(league):
    print("\nSelect a team to propose a trade with:")
    other_teams = [t for t in league.teams if t != league.user_team]
    other_teams.sort(key=lambda t: t.team_name)
    
    for i, team in enumerate(other_teams, start=1):
        print(f"{i}. {team.team_name} | Tier: {team.tier} | Record: {team.wins}-{team.losses}")
    
    choice = input("\nEnter a number, or 'x' to cancel: ")
    if choice.lower() == 'x':
        return
    
    try:
        index = int(choice) - 1
        team_b = other_teams[index]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return
    
    trade = Trade(league)
    trade.select_team(league.user_team, team_b)
    
    print(f"\nProposing a trade with {team_b.team_name}...")

    print(f"\nYour Roster ({league.user_team.team_name}):")
    print_player_table(league.user_team.roster)

    while True:
        player_choice = input("\nEnter a Player ID to offer, or 'done' when finished: ")
        if player_choice.lower() == 'done':
            break

        player = None
        for p in league.user_team.roster:
            if p.player_id == player_choice:
                player = p
                break

        if player is None:
            print("Invalid Player ID.")
            continue
    
        success, message = trade.add_offered_player(player)
        print(message)

    print(f"\n{team_b.team_name}'s Roster: ")
    print_player_table(team_b.roster)

    while True:
        player_choice = input("\nEnter a Player ID to request, or 'done' when finished: ")
        if player_choice.lower() == 'done':
            break

        player = None
        for p in team_b.roster:
            if p.player_id == player_choice:
                player = p
                break

        if player is None:
            print("Invalid Player ID.")
            continue
    
        success, message = trade.add_requested_player(player)
        print(message)

    print("\n--- Trade Summary ---")
    print(f"\nYou are offering:")
    if trade.assets_offered:
        print_player_table(trade.assets_offered)
    else:
        print("(nothing)")
    
    print(f"\nYou are requesting:")
    if trade.assets_requested:
        print_player_table(trade.assets_requested)
    else:
        print("(nothing)")
    
    offered_value = sum(calculate_trade_value(p) for p in trade.assets_offered)
    requested_value = sum(calculate_trade_value(p) for p in trade.assets_requested)
    print(f"\nTotal value offered: {offered_value:.1f}")
    print(f"Total value requested: {requested_value:.1f}")
    
    confirm = input("\nSubmit this trade proposal? (y/n): ")
    if confirm.lower() != 'y':
        print("Trade cancelled.")
        return
    
    success, message = trade.evaluate_trade()
    print(f"\n{message}")
    
    if success:
        trade.execute_trade()
        print("Trade completed!")

# Allows the user to skip the free agency period
def skip_free_agency(league):
    confirm = input("\nWould you like to actively manage free agency, or skip to the end? (manage/skip): ")
    if confirm.lower() == 'skip':
        confirm_skip = input("Are you sure? You won't be able to sign free agents this period. (y/n): ")
        if confirm_skip.lower() == 'y':
            while league.calendar.phase == "Free Agency":
                league.cpu_free_agency_day()
                prev_label = league.calendar.get_season_label()
                league.calendar.advance_day()
            print(f"\nFree Agency skipped! Phase advanced to: {league.calendar.phase}")
            league.end_of_season(prev_label)
            return

# Displays the championship history of the league
def display_champions(league):
    print("\nChampionship History")
    print("-" * 30)
    if not league.champions:
        print("No championships yet.")
    for champ in league.champions:
        print(champ)

# Displays how teams feel about where they currently stand(relevant to trading)
def display_tiers(league):
    print("\nTeam Tiers")
    print("-" * 50)
    for team in sorted(league.teams, key=lambda t: t.team_name):
        pct = team.wins / (team.wins + team.losses) if (team.wins + team.losses) > 0 else 0
        print(f"{team.team_name:<20} | {team.tier:<20} | OVR: {team.get_average_overall():.1f} | Record: {team.wins}-{team.losses} ({pct:.3f})")

# Handles the view menu
def view_menu(league):
    while True:
        print("\nView Menu:")
        print("1. My Team Roster")
        print("2. All Team Rosters")
        print("3. All Players in League")
        print("4. Free Agents")
        print("5. League Standings")
        print("6. Team Tiers")
        print("7. Championship History")
        print("8. Back to Main Menu")
        choice = input("Enter your choice: ")
        if choice == '1':
            league.get_team_roster(league.user_team.team_name)
        elif choice == '2':
            display_all_rosters(league)
        elif choice == '3':
            display_all_players(league)
        elif choice == '4':
            display_free_agents(league)
        elif choice == '5':
            league.display_standings()
        elif choice == '6':
            display_tiers(league)
        elif choice == '7':
            display_champions(league)
        elif choice == '8':
            return
        else:
            print("Invalid choice. Please enter a valid choice")

# Displays the main menu and handles user input for all game actions.
def main_menu(league):
    while True:
        league.calendar.display_date()
        print(f"\nMain Menu: | Phase: {league.calendar.phase}")
        print("1. View")
        print("2. Trades")
        print("3. Simulate Season")
        print("4. Advance Phase")
        print("5. Draft")
        print("6. Free Agency")
        print("7. Playoffs")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            view_menu(league)
        elif choice == '2':
                if not league.user_team.roster:
                    print("\nYou need a full roster before proposing trades.")
                else:
                    trade_menu(league)
        elif choice == '3':
            if league.calendar.phase != "Regular Season":
                print(f"\nSimulation is only available during the Regular Season.")
                print(f"Current phase: {league.calendar.phase}")
            else:
                confirm = input("\nAre you sure you want to simulate the season? (y/n): ")
                if confirm.lower() == 'y':
                    league.simulate_season()
                    league.display_standings()
                    print(f"\nSeason simulated! Current phase: {league.calendar.phase}")
        elif choice == '4':
            current = league.calendar.phase
            if current == "Regular Season":
                print("\nYou must simulate the season first!")
            elif current == "Trade Deadline":
                print(f"\nAdvancing through Trade Deadline...")
                while league.calendar.phase == "Trade Deadline":
                    league.calendar.advance_day()
                print(f"\nPhase advanced to: {league.calendar.phase}")
            elif current == "Draft":
                print("\nThe draft is open — use option 5 to run the draft!")
            elif current == "Free Agency":
                print("\nFree agency is open — use option 6 to manage free agency!")
            elif current == "Playoffs":
                print("\nPlayoffs are open — use option 7 to run the playoffs!")
            else:
                league.calendar.advance_day()
                print(f"\nAdvanced to: {league.calendar.phase}")
        elif choice == '5':
            if league.calendar.phase != "Draft":
                print(f"\nThe draft is not currently open.")
                print(f"Current phase: {league.calendar.phase}")
            else:
                league.run_draft()
                # advance calendar to free agency after draft
                while league.calendar.phase == "Draft":
                    league.calendar.advance_day()
                print(f"\nDraft complete! Phase advanced to: {league.calendar.phase}")
        elif choice == '6':
            if league.calendar.phase != "Free Agency":
                print(f"\nFree agency is not currently open.")
                print(f"Current phase: {league.calendar.phase}")
            else:
                free_agency_day(league)
        elif choice == '7':
            if league.calendar.phase != "Playoffs":
                print(f"\nPlayoffs are not currently open.")
                print(f"Current phase: {league.calendar.phase}")
            else:
                league.run_playoffs()
                while league.calendar.phase == "Playoffs":
                    league.calendar.advance_day()
                print(f"\nPlayoffs complete! Phase advanced to: {league.calendar.phase}")
        elif choice == '8':
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-8.")