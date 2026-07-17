import random
from RLdata import player_first, player_last, position


class Player:
    id_counter = 0
    
    POSITION_WEIGHTS = {
        'PG': {'Shooting': 0.3, 'Defense': 0.2, 'Passing': 0.3, 'Rebounding': 0.1, 'Athleticism': 0.1},
        'SG': {'Shooting': 0.35, 'Defense': 0.2, 'Passing': 0.15, 'Rebounding': 0.1, 'Athleticism': 0.2},
        'SF': {'Shooting': 0.25, 'Defense': 0.25, 'Passing': 0.2, 'Rebounding': 0.15, 'Athleticism': 0.15},
        'PF': {'Shooting': 0.2, 'Defense': 0.3, 'Passing': 0.2, 'Rebounding': 0.2, 'Athleticism': 0.1},
        'C': {'Shooting': 0.1, 'Defense': 0.4, 'Passing': 0.1, 'Rebounding': 0.3, 'Athleticism': 0.1}
    }
    def __init__(self, player_first, player_last, position, target_overall=None, age=None):
        Player.id_counter += 1
        self.player_id = f"P{Player.id_counter:03d}"
        self.player_first = random.choice(player_first)
        self.player_last = random.choice(player_last)
        self.position = random.choice(position)
        self.age = age if age is not None else random.randint(19, 35)
        self.target_overall = target_overall if target_overall is not None else self.generate_target_overall()
        self.ratings = self.generate_ratings_for_overall(self.target_overall)
        self.potential = self.calculate_potential()
        self.overall = self.calculate_overall()
        self.contract_value = self.generate_value()
        self.salary = self.generate_contract()
        self.contract_years = self.generate_contract_years()
        self.acquired_date = None
        self.last_traded_date = None
        self.minutes = 0


    # Potential is based on age, with younger players having a chance at higher potential
    def calculate_potential(self):
        if self.age <= 22:
            return random.randint(65, 99)
        elif self.age <= 29:
            return random.randint(60, 85)
        else: # 30+
            return random.randint(40, 70)

    # Once game is started will generate a target overall so league talent is spread realisticly
    def generate_target_overall(self):
        if self.age < 25:
            overall_tiers = [
                (70, 75),
                (60, 69),
                (50, 59)
            ]
            weights = [65, 30, 5]
        elif self.age <= 32:   
            overall_tiers = [
                (90, 99),   # Superstar
                (80, 89),   # All-Star
                (70, 79),   # Role Player
                (60, 69),   # Bench
                (50, 59),   # Reserves
            ]
            weights = [7, 12, 65, 10, 6]
        else:
            overall_tiers = [
                (80, 85),
                (70, 79),
                (60, 69),
                (50, 59)
            ]
            weights = [8, 75, 10, 7]

        tier = random.choices(overall_tiers, weights=weights, k=1)[0]
        return random.randint(tier[0], tier[1])

    # ratings are generated based on position
    def generate_ratings_for_overall(self, target_overall):
        variance = 8
        weights = Player.POSITION_WEIGHTS[self.position]
        ratings = {}
        for stat, weight in weights.items():
            bias = (weight - 0.2) * 40
            value = target_overall + bias + random.randint(-variance, variance)
            ratings[stat] = max(30, min(99, value))
        return ratings
    
    # overall is calculated based on ratings, with different weights for each position to reflect their unique skill sets
    def calculate_overall(self):
        weights = Player.POSITION_WEIGHTS[self.position]
        overall = sum(self.ratings[stat] * weight for stat, weight in weights.items())
        return int(overall)
    
    # give players a potential grade based on their current potential rating
    def get_potential_grade(self):
        if self.potential >= 90:
            return 'S'
        elif self.potential >= 80:
            return 'A'
        elif self.potential >= 70:
            return 'B'
        elif self.potential >= 60:
            return 'C'
        else:
            return 'D'

    # generate contract value based on overall and potential   
    def generate_value(self):
        return int((self.overall * 0.65) + (self.potential * 0.35))

    # generate contract    
    def generate_contract(self):
        if self.contract_value >= 90:
            return random.randint(30_000_000, 40_000_000)
        elif self.contract_value >= 80:
            return random.randint(10_000_000, 25_000_000)
        elif self.contract_value >= 70:
            return random.randint(5_000_000, 10_000_000)
        elif self.contract_value >= 60:
            return random.randint(1_000_000, 5_000_000)
        else:
            return random.randint(500_000, 1_000_000)
        
    # generate contract years
    def generate_contract_years(self):
        if self.contract_value >= 90:
            return random.randint(4, 5)
        elif self.contract_value >= 80:
            return random.randint(3, 5)
        elif self.contract_value >= 70:
            return random.randint(2, 4)
        elif self.contract_value >= 60:
            return random.randint(1, 3)
        else:
            return random.randint(1, 2)

    # handles player progression and regression based on age, with younger players being able to improve more based on potential, while older players regress more as they age    
    def develop(self):
        self.age += 1
        self.contract_years -= 1
        if self.age <= 25:
            if self.potential >= 90:
                self.overall += random.randint(4, 7)
            elif self.potential >= 80:
                self.overall += random.randint(2, 5)
            elif self.potential >= 70:
                self.overall += random.randint(1, 3)
            elif self.potential >= 60:
                self.overall += random.randint(0, 2)
            else:
                self.overall += random.randint(0, 1)
        elif self.age <= 34:
            coinflip = random.randint(1, 2)
            if coinflip == 1:
                self.overall += random.randint(0, 1)
            else:
                self.overall -= random.randint(0, 1)
        else: # 35+
            if self.age == 35:
                self.overall -= random.randint(0, 1)
            elif self.age == 36:
                self.overall -= random.randint(1, 3)
            elif self.age == 37:
                self.overall -= random.randint(2, 5)
            elif self.age == 38:
                self.overall -= random.randint(3, 7)
            elif self.age == 39:
                self.overall -= random.randint(4, 8)
            elif self.age >= 40:
                self.overall -= random.randint(5, 10)
                # Players that are 40 must retire once that season ends.
        self.contract_value = self.generate_value()

