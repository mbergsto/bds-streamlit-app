def mock_consume_latest_processed_data(*args, **kwargs):
    return [
        {
            "team_name": "Hanwha Eagles",
            "team_form_score": 54,
            "team_stats": {
                "wins": 10,
                "losses": 5,
                "draws": 1,
                "score_difference": 25
            },
            "batters": [
                {
                    "player_name": "Hwang Young-mook",
                    "on_base_percentage": 0.333,
                    "batting_average": 0.333,
                    "form_score": 7.2
                },
                {
                    "player_name": "Kim Min-woo",
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
            "team_form_score": 44,
            "team_stats": {
                "wins": 8,
                "losses": 6,
                "draws": 2,
                "score_difference": 15
            },
            "batters": [
                {
                    "player_name": "Lee Jae-won",
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

