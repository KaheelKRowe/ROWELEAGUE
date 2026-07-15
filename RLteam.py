from RLplayer import Player

class Team:
    id_counter = 0
    def __init__(self, team_name, conference, division):
        Team.id_counter += 1
        self.team_id = f"T{Team.id_counter:03d}"
        self.team_name = team_name
        self.conference = conference
        self.division = division
        self.roster = []
        self.salary_cap = 140_000_000
        self.payroll = 0
        self.dead_cap = 0
        self.wins = 0
        self.losses = 0
        self.tier = None
    
    # add player to team if roster spots and salary cap allow
    def add_player(self, player):
        if len(self.roster) < 15 and self.payroll + player.salary <= self.salary_cap:
            self.roster.append(player)
            self.payroll += player.salary
            return True
        return False
    
    # remove player from team and adjust payroll and dead cap
    def remove_player(self, player_id):
        for player in self.roster:
            if player.player_id == player_id:
                self.roster.remove(player)
                self.payroll -= player.salary
                self.dead_cap += player.salary
                return True
        return False
    
    # calculate available salary
    def available_salary(self):
        return self.salary_cap - self.payroll - self.dead_cap
    
    # calculate average team overall
    def get_average_overall(self):
        if not self.roster:
            return 0
        total_overall = sum(player.overall for player in self.roster)
        return total_overall / len(self.roster)
    
    # Determines the positional needs for a team
    def get_positional_needs(self):
        needs = []
        for pos in ['PG', 'SG', 'SF', 'PF', 'C']:
            count = sum(1 for p in self.roster if p.position == pos)
            if count < 2:
                needs.append(pos)
        return needs
