# List of team names, subject to change
team_name = [
    "Thunder Hawks",
    "River City Raiders",
    "Metro Monarchs",
    "Skyline Serpents",
    "Crimson Wolves",
    "Blue Ridge Ballers",
    "Golden Vipers",
    "Shadow Legends",
    "Patriot Panthers",
    "Phoenix Flames",
    "Wildfire Warriors",
    "Jetstream Jumpers",
    "Steel Storm",
    "Avalanche Blizzards",
    "Iron Giants",
    "Arctic Eagles",
    "Night Riders",
    "Silver Spartans",
    "Lightning Crew",
    "Stormbreakers",
    "Tornado Tigers",
    "Nova Knights",
    "Timberline Titans",
    "Coastal Crushers"
]

divisions = ["Atlantic", "Central", "Southeast", "Northwest", "Pacific", "Southwest"]

# Puts the teams into conferences, with the first 12 teams in the Eastern Conference and the remaining 12 in the Western Conference. This allows for easier scheduling and division of teams within the league.
conferences = {
    "Eastern": {
        "Atlantic": team_name[:4],
        "Central": team_name[4:8],
        "Southeast": team_name[8:12]
    },
    "Western": {
        "Northwest": team_name[12:16],
        "Pacific": team_name[16:20],
        "Southwest": team_name[20:24]
    }
}

# List of player first and last names, as well as positions, used to generate players in the league. The names list can be modified later to add more names for diversity later
player_first = ['John', 'Bill', 'Jimmy', 'Drazen', 'Mose', 'Deandre', 'Tyrone', 'Kai', 'Jaylen', 'Thomas', 'Nikola', 
                'Kyrie', 'Stephen', 'Kevin', 'Michael', 'Larry', 'Jaren', 'Steven', 'Trey', 'Santi', 'OG', 'Ace', 
                'Scottie', 'Devin', 'Miles', 'Bruce', 'Jalen', 'Carter', 'Jamal', 'Brandon', 'Julian', 'Stephon', 
                'Jared', 'Max', 'Alex', 'Cody', 'Josh', 'Bryce', 'Jordan', 'Bob', 'Dwyane', 'Isaiah', 'Mike', 'Cade',
                'Anthony', 'Egor', 'Rudy', 'Mo', 'Shaun', 'Derrick', 'Walter', 'Zach', 'Nate', 'Victor', 'Kyle', 'Peter', 'Paul', 'Jason']

player_last = ['Wayne', 'White', 'Jordan', 'James', 'Irving', 'Bryant', 'Curry', 'Morant', 'Westbrook', 'Durant',
               'Clark', 'Clarke', 'Dada', 'Duguid', 'Rowe', 'Brooks', 'Parker', 'Doe', 'Baker', 'Alexander', 'Jokic', 'Edwards',
               'Thompson', 'Fox', 'Perry', 'Edey', 'Doncic', 'Rodman', 'Pippen', 'George', 'Green', 'Harper', 'Holiday',
               'Huff', 'Hyland', 'Ingram', 'Johnson', 'Jackson', 'Lillard', 'Love', 'Lopez', 'Nash', 'Rose', 'Russell',
               'Smith', 'West', 'Young', 'Martin', 'Mitchell', 'Bunyun', 'Robinson', 'Sharpe', 'Sims', 'Tatum', 'VanVleet', 'Collins']

position = ['PG', 'SG', 'SF', 'PF', 'C']

ROSTER_BLUEPRINTS = {
    "Champion Favorite": [
        ("elite", 92, 99), ("elite", 88, 94),
        ("starter", 82, 88), ("starter", 80, 86), ("starter", 78, 84), ("starter", 76, 82), ("starter", 75, 80),
        ("role", 72, 78), ("role", 70, 76), ("role", 68, 74), ("role", 65, 71), ("role", 62, 68)
    ],
    "Contender": [
        ("elite", 88, 93),
        ("starter", 82, 87), ("starter", 80, 85), ("starter", 78, 83), ("starter", 76, 81), ("starter", 74, 79), ("starter", 72, 77),
        ("role", 70, 75), ("role", 68, 73), ("role", 65, 71), ("role", 62, 68), ("role", 60, 66)
    ],
    "Playoff Team": [
        ("starter", 80, 85), ("starter", 78, 83), ("starter", 76, 81), ("starter", 74, 79), ("starter", 72, 77),
        ("role", 70, 75), ("role", 68, 73), ("role", 66, 71), ("role", 64, 69), ("role", 62, 67), ("role", 60, 65), ("role", 58, 63)
    ],
    "Retooling": [
        ("starter", 76, 81), ("starter", 74, 79), ("starter", 72, 77),
        ("role", 68, 74), ("role", 66, 72), ("role", 64, 70), ("role", 62, 68), ("role", 60, 66),
        ("role", 58, 64), ("role", 56, 62), ("role", 54, 60), ("role", 52, 58)
    ],
    "Rebuilding": [
        ("starter", 70, 75), ("starter", 68, 73),
        ("role", 66, 72), ("role", 64, 70), ("role", 62, 68), ("role", 60, 66), ("role", 58, 64),
        ("role", 55, 62), ("role", 53, 60), ("role", 50, 58), ("role", 48, 55), ("role", 45, 52)
    ],
}

ELITE_THRESHOLD = 88
STARTER_THRESHOLD = 75