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
                'Anthony', 'Egor', 'Rudy', 'Mo', 'Shaun', 'Derrick', 'Walter', 'Zach', 'Nate', 'Victor', 'Kyle', 'Peter', 'Paul']

player_last = ['Wayne', 'White', 'Jordan', 'James', 'Irving', 'Bryant', 'Curry', 'Morant', 'Westbrook', 'Durant',
               'Clark', 'Dada', 'Duguid', 'Rowe', 'Brooks', 'Parker', 'Doe', 'Baker', 'Alexander', 'Jokic', 'Edwards',
               'Thompson', 'Fox', 'Perry', 'Edey', 'Doncic', 'Rodman', 'Pippen', 'George', 'Green', 'Harper', 'Holiday',
               'Huff', 'Hyland', 'Ingram', 'Johnson', 'Jackson', 'Lillard', 'Love', 'Lopez', 'Nash', 'Rose', 'Russell',
               'Smith', 'West', 'Young', 'Martin', 'Mitchell', 'Bunyun', 'Robinson', 'Sharpe', 'Sims', 'Tatum', 'VanVleet']

position = ['PG', 'SG', 'SF', 'PF', 'C']
