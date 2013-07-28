# Data Format Design Document

The current CSV data is lacking in many regards, most notably important
information about the game is contained in a human readable summary, but not
in machine readable columns. We therefore are going to parse, correct, and
rewrite the data in a new format to be easier to work with.

## Old Format

The old data format used the following columns:
    
* **GameID**: Year, Month, Day, Away Team, and Home Team. For example:
  20020905\_SF@NYG
* **Quarter**: Quarter of the game, with 1-4 being the normal game, 5+ is
  overtime.
* **Minute**: Minutes left in the game. 60-0 for normal time, negative numbers
  -1 to -15 are overtime. Blank is used at the stat of games when the clock is
  stopped.
* **Seconds**: Seconds, counting down from 60-0 even when in overtime.
* **Offense**: The team that starts with possession, including the kicking team
  when punting or setting up a kickoff.
* **Defense**: The team that is not the offense, as defined above.
* **Down**: 1-4, although some are left blank if a down doesn't make sense (for
  example on a kickoff).
* **ToGo**: Yards to first down, left blank if a first down doesn't make sense.
* **Yardline**: Yards from the goal line for the Offensive team, 100-0.
* **Description**: A human readable description of the play. Unfortunately it
  contains keywords that tell you about the play, for example "TOUCHDOWN" or
  "FUMBLE".
* **OffScore**: The total score that the team on Offense has.
* **DefScore**: The total score that the team on Defense has.
* **Season**: The year the season started in.

## New Format

**Version**: 0.1

The new format is also a comma separated variable list, with the following
columns:

### Static Game Information

* **Season**: The year the season started in.
* **Year**: The complete  year the game took place.
* **Month**: The two digit month. Leading zeros are optional, but encouraged.
* **Day**: Two digit day of the month. Leading zeros are optional, but
  encouraged.
* **Home Team**: The team designated by the NFL as the home team using a team
  code.
* **Away Team**: The team designated by the NFL as the away team using a team
  code.

### Game Information

* **Home Team Score**: The score of the home team at the time when the play
  starts. This means that points scored on a play first show up on the next
  line.
* **Away Team Score**: The score of the away team at the time when the play
  starts.
* **Time**: The time since the game started in seconds. 0-3600 would cover the
  first four quarters, overtime simply continues counting past 3600.

### Play Information

* **Team with Ball**: The team with possession of the ball at the start of the
  play, using a team code.
* **Down**: The down at the start of the play. 1-4 is used for normal plays,
  NULL is used when a down does not make sense.
* **Yard Line**: Yards from the goal line.
* **To Go**: Yards to first down, NULL is used if a first down doesn't make
  sense.
* **Score Type**: Type of scoring play made, of the following: Touchdown, Extra
  Point, Two Point Conversion, Safety, and Field Goal.
* **Scoring Team**: The team that scored points given as a team code. If no
  score was made on the play, NULL is used.

### Other 

* **Description**: A human readable description of the play. It may contain
  anything the collator thinks is relevant, but anything numeric should be
  reflected in the other columns. That is, it should be assumed that any script
  is ignoring this field.

## Team Codes

Each team is identified by a unique two or three letter [A-Z] code, as follows:

* **AFC**: AFC Probowl Team
* **ARI**: Arizona Cardinals
* **ATL**: Atlanta Falcons
* **BAL**: Baltimore Ravens
* **BUF**: Buffalo Bills
* **CAR**: Carolina Panthers
* **CHI**: Chicago Bears
* **CIN**: Cincinnati Bengals
* **CLE**: Cleveland Browns
* **DAL**: Dallas Cowboys
* **DEN**: Denver Broncos
* **DET**: Detroit Lions
* **GB**:  Green Bay Packers
* **HOU**: Houston Texans
* **IND**: Indianapolis Colts
* **JAC**: Jacksonville Jaguars
* **KC**:  Kansas City Chiefs 
* **MIA**: Miami Dolphins
* **MIN**: Minnesota Vikings
* **NE**: New England Patriots
* **NO**: New Orleans Saints
* **NFC**: NFC Probowl Team
* **NYG**: New York Giants
* **NYJ**: New York Jets
* **OAK**: Oakland Raiders
* **PHI**: Philadelphia Eagles
* **PIT**: Pittsburgh Steelers
* **SD**: San Diego Chargers
* **SEA**: Seattle Seahawks
* **SF**: San Francisco 49ers
* **STL**: Saint Louis Rams
* **TB**: Tampa Bay Buccaneers
* **TEN**: Tennessee Titans
* **WAS**: Washington Redskins