# Rookie class
class Rookie(Player):
    def __init__(self, player_first, player_last, position):
        super().__init__(player_first, player_last, position)
        self.age = random.randint(18, 22)
        self.ratings = self.rookie_ratings()
        self.potential = self.calculate_potential()
        self.overall = self.calculate_overall()
        self.salary = 0
        self.contract_years = 3

    # generates potential for rookies based on rarity
    def calculate_potential(self):
        potential_tiers = [
        (90, 99),   # S
        (80, 89),   # A
        (70, 79),   # B
        (60, 69),   # C
        (50, 59)    # D
        ]
        weights = [5, 12, 28, 30, 25]  # percentages adding to 100

        tier = random.choices(potential_tiers, weights=weights, k=1)[0]
        return random.randint(tier[0], tier[1])

    # generates ratings for rookies according to their position
    def rookie_ratings(self):
        if self.position == 'PG':
            ratings = {
            'Shooting': random.randint(60, 80),
            'Defense': random.randint(45, 60),
            'Passing': random.randint(65, 85),
            'Rebounding': random.randint(40, 55),
            'Athleticism': random.randint(50, 99)
            }
        elif self.position == 'SG':
            ratings = {
            'Shooting': random.randint(60, 85),
            'Defense': random.randint(55, 70),    
            'Passing': random.randint(55, 65),
            'Rebounding': random.randint(40, 55),
            'Athleticism': random.randint(55, 99)
            }
        elif self.position == 'SF':
            ratings = {
            'Shooting': random.randint(60, 80),
            'Defense': random.randint(60, 75),    
            'Passing': random.randint(50, 65),
            'Rebounding': random.randint(50, 65),
            'Athleticism': random.randint(60, 99)
            }
        elif self.position == 'PF':
            ratings = {
            'Shooting': random.randint(40, 60),
            'Defense': random.randint(60, 85),    
            'Passing': random.randint(40, 50),
            'Rebounding': random.randint(60, 80),
            'Athleticism': random.randint(55, 99)
            }
        else: # C
            ratings = {
            'Shooting': random.randint(40, 50),
            'Defense': random.randint(60, 85),    
            'Passing': random.randint(40, 45),
            'Rebounding': random.randint(70, 85),
            'Athleticism': random.randint(40, 90)
            }
        return ratings
