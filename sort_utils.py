
def sort_by_avg_form_score(data):
    return sorted(data, key=lambda x: x['team_form_score'], reverse=True)

def sort_teams_by_form_score(data):
    for team in data:
        team['batters'] = sorted(team['batters'], key=lambda x: x['form_score'], reverse=True)
        team['pitchers'] = sorted(team['pitchers'], key=lambda x: x['form_score'], reverse=True)
    return data

