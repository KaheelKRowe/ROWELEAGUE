import random

from RLplayer import Rookie
from RLdata import player_first, player_last, position
from RLui import print_player_table

class Draft:
    def __init__(self, league):
        self.league = league
        self.rookie_pool = []
        self.draft_order = []
        self.generate_rookies()
        self.current_pick = 1
        self.total_picks = 48

    def generate_rookies(self, num_rookies=75):
        for _ in range(num_rookies):
            rookie = Rookie(player_first, player_last, position)
            self.rookie_pool.append(rookie)
            self.league.all_players.append(rookie)
            self.rookie_pool.sort(key=lambda p: p.overall, reverse=True)
    
    def determine_draft_order(self):
        # sort teams by win percentage ascending (worst first)
        sorted_teams = sorted(self.league.teams,
                            key=lambda t: t.wins / (t.wins + t.losses)
                            if (t.wins + t.losses) > 0 else 0)
        
        # assign weights — worst team gets highest weight
        weights = [len(sorted_teams) - i for i in range(len(sorted_teams))]
        
        # lottery for first pick
        remaining_teams = sorted_teams.copy()
        remaining_weights = weights.copy()
        
        # lottery determines top 4 picks
        for i in range(4):
            pick = random.choices(remaining_teams, weights=remaining_weights, k=1)[0]
            self.draft_order.append(pick)
            idx = remaining_teams.index(pick)
            remaining_teams.pop(idx)
            remaining_weights.pop(idx)
        
        # remaining picks follow worst to best record
        self.draft_order.extend(remaining_teams)
        
        # second round follows same order
        self.draft_order.extend(self.draft_order[:24].copy())
        print(f"DEBUG: Draft order length: {len(self.draft_order)}")

    def get_rookie_salary(self):
        if self.current_pick <= 2:
            return 10_000_000
        elif self.current_pick <= 5:
            return random.randint(8_000_000, 9_000_000)
        elif self.current_pick <= 12:
            return random.randint(6_000_000, 8_000_000)
        elif self.current_pick <= 24:
            return random.randint(4_000_000, 6_000_000)
        elif self.current_pick <= 36:
            return random.randint(2_000_000, 4_000_000)
        else:
            return random.randint(1_000_000, 2_000_000)

    def cpu_pick(self, team):
        needs = team.get_positional_needs()
        best = None

        if needs:
            for pos in needs:
                for player in self.rookie_pool:
                    if player.position == pos:
                        if best is None or player.overall > best.overall:
                            best = player
                if best:
                    break  # only look for one position of need
        else:
            # upgrade check
            for player in self.rookie_pool:
                roster_at_pos = [p for p in team.roster if p.position == player.position]
                if roster_at_pos:
                    weakest = min(roster_at_pos, key=lambda p: p.overall)
                    if player.overall > weakest.overall + 3:
                        if best is None or player.overall > best.overall:
                            best = player
                else:
                    if best is None or player.overall > best.overall:
                        best = player

        if best:
            best.salary = self.get_rookie_salary()
            # handle full roster
            if len(team.roster) >= 15:
                weakest = min(team.roster, key=lambda p: p.overall)
                team.remove_player(weakest.player_id)
                self.league.free_agents.append(weakest)
            if team.add_player(best):
                self.rookie_pool.remove(best)
                best.drafted_by = team.team_name
                print(f"Pick {self.current_pick}: {team.team_name} selects {best.player_first} {best.player_last} | {best.position} | OVR: {best.overall} | Signed")
            else:
                self.rookie_pool.remove(best)
                self.league.free_agents.append(best)
                print(f"Pick {self.current_pick}: {team.team_name} selects {best.player_first} {best.player_last} | {best.position} | OVR: {best.overall} | Released")
            self.current_pick += 1
    
    def display_rookies(self):
        self.rookie_pool.sort(key=lambda p: p.overall, reverse=True)
        print_player_table(self.rookie_pool)
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
                        self.rookie_pool.sort(key=lambda p: p.overall, reverse=True)
                        print_player_table(self.rookie_pool)
                    elif choice_2 == '2':
                        print("1. PG | 2. SG | 3. SF | 4. PF | 5. C")
                        choice_3 = input("Enter position choice: ")
                        if choice_3 == '1':
                            self.rookie_pool.sort(key=lambda p: p.overall, reverse=True)
                            filtered = [p for p in self.rookie_pool if p.position == 'PG']
                            print_player_table(filtered)
                        elif choice_3 == '2':
                            self.rookie_pool.sort(key=lambda p: p.overall, reverse=True)
                            filtered = [p for p in self.rookie_pool if p.position == 'SG']
                            print_player_table(filtered)
                        elif choice_3 == '3':
                            self.rookie_pool.sort(key=lambda p: p.overall, reverse=True)
                            filtered = [p for p in self.rookie_pool if p.position == 'SF']
                            print_player_table(filtered)
                        elif choice_3 == '4':
                            self.rookie_pool.sort(key=lambda p: p.overall, reverse=True)
                            filtered = [p for p in self.rookie_pool if p.position == 'PF']
                            print_player_table(filtered)
                        elif choice_3 == '5':
                            self.rookie_pool.sort(key=lambda p: p.overall, reverse=True)
                            filtered = [p for p in self.rookie_pool if p.position == 'C']
                            print_player_table(filtered)
                        else:
                            print("Invalid position choice. Please try again.")
                    elif choice_2 == '3':
                        self.rookie_pool.sort(key=lambda p: p.salary, reverse=True)
                        print_player_table(self.rookie_pool)
                    elif choice_2 == '4':
                        self.rookie_pool.sort(key=lambda p: p.age)
                        print_player_table(self.rookie_pool)
                    elif choice_2 == '5':
                        self.rookie_pool.sort(key=lambda p: p.potential, reverse=True)
                        print_player_table(self.rookie_pool)
                    elif choice_2 == '6':
                        return
                    else:
                        print("Invalid choice. Please enter a valid choice")
            elif choice == '2':
                return
            else:
                print("Invalid choice. Please enter a valid choice")
    
    def user_pick(self):
        picked = False
        while not picked:
            print(f"\nPick {self.current_pick} | {self.league.user_team.team_name}")
            print("| 1. View Rookies | 2. Make Selection | 3. Pass (send to free agency)")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.display_rookies()
            elif choice == '2':
                while True:
                    rookie_choice = input("\nEnter a Player ID: ")
                    found = False
                    for player in self.rookie_pool:
                        if player.player_id == rookie_choice:
                            found = True
                            print(f"\nSelected {player.player_first} {player.player_last} | {player.position} | OVR: {player.overall} | Age: {player.age} | Salary: ${player.salary:,}")
                            confirm = input("Sign this player? (y/n): ")
                            if confirm.lower() == 'y':
                                player.salary = self.get_rookie_salary()
                                if self.league.user_team.add_player(player):
                                    self.rookie_pool.remove(player)
                                    player.drafted_by = self.league.user_team.team_name
                                    self.current_pick += 1
                                    picked = True
                                    print(f"\nSigned! {player.player_first} {player.player_last} | {player.position} | OVR: {player.overall} | Age: {player.age} | Salary: ${player.salary:,}")
                                else:
                                    # handle full roster
                                    pass
                            else:
                                self.league.free_agents.append(player)
                                self.rookie_pool.remove(player)
                                player.drafted_by = self.league.user_team.team_name
                                self.current_pick += 1
                                picked = True
                            break
                    if not found:
                        print("Invalid Player ID.")
                    if picked:
                        break
            elif choice == '3':
                print(f"\nPick {self.current_pick} passed to free agency.")
                self.current_pick += 1
                picked = True  # user passes their pick

    def conduct_draft(self):
        self.determine_draft_order()
        user_picks = [i+1 for i, t in enumerate(self.draft_order) if t == self.league.user_team]
        print(f"\nSeason {self.league.season} Draft")
        print(f"Your pick positions: {user_picks}")
        
        draft_results = {team.team_name: [] for team in self.league.teams}
        
        for _ in range(self.total_picks):
            print(f"DEBUG: Processing pick {self.current_pick}")
            team = self.draft_order[self.current_pick - 1]
            if team == self.league.user_team:
                self.user_pick()
            else:
                self.cpu_pick(team)

        for rookie in self.rookie_pool:
            self.league.free_agents.append(rookie)
        self.rookie_pool.clear()
        print(f"\nDraft complete! {len(self.league.free_agents)} players available in free agency.")

        print("\nDraft Results")
        for team in self.league.teams:
            rookies = [p for p in self.league.all_players if hasattr(p, 'drafted_by') and p.drafted_by == team.team_name]
            if rookies:
                print(f"\n{team.team_name}")
                for r in rookies:
                    print(f"{r.player_first} {r.player_last} | {r.position} | OVR: {r.overall} | Age: {r.age} | Salary: ${r.salary:,}")


