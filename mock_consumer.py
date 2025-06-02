def mock_consume_latest_processed_data1(*args, **kwargs):
    return [
        {
            "team_name": "Hanwha Eagles",
            "team_stats": {
                "wins": 10,
                "losses": 5,
                "draws": 1,
                "score_difference": 25,
                "avg_form_score": 7.8
            },
            "batters": [
                {
                    "player_name": "Hwang Young-mook",
                    "position": "2B",
                    "on_base_percentage": 0.333,
                    "batting_average": 0.333,
                    "form_score": 7.2
                },
                {
                    "player_name": "Kim Min-woo",
                    "position": "CF",
                    "on_base_percentage": 0.375,
                    "batting_average": 0.300,
                    "form_score": 6.9
                }
            ],
            "pitchers": [
                {
                    "player_name": "Im Chan-kyu",
                    "era": 6.00,
                    "whip": 1.67,
                    "k_per_9": 6.00,
                    "bb_per_9": 3.00,
                    "form_score": 7.5
                }
            ]
        },
        {
            "team_name": "LG Twins",
            "team_stats": {
                "wins": 8,
                "losses": 6,
                "draws": 2,
                "score_difference": 15,
                "avg_form_score": 7.5
            },
            "batters": [
                {
                    "player_name": "Lee Jae-won",
                    "position": "RF",
                    "on_base_percentage": 0.400,
                    "batting_average": 0.350,
                    "form_score": 8.1
                }
            ],
            "pitchers": [
                {
                    "player_name": "Casey Kelly",
                    "era": 3.50,
                    "whip": 1.20,
                    "k_per_9": 8.50,
                    "bb_per_9": 2.20,
                    "form_score": 8.3
                }
            ]
        }
    ]

def sort_by_avg_form_score(data):
    """
    Sorts the data by average form score in descending order.
    """
    return sorted(data, key=lambda x: x['team_stats']['avg_form_score'], reverse=False)

def sort_teams_players_by_form_score(data):
    """
    Sorts each team's players by their form score in descending order.
    """
    for team in data:
        team['batters'] = sorted(team['batters'], key=lambda x: x['form_score'], reverse=True)
        team['pitchers'] = sorted(team['pitchers'], key=lambda x: x['form_score'], reverse=True)
    return data

def mock_consume_latest_processed_data(*args, **kwargs):
    """
    Mock function to simulate consuming processed data from Kafka.
    Returns a fixed set of team data.
    """
    data = mock_consume_latest_processed_data1(*args, **kwargs)
    
    # Sort the data by average form score
    sorted_data = sort_by_avg_form_score(data)
    sorted_data = sort_teams_players_by_form_score(sorted_data)
    
    return sorted_data