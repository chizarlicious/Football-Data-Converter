#!/usr/bin/env bash

printf '%b' '\n++++ Testing test_game_info.py ++++\n'
python3 -m tests.test_game_info
printf '%b' '\n++++ End ++++\n'

printf '%b' '\n++++ Testing test_team_stats.py ++++\n'
python3 -m tests.test_team_stats
printf '%b' '\n++++ End ++++\n'

printf '%b' '\n++++ Testing play_by_play/test_general.py ++++\n'
python3 -m tests.play_by_play.test_general
printf '%b' '\n++++ End ++++\n'

printf '%b' '\n++++ Testing play_by_play/test_state.py ++++\n'
python3 -m tests.play_by_play.test_state
printf '%b' '\n++++ End ++++\n'

printf '%b' '\n++++ Testing play_by_play/test_play.py ++++\n'
python3 -m tests.play_by_play.test_play
printf '%b' '\n++++ End ++++\n'

printf '%b' '\n++++ Testing play_by_play/test_penalty.py ++++\n'
python3 -m tests.play_by_play.test_penalty
printf '%b' '\n++++ End ++++\n'

printf '%b' '\n++++ Testing play_by_play/test_turnover.py ++++\n'
python3 -m tests.play_by_play.test_turnover
printf '%b' '\n++++ End ++++\n'

printf '%b' '\n++++ Testing test_title_info.py ++++\n'
python3 -m tests.test_title_info
printf '%b' '\n++++ End ++++\n'
