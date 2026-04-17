import random

from RLplayer import Player
from RLdata import player_first, player_last, position, conferences
from RLteam import Team
from RLcalendar import Calendar

class League:
    def __init__(self):
        self.teams = []
        self.free_agents = []
        self.calendar = Calendar()
        self.all_players = []
        self.generate_teams()
        self.generate_players()
        self.distribute_players()
        self.user_team = None
        self.season = 1
    
    # Takes a list of team names and creates Team objects aswell as adding teams to their respective conferences
    def generate_teams(self):
        for conference, divisions in conferences.items():
            for division, teams in divisions.items():
                for team_name in teams:
                    team = Team(team_name, conference, division)
                    self.teams.append(team)
    
    # Creates a list of Player objects and adds them to the free agents pool and all players list
    def generate_players(self, num_players=400):
        for _ in range(num_players):
            player = Player(player_first, player_last, position)
            self.free_agents.append(player)
            self.all_players.append(player)

    # Distributes players to teams based on their contract value, with higher value players being distributed first to create a more balanced league. If a team cannot afford a player or has no roster spots, the player is returned to the free agents pool.
    def distribute_players(self):
        self.free_agents.sort(key=lambda p: p.salary, reverse=True)
        random.shuffle(self.teams)

        for i in range(12):
            for team in self.teams:
                if self.free_agents:
                    player = self.free_agents.pop(0)
                    if not team.add_player(player):
                        self.free_agents.append(player)

    # Display the roster of a team based on user input, allowing them to select a team by either name or ID. If the team is found, their roster is displayed along with payroll and cap space information. If not found, an error message is shown.
    def get_team_roster(self, team_name):
        for team in self.teams:
            if team.team_name == team_name or team.team_id == team_name:
                print(f"\n{team.team_id} | {team.team_name} | {team.conference} | {team.division} | Team OVR: {team.get_average_overall():.2f} | Payroll: ${team.payroll:,} | Cap Space: ${team.available_salary():,}")
                print("-" * 60)
                for player in team.roster:
                    print(f"{player.player_id} | {player.player_first} {player.player_last} | {player.position} | Age: {player.age} | OVR: {player.overall} | Pot: {player.get_potential_grade()} | Salary: ${player.salary:,} | Years: {player.contract_years}")
                return
        print(f"Team '{team_name}' not found.")
    
    # Simulates a game between two teams, with the outcome weighted by the average overall of each team.
    def simulate_game(self, team1, team2):
        team1_avg_ovr = team1.get_average_overall()
        team2_avg_ovr = team2.get_average_overall()
        team1_win_chance = team1_avg_ovr / (team1_avg_ovr + team2_avg_ovr)
        if random.random() < team1_win_chance:
            team1.wins += 1
            team2.losses += 1
        else:
            team2.wins += 1
            team1.losses += 1

    # Simulates a season with 4 divisional games, 3 conference games, and 2 non-conference games, with a total of 60 games for each team.
    def simulate_season(self):
        print(f"\nSimulating Season {self.season}...")
        played = set()

        for team in self.teams:
            division_rivals = [t for t in self.teams if t.division == team.division and t.team_id != team.team_id]

            for rival in division_rivals:
                matchup = frozenset([team.team_id, rival.team_id])
                if matchup not in played:
                    played.add(matchup)
                    for game in range(4):
                        self.simulate_game(team, rival)
            
            conference_rivals = [t for t in self.teams if t.conference == team.conference and t.division != team.division]

            for rival in conference_rivals:
                matchup = frozenset([team.team_id, rival.team_id])
                if matchup not in played:
                    played.add(matchup)
                    for game in range(3):
                        self.simulate_game(team, rival)
            
            non_conference_rivals = [t for t in self.teams if t.conference != team.conference]

            for rival in non_conference_rivals:
                matchup = frozenset([team.team_id, rival.team_id])
                if matchup not in played:
                    played.add(matchup)
                    for game in range(2):
                        self.simulate_game(team, rival)
            
        while self.calendar.phase == "Regular Season":
            self.calendar.advance_day()

    # Displays the standings for each conference and division.
    def display_standings(self):
        for conference in ["Eastern", "Western"]:
            print(f"\n{conference} Conference")
            print("=" * 50)
            
            for division in ["Atlantic", "Central", "Southeast"] if conference == "Eastern" else ["Northwest", "Pacific", "Southwest"]:
                print(f"\n  {division} Division")
                print("  " + "-" * 45)
                print(f"  {'Team':<20} {'W':<5} {'L':<5} {'PCT':<10}")
                
                division_teams = [t for t in self.teams if t.conference == conference and t.division == division]
                division_teams.sort(key=lambda t: t.wins / (t.wins + t.losses) if (t.wins + t.losses) > 0 else 0, reverse=True)
                
                for team in division_teams:
                    pct = team.wins / (team.wins + team.losses) if (team.wins + team.losses) > 0 else 0
                    print(f"  {team.team_name:<20} {team.wins:<5} {team.losses:<5} {pct:.3f}")

    # End of season actions, handles removing retiring players and players whose contracts have expired, as resetting team records.
    def end_of_season(self):
        self.calendar.display_date()
        print(f"\nSeason {self.season} has ended.")
        self.season += 1
        
        for team in self.teams:
            team.wins = 0
            team.losses = 0

        to_retire = []
        to_free_agency = []

        for player in self.all_players:
            player.develop()
            if player.age >= 40:
                to_retire.append(player)
            elif player.contract_years == 0:
                to_free_agency.append(player)

        for player in to_retire:
            self.all_players.remove(player)
            for team in self.teams:
                team.remove_player(player.player_id)
        
        for player in to_free_agency:
            self.free_agents.append(player)
            for team in self.teams:
                team.remove_player(player.player_id)
        
            