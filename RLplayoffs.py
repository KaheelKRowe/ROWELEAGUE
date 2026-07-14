import random

class Playoffs:
    def __init__(self, league):
        self.league = league
        self.eastern_seeds = []
        self.western_seeds = []
        self.bracket = {}
        self.champion = None

    
    def determine_seeds(self):
        for conference in ["Eastern", "Western"]:
            conference_teams = [t for t in self.league.teams if t.conference == conference]

            division_winners = set()
            for division in ["Atlantic", "Central", "Southeast"] if conference == "Eastern" else ["Northwest", "Pacific", "Southwest"]:
                division_teams = [t for t in conference_teams if t.division == division]
                winner = max(division_teams, key=lambda t: t.wins / (t.wins + t.losses) if (t.wins + t.losses) > 0 else 0)
                division_winners.add(winner.team_id)

            conference_teams.sort(key=lambda t: (
                t.wins / (t.wins + t.losses) if (t.wins + t.losses) > 0 else 0,
                t.team_id in division_winners
            ), reverse=True)

            top_seven = conference_teams[:7]

            if conference == "Eastern":
                self.eastern_seeds = top_seven
            else:
                self.western_seeds = top_seven
    
    def display_seeds(self):
        for conference in ["Eastern", "Western"]:
            print(f"\n{conference} Conference")
            print("=" * 50)

            seeds = self.eastern_seeds if conference == "Eastern" else self.western_seeds
            for i, team in enumerate(seeds, start=1):
                pct = team.wins / (team.wins + team.losses) if (team.wins + team.losses) > 0 else 0
                print(f" #{i} {team.team_name:<20} {team.wins:<5} {team.losses:<5} {pct:.3f}")
    
    def create_bracket(self):
        self.bracket = {}

        for conference, seeds in [("Eastern", self.eastern_seeds), ("Western", self.western_seeds)]:
            
            # 1 Seed from each conference gets a bye round
            bye_team = seeds[0]

            round_1 = [
                (seeds[1], seeds[6]), # 2 vs 7
                (seeds[2], seeds[5]), # 3 vs 6
                (seeds[3], seeds[4])  # 4 vs 5
            ]

            self.bracket[conference] = {
                "bye": bye_team,
                "round_1": round_1,
                "round_1_winners": [],
                "round_2": [],
                "conference_final": [],
                "Conference_champion": None
            }

            for matchup in round_1:
                winner = self.simulate_series(matchup[0], matchup[1])
                self.bracket[conference]["round_1_winners"].append(winner)

            winners = self.bracket[conference]["round_1_winners"]
            # winners[0] = winner of 2v7
            # winners[1] = winner of 3v6
            # winners[2] = winner of 4v5

            round_2 = [
                (bye_team, winners[2]),
                (winners[0], winners[1])
            ]

            self.bracket[conference]["round_2"] = round_2

            round_2_winners = []
            for matchup in round_2:
                winner = self.simulate_series(matchup[0], matchup[1])
                round_2_winners.append(winner)

            self.bracket[conference]["conference_final"] = round_2_winners

            conf_champion = self.simulate_series(round_2_winners[0], round_2_winners[1])
            self.bracket[conference]["Conference_champion"] = conf_champion

        east_champion = self.bracket["Eastern"]["Conference_champion"]
        west_champion = self.bracket["Western"]["Conference_champion"]

        print(f"\n=== CHAMPIONSHIP ===")
        season_label = self.league.calendar.get_season_label()
        champion = self.simulate_series(east_champion, west_champion)
        self.champion = champion
        self.league.champions.append(f"{champion.team_name} ({season_label})")

        print(f"\n The {champion.team_name} Are The Champions of the {season_label} Season!")



    def simulate_series(self, team1, team2):
        team1_wins = 0
        team2_wins = 0
        game_num = 1

        print(f"\n{team1.team_name} vs {team2.team_name}")

        while team1_wins < 4 and team2_wins < 4:
            team1_avg_ovr = team1.get_average_overall()
            team2_avg_ovr = team2.get_average_overall()
            team1_win_chance = team1_avg_ovr / (team1_avg_ovr + team2_avg_ovr)

            if random.random() < team1_win_chance:
                team1_wins += 1
                print(f"Game {game_num}: {team1.team_name} wins | Series: {team1_wins}-{team2_wins}")
            else:
                team2_wins += 1
                print(f"Game {game_num}: {team2.team_name} wins | Series: {team1_wins}-{team2_wins}")

            game_num += 1
        
        winner = team1 if team1_wins == 4 else team2
        print(f"\n{winner.team_name} wins the series {max(team1_wins, team2_wins)}-{min(team1_wins, team2_wins)}!")
        return winner

        

