import random
from RLdata import player_first, player_last, position


class Player:
    id_counter = 0
    def __init__(self, player_first, player_last, position):
        Player.id_counter += 1
        self.player_id = f"P{Player.id_counter:03d}"
        self.player_first = random.choice(player_first)
        self.player_last = random.choice(player_last)
        self.position = random.choice(position)
        self.age = random.randint(19, 35)
        self.ratings = self.generate_ratings()
        self.potential = self.calculate_potential()
        self.overall = self.calculate_overall()
        self.contract_value = self.generate_value()
        self.salary = self.generate_contract()
        self.contract_years = self.generate_contract_years()

    # Potential is based on age, with younger players having a chance at higher potential
    def calculate_potential(self):
        if self.age <= 22:
            return random.randint(65, 99)
        elif self.age <= 29:
            return random.randint(60, 85)
        else: # 30+
            return random.randint(40, 70)


    # ratings are generated based on position, with some randomness to create variety among players
    def generate_ratings(self):
            if self.position == 'PG':
                ratings = {
                'Shooting': random.randint(60, 99),
                'Defense': random.randint(45, 70),
                'Passing': random.randint(65, 99),
                'Rebounding': random.randint(40, 65),
                'Athleticism': random.randint(50, 99)
                }
            elif self.position == 'SG':
                ratings = {
                'Shooting': random.randint(60, 99),
                'Defense': random.randint(55, 80),    
                'Passing': random.randint(55, 75),
                'Rebounding': random.randint(40, 65),
                'Athleticism': random.randint(55, 99)
                }
            elif self.position == 'SF':
                ratings = {
                'Shooting': random.randint(60, 90),
                'Defense': random.randint(60, 90),    
                'Passing': random.randint(50, 75),
                'Rebounding': random.randint(50, 75),
                'Athleticism': random.randint(60, 99)
                }
            elif self.position == 'PF':
                ratings = {
                'Shooting': random.randint(40, 70),
                'Defense': random.randint(60, 99),    
                'Passing': random.randint(40, 60),
                'Rebounding': random.randint(60, 90),
                'Athleticism': random.randint(55, 99)
                }
            else: # C
                ratings = {
                'Shooting': random.randint(40, 60),
                'Defense': random.randint(60, 99),    
                'Passing': random.randint(40, 50),
                'Rebounding': random.randint(70, 99),
                'Athleticism': random.randint(40, 90)
                }
            return ratings
    
    # overall is calculated based on ratings, with different weights for each position to reflect their unique skill sets
    def calculate_overall(self):
        if self.position == 'PG':
            overall = ((self.ratings['Shooting'] * 0.3) + (self.ratings['Defense'] * 0.2) + (self.ratings['Passing'] * 0.3) + (self.ratings['Rebounding'] * 0.1) + (self.ratings['Athleticism'] * 0.1))
        elif self.position == 'SG':
            overall = ((self.ratings['Shooting'] * 0.35) + (self.ratings['Defense'] * 0.2) + (self.ratings['Passing'] * 0.15) + (self.ratings['Rebounding'] * 0.1) + (self.ratings['Athleticism'] * 0.2))
        elif self.position == 'SF':
            overall = ((self.ratings['Shooting'] * 0.25) + (self.ratings['Defense'] * 0.25) + (self.ratings['Passing'] * 0.2) + (self.ratings['Rebounding'] * 0.15) + (self.ratings['Athleticism'] * 0.15))
        elif self.position == 'PF':
            overall = ((self.ratings['Shooting'] * 0.2) + (self.ratings['Defense'] * 0.3) + (self.ratings['Passing'] * 0.2) + (self.ratings['Rebounding'] * 0.2) + (self.ratings['Athleticism'] * 0.1))
        else: # C
            overall = ((self.ratings['Shooting'] * 0.1) + (self.ratings['Defense'] * 0.4) + (self.ratings['Passing'] * 0.1) + (self.ratings['Rebounding'] * 0.3) + (self.ratings['Athleticism'] * 0.1))
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



