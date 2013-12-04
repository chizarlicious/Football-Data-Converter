# Data Format Design Document

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
