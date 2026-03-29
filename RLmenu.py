from RLleague import League
from RLui import display_teams, main_menu

league = League()

display_teams(league)

main_menu(league)

print(f"\nFree Agents: {len(league.free_agents)}")

