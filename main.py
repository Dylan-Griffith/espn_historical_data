import pandas as pd
from ff_espn_api import League

league_id = 207951
years = [2015, 2016, 2017, 2018]
swid = '{EBA13257-A03D-4F49-A132-57A03DDF49E2}'
espn_s2 = 'AEA6V72GDokBcm9I5EtHPmnb69ywSlFDv68rZfa2HGA18RnnTKF8OzjAt%2FLGtz0PuM1CrZAVWyK7faqZ%2BwThvxWqIS20HVtHe6WmYAMt3rZbhBZAa3NkeShrB3fgUUIeYgQ3f8k1dJ8mw0SPrLV7KKxDTZzik6vpEkd%2BgslXJ5dTj63mjhB1%2Blp84dgi3mL58Sv8NvHUH%2FYTaAZCax8pXx7M7eDKbiWOtgDmPx1ec7w6tnrUJerrxg04gVYZ2Kp4wQn%2FeAYG7tfDyWRYq0OqSuOG'


def get_weekly_data(week, year):
    league = League(league_id, year, espn_s2, swid)

    week_matchup = league.scoreboard(week)
    frame = []
    for team in week_matchup:
        away_team = team.away_team.team_name
        away_score = team.away_score

        home_team = team.home_team.team_name
        home_score = team.home_score

        frame.append([year, week, away_team, away_score, home_score])
        frame.append([year, week, home_team, home_score, away_score])

    df = pd.DataFrame(frame, columns=['year', 'week', 'team_name', 'score', 'opp_score'])
    df['win'] = df['score'] > df['opp_score']
    df['week_avg'] = df['score'].mean()
    df['plus_minus'] = df['score'] - df['score'].mean()
    df['opp_plus_minus'] = df['opp_score'] - df['score'].mean()

    return df


def get_league_historical_data():
    years = [2015, 2016, 2017, 2018]

    t = []
    for year in years:
        print('Getting {}'.format(year))
        for x in range(1, 14):
            print('week: ', x)
            t.append(get_weekly_data(x, year))

    return pd.concat(t)


def save_data(df):
    df.to_csv('espn_historical_data.csv')


def main():
    df = get_league_historical_data()
    save_data(df)


if __name__ == '__main__':
    main()
