#!/usr/bin/env bash

printf '%b' '\n\n++++ Testing test_game_info.py ++++\n\n'
python3 -m tests.test_game_info
printf '%b' '\n\n++++ Testing test_team_stats.py ++++\n\n'
python3 -m tests.test_team_stats
