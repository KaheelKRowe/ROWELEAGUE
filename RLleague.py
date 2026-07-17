import random

from RLplayer import Player
from RLdata import player_first, player_last, position, conferences, ROSTER_BLUEPRINTS, ELITE_THRESHOLD, STARTER_THRESHOLD
from RLteam import Team
from RLcalendar import Calendar
from RLdraft import Draft
from RLplayoffs import Playoffs
from RLtrades import assign_all_tiers

class League:
    def __init__(self):
        self.teams = []
        self.free_agents = []
        self.calendar = Calendar()
        self.all_players = []
        self.generate_teams()
        self.distribute_players()
        self.generate_free_agents()
        for team in self.teams:
            team.assign_minutes()
        assign_all_tiers(self, "preseason")
        self.user_team = None
        self.season = 1
        self.champions = []
    
    # Takes a list of team names and creates Team objects aswell as adding teams to their respective conferences
    def generate_teams(self):
        for conference, divisions in conferences.items():
            for division, teams in divisions.items():
                for team_name in teams:
                    team = Team(team_name, conference, division)
                    self.teams.append(team)
    
    # Creates a list of Player objects and adds them to the free agents pool and all players list
    def generate_free_agents(self, num_players=122):
        for _ in range(num_players):
            target_overall = random.randint(50, 75)
            
            # higher overall correlates with older age
            if target_overall >= 72:
                age = random.randint(29, 35)
            elif target_overall >= 63:
                age = random.randint(24, 30)
            else:
                age = random.randint(20, 26)
            
            player = Player(player_first, player_last, position, target_overall=target_overall, age=age)
            
            self.free_agents.append(player)
            self.all_players.append(player)
    
    def get_age_for_tier(self, tier):
        if tier == "elite":
            return random.randint(26, 32)  # prime years, matches your develop() prime window
        elif tier == "starter":
            return random.randint(22, 33)
        else:  # role
            return random.randint(19, 35)  # widest range — could be a raw prospect or a vet

    def build_roster_from_blueprint(self, blueprint, player_first, player_last):
        all_positions = ['PG', 'SG', 'SF', 'PF', 'C']
        
        elite_slots = [slot for slot in blueprint if slot[0] == "elite"]
        starter_slots = [slot for slot in blueprint if slot[0] == "starter"]
        role_slots = [slot for slot in blueprint if slot[0] == "role"]
        
        roster = []
        position_counts = {pos: 0 for pos in all_positions}
        MAX_TOP_TIER_PER_POSITION = 2  # combined elite + starter cap per position
        
        # Elite slots — guaranteed unique positions (never repeats within elite itself)
        available_positions = all_positions.copy()
        random.shuffle(available_positions)
        for i, (tier, low, high) in enumerate(elite_slots):
            pos = available_positions[i]
            target_overall = random.randint(low, high)
            age = self.get_age_for_tier(tier)
            player = Player(player_first, player_last, [pos], target_overall=target_overall, age=age)
            roster.append(player)
            position_counts[pos] += 1
        
        # Starter slots — respect the combined top-tier cap, spread as evenly as possible
        for (tier, low, high) in starter_slots:
            eligible = [pos for pos in all_positions if position_counts[pos] < MAX_TOP_TIER_PER_POSITION]
            if not eligible:
                eligible = all_positions  # fallback if somehow everything's capped
            min_count = min(position_counts[pos] for pos in eligible)
            candidates = [pos for pos in eligible if position_counts[pos] == min_count]
            pos = random.choice(candidates)
            
            target_overall = random.randint(low, high)
            age = self.get_age_for_tier(tier)
            player = Player(player_first, player_last, [pos], target_overall=target_overall, age=age)
            roster.append(player)
            position_counts[pos] += 1
        
        # Role slots — freely shuffled, no cap needed (depth is fine here)
        role_positions = (all_positions * ((len(role_slots) // len(all_positions)) + 1))[:len(role_slots)]
        random.shuffle(role_positions)
        for (tier, low, high), pos in zip(role_slots, role_positions):
            target_overall = random.randint(low, high)
            age = self.get_age_for_tier(tier)
            player = Player(player_first, player_last, [pos], target_overall=target_overall, age=age)
            roster.append(player)
        
        return roster
    
    # Distributes players to teams based on their contract value, with higher value players being distributed first to create a more balanced league. If a team cannot afford a player or has no roster spots, the player is returned to the free agents pool.
    def distribute_players(self):
        blueprint_list = (
            ["Rebuilding"] * 10 +
            ["Retooling"] * 4 +
            ["Playoff Team"] * 4 +
            ["Contender"] * 4 +
            ["Champion Favorite"] * 2
        )
        random.shuffle(blueprint_list)
        random.shuffle(self.teams)
        
        for team, tier_name in zip(self.teams, blueprint_list):
            blueprint = ROSTER_BLUEPRINTS[tier_name]
            roster_players = self.build_roster_from_blueprint(blueprint, player_first, player_last)
            for player in roster_players:
                team.add_player(player)
                self.all_players.append(player)
        
        # Safety net — guarantee every team reaches 12 players
        for team in self.teams:
            while len(team.roster) < 12:
                position_counts = {pos: sum(1 for p in team.roster if p.position == pos) for pos in ['PG', 'SG', 'SF', 'PF', 'C']}
                min_count = min(position_counts.values())
                eligible_positions = [pos for pos, count in position_counts.items() if count == min_count]
                chosen_position = random.choice(eligible_positions)
                
                target_overall = random.randint(45, 55)
                age = random.randint(20, 34)
                filler = Player(player_first, player_last, [chosen_position], target_overall=target_overall, age=age)
                if team.add_player(filler):
                    self.all_players.append(filler)
                else:
                    break

    # Display the roster of a team based on user input, allowing them to select a team by either name or ID. If the team is found, their roster is displayed along with payroll and cap space information. If not found, an error message is shown.
    def get_team_roster(self, team_name):
        for team in self.teams:
            if team.team_name == team_name or team.team_id == team_name:
                print(f"\n{team.team_id} | {team.team_name} | {team.conference} | {team.division} | Team OVR: {team.get_average_overall():.2f} | Payroll: ${team.payroll:,} | Cap Space: ${team.available_salary():,}")
                print("-" * 60)
                for player in team.roster:
                    print(f"{player.player_id} | {player.player_first} {player.player_last} | {player.position} | Age: {player.age} | OVR: {player.overall} | Pot: {player.get_potential_grade()} | Salary: ${player.salary:,} | Years: {player.contract_years} | MIN: {player.minutes}")
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
        print(f"\nSimulating Season {self.calendar.get_season_label()}...")
        played = set()

        for team in self.teams:
            team.assign_minutes()
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

        if self.calendar.phase == "Trade Deadline":
            assign_all_tiers(self, "deadline")

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
    def end_of_season(self, season_label=None):
        if season_label is None:
            season_label = self.calendar.get_season_label()
        self.calendar.display_date()
        print(f"\nSeason {season_label} has ended.")

        self.season += 1
        
        for team in self.teams:
            team.wins = 0
            team.losses = 0
            team.dead_cap = 0

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

    # Handles the logic for the cpu free agency signing, including the positonal need based signing, and upgrading.    
    def cpu_free_agency_day(self):
        for team in self.teams:
            if team != self.user_team:
                needs = team.get_positional_needs()
                    
                if needs:
                    # need based signing
                    for pos in needs:
                        best = None
                        for player in self.free_agents:
                            if player.position == pos and player.salary <= team.available_salary():
                                if best is None or player.overall > best.overall:
                                    best = player
                        if best:
                            team.add_player(best)
                            self.free_agents.remove(best)
                            best.acquired_date = self.calendar.current_date
                            print(f"{team.team_name} signed {best.player_first} {best.player_last} | {best.position} | OVR: {best.overall}")
                else:
                    # upgrade check
                    for pos in ['PG', 'SG', 'SF', 'PF', 'C']:
                        roster_at_pos = [p for p in team.roster if p.position == pos]
                        if not roster_at_pos:
                            continue
                        weakest = min(roster_at_pos, key=lambda p: p.overall)
                        best = None
                        for player in self.free_agents:
                            if player.position == pos and player.salary <= team.available_salary():
                                if player.overall > weakest.overall + 3:
                                    if best is None or player.overall > best.overall:
                                        best = player
                        if best:
                            team.remove_player(weakest.player_id)
                            self.free_agents.append(weakest)
                            team.add_player(best)
                            self.free_agents.remove(best)
                            best.acquired_date = self.calendar.current_date
                            self.refresh_minutes(team)
                            print(f"{team.team_name} signed {best.player_first} {best.player_last} and released {weakest.player_first} {weakest.player_last}")
    
    # Runs the draft for the league
    def run_draft(self):
        draft = Draft(self)
        draft.conduct_draft()
    
    # Runs the playoffs for the league
    def run_playoffs(self):
        playoffs = Playoffs(self)
        playoffs.determine_seeds()
        playoffs.display_seeds()
        playoffs.create_bracket()

    def refresh_minutes(self, *teams):
            for team in teams:
                team.assign_minutes()
        
            