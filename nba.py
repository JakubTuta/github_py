from requests import get
from pprint import PrettyPrinter

BASE_URL = "https://data.nba.net"
ALL_JSON = "/prod/v1/today.json"

printer = PrettyPrinter()


def get_links():
    data = get(f"{BASE_URL}{ALL_JSON}").json()
    links = data['links']
    return links


def get_scoreboard():
    print("TODAY'S GAMES: \n\n")
    scoreboard = get_links()['currentScoreboard']
    games = get(f"{BASE_URL}{scoreboard}").json()['games']

    for game in games:
        home_team = game['hTeam']
        visit_team = game['vTeam']
        clock = game['clock']
        period = game['period']

        print("========================")
        print(f"{home_team['triCode']} vs {visit_team['triCode']}")
        print(f"{home_team['score']} - {visit_team['score']}")
        print(f"Kwarta: {period['current']} - czas: {clock}")


def get_stats():
    stats = get_links()['leagueTeamStatsLeaders']
    teams = get(f"{BASE_URL}{stats}").json()[
        'league']['standard']['regularSeason']['teams']

    teams = list(filter(lambda x: x['name'] != 'Team', teams))
    teams.sort(key=lambda x: int(x['ppg']['rank']))

    for i, team in enumerate(teams):
        name = team['name']
        nickname = team['nickname']
        ppg = team['ppg']['avg']
        print(f"{i+1}. {name} {nickname} - {ppg}")


def main():
    info = input("Co chcesz zobaczyć?:\nGry\nStatystkyki\n")

    if info == "Gry" or info == "gry":
        get_scoreboard()
    elif info == "Statystyki" or info == "statystyki":
        get_stats()
    else:
        print("Zła komenda")


if __name__ == "__main__":
    main()
