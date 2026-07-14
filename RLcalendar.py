from datetime import date, timedelta

class Calendar:
    def __init__(self):
        start_year = date.today().year
        self.current_date = date(start_year, 10, 22)
        self.season_start_year = start_year
        self.season_end_year = start_year + 1
        self.phase = "Regular Season"
        self.trade_deadline = date(self.season_end_year, 1, 15)
        self.playoffs_start = date(self.season_end_year, 3, 1)
        self.draft_date = date(self.season_end_year, 5, 15)
        self.free_agency_start = date(self.season_end_year, 7, 10)
        self.season_end = date(self.season_end_year, 10, 21)

    # Displays the current date of the game.
    def display_date(self):
        print(f"{self.current_date.strftime('%B %d, %Y')} | {self.phase}")
    
    # Advances the day of the game and updates the phase of the game.
    def advance_day(self):
        self.current_date += timedelta(days=1)
        if self.current_date >= self.trade_deadline and self.phase == "Regular Season":
            self.phase = "Trade Deadline"
        elif self.current_date >= self.playoffs_start and self.phase in ["Regular Season", "Trade Deadline"]:
            self.phase = "Playoffs"
        elif self.current_date >= self.draft_date and self.phase == "Playoffs":
            self.phase = "Draft"
        elif self.current_date >= self.free_agency_start and self.phase == "Draft":
            self.phase = "Free Agency"
        elif self.current_date >= self.season_end and self.phase == "Free Agency":
            self.season_start_year += 1
            self.season_end_year += 1
            self.current_date = date(self.season_start_year, 10, 22)
            self.phase = "Regular Season"
            self.new_season()

    # Sets the importants dates for the start of the next season.    
    def new_season(self):
        self.trade_deadline = date(self.season_end_year, 1, 15)
        self.playoffs_start = date(self.season_end_year, 3, 1)
        self.draft_date = date(self.season_end_year, 5, 15)
        self.free_agency_start = date(self.season_end_year, 7, 10)
        self.season_end = date(self.season_end_year, 10, 21)

    def get_season_label(self):
        return f"{str(self.season_start_year)[-2:]}-{str(self.season_end_year)[-2:]}"
    
    def get_draft_year(self):
        return self.season_end_year