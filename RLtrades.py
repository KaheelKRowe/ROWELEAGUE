from RLplayer import Player

class Trade:
    TIER_MULTIPLIERS = {
        "Rebuilding": 0.9,
        "Retooling": 1.0,
        "Playoff Team": 1.1,
        "Contender": 1.25,
        "Champion Favorite": 1.4
    }
    def __init__(self, league):
        self.league = league
        self.team_a = None
        self.team_b = None
        self.assets_offered = []
        self.assets_requested = []
    
    # Allows user to select which team they would like to trade with
    def select_team(self, team_a, team_b):
        self.team_a = team_a
        self.team_b = team_b

    # Checks if user's player is eligible to be offered
    def add_offered_player(self, player):
        if player not in self.team_a.roster:
            return False, "Player is not on your roster"
        if not is_tradeable(player, self.league.calendar.current_date):
            return False, "Player is not eligible to be traded right now."
        if player in self.assets_offered:
            return False, "Player is already in the trade."
        self.assets_offered.append(player)
        return True, f"{player.player_first} {player.player_last} added to offer."
    
    # Checks if user's player is eligible to be requested
    def add_requested_player(self, player):
        if player not in self.team_b.roster:
            return False, "Player is not on their roster"
        if not is_tradeable(player, self.league.calendar.current_date):
            return False, "Player is not eligible to be traded right now."
        if player in self.assets_requested:
            return False, "Player is already in the trade."
        self.assets_requested.append(player)
        return True, f"{player.player_first} {player.player_last} added to request."
    
    # Checks if the trade is valid and meets all requirements
    def evaluate_trade(self):
        offered_value = sum(calculate_trade_value(p) for p in self.assets_offered)
        requested_value = sum(calculate_trade_value(p) for p in self.assets_requested)

        # Checks if offer meets CPU team's value requirements
        multiplier = self.TIER_MULTIPLIERS.get(self.team_b.tier, 1.0)
        required_value = requested_value * multiplier

        if offered_value < required_value:
            return False, f"{self.team_b.team_name} is not willing to accept this trade."
        
        # Checks if the trade meets the salary requirements
        offered_salary_total = sum(p.salary for p in self.assets_offered)
        requested_salary_total = sum(p.salary for p in self.assets_requested)

        team_b_new_payroll = self.team_b.payroll - requested_salary_total + offered_salary_total
        if team_b_new_payroll > self.team_b.salary_cap:
            return False, f"{self.team_b.team_name} does not have the salary cap to accept this trade."
        
        team_a_new_payroll = self.team_a.payroll - offered_salary_total + requested_salary_total
        if team_a_new_payroll > self.team_a.salary_cap:
            return False, f"{self.team_a.team_name} you do not have the salary cap to accept this trade."
        
        # Checks if the trade would exceed the roster limit
        team_a_new_size = len(self.team_a.roster) - len(self.assets_offered) + len(self.assets_requested)
        team_b_new_size = len(self.team_b.roster) - len(self.assets_requested) + len(self.assets_offered)
        
        if team_a_new_size > 15:
            return False, f"{self.team_a.team_name} would exceed the roster limit."
        if team_b_new_size > 15:
            return False, f"{self.team_b.team_name} would exceed the roster limit."
        
        return True, f"{self.team_b.team_name} has accepted the trade."
    
    # Executes the trade once the evaluation is valid
    def execute_trade(self):
        current_date = self.league.calendar.current_date

        for player in self.assets_offered:
            self.team_a.roster.remove(player)
            self.team_a.payroll -= player.salary
            self.team_b.roster.append(player)
            self.team_b.payroll += player.salary
            player.last_traded_date = current_date

        for player in self.assets_requested:
            self.team_b.roster.remove(player)
            self.team_b.payroll -= player.salary
            self.team_a.roster.append(player)
            self.team_a.payroll += player.salary
            player.last_traded_date = current_date
        
        self.assets_offered.clear()
        self.assets_requested.clear()

# Assigns expected salary based on contract value
def get_expected_salary(contract_value):
    if contract_value >= 90:
        return 35_000_000
    elif contract_value >= 80:
        return 17_500_000
    elif contract_value >= 70:
        return 7_500_000
    elif contract_value >= 60:
        return 3_000_000
    else:
        return 750_000

# Calculates trade value based on overall, potential for young players, age, and salary
def calculate_trade_value(player):
    value = player.overall

    if player.age <= 25:
        value += player.potential * 0.4
    elif player.age <= 32:
        value += 10
    else:
        years_past_prime = player.age - 32
        value -= (years_past_prime ** 2) * 1

    expected = get_expected_salary(player.contract_value)
    if player.salary < expected:
        value += 10
    elif player.salary > expected:
        value -= 10

    if player.contract_years >= 4 and player.salary < expected:
        value += 10
    elif player.contract_years >= 4 and player.salary > expected:
        value -= 10

    return value

# Calculates the preseason score for a team
def calculate_preseason_score(team):
    avg_ovr = team.get_average_overall()
    normalized_ovr = (avg_ovr - 50) / 40
    return normalized_ovr

# Calculates the deadline score for a team
def calculate_deadline_score(team):
    win_pct = team.wins / (team.wins + team.losses) if (team.wins + team.losses > 0) else 0.5
    avg_ovr = team.get_average_overall()
    normalized_ovr = (avg_ovr - 50) / 40
    score = (win_pct * 0.6) + (normalized_ovr * 0.4)
    return score

# Determines the tier of a team
def get_team_tier(team, phase="deadline"):
    if phase == "preseason":
        score = calculate_preseason_score(team)
    else:
        score = calculate_deadline_score(team)

    if score >= 0.8:
        return "Champion Favorite"
    elif score >= 0.6:
        return "Contender"
    elif score >= 0.45:
        return "Playoff Team"
    elif score >= 0.3:
        return "Retooling"
    else:
        return "Rebuilding"

# Assigns tiers to all teams
def assign_all_tiers(league, phase="deadline"):
    for team in league.teams:
        team.tier = get_team_tier(team, phase)

# Checks if a player is tradeable
def is_tradeable(player, current_date):
    from RLplayer import Rookie

    # Recently Traded players cannot be traded for 45 days
    if player.last_traded_date:
        days_since_trade = (current_date - player.last_traded_date).days
        if days_since_trade < 45:
            return False
    
    # Newly signed players cant be traded for 60 days unless its a rookie being traded on draft day
    if player.acquired_date:
        days_since_acquired = (current_date - player.acquired_date).days

        if isinstance(player, Rookie) and days_since_acquired == 0:
            return True

        if days_since_acquired < 60:
            return False
    
    return True