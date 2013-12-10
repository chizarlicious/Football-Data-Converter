# Data Format Design Document

**Version**: 0.1

The data format is a [JSON](https://en.wikipedia.org/wiki/JSON) file with the
following objects:

## Seasons Object

* **season**: The year the season started in.
* **games**: A list of game objects.

### Game Object

The Game Object contains information about a single football game.

* **home team**: The team designated by the NFL as the home team using a team
  code.
* **away Team**: The team designated by the NFL as the away team using a team
  code.
* **venue**: A Venue Object.
* **datetime**: A Datetime Object.
* **weather**: A Weather Object.
* **betting**: A Betting Object.
* **officials**: An Officials Object.
* **team stats**: A Team Stats Object.
* **plays**: A list of Play Objects.

#### Venue Object

The Venue Object contains information about the venue where the game was
played.

* **stadium**: The name of the stadium where the game was played.
* **attendance**: The number of attending spectators.
* **surface**: The playing field surface type.

#### Datetime Object

The Datetime Object contains information about when the game was played.

* **date**: The date when the game was played in its local timezone as defined
  by [ISO 8601](https://en.wikipedia.org/wiki/Iso_date).
* **start time**: The time when the game started in its local timezone. A 24
  hour clock is used, with a colon between the hour and the minute. The time is
  rounded to the nearest minute.
* **duration**: The duration of the game, in seconds.

#### Weather Object

The Weather Object contains information about the weather when the game was
started.

* **temperature**: The temperature in degrees Fahrenheit, rounded to the
  nearest degree.
* **relative humidity**: Relative humidity given as a double between [0., 1.].
* **wind speed**: Wind speed in miles per hour, rounded to the nearest integer.
* **wind chill**: Effective temperature when accounting for wind chill, in
  degrees Fahrenheit, rounded to the nearest degree.

#### Betting Object

The Betting Object contains information about the gambling odds given before
the game.

* **winner**: The expected winner.
* **spread**: The amount of points subtracted from the winner's score when
  comparing it to the loser's to see if they won for purposes of betting.
* **over under**: The over/under line for betting. A negative number indicates
  'under' while a positive number indicates 'over'.

#### Officials

The Officials Object contains information about the game officials.

* **referee**: The name of the referee.
* **umpire**: The name of the umpire.
* **head linesman**: The name of the head linesman.
* **field judge**: The name of the field judge.
* **back judge**: The name of the back judge.
* **side judge**: The name of the side judge.
* **line judge**: The name of the line judge.

#### Team Stats

The Team Stats Object contains information about game statistics for both
teams.

* **home team**: A Statistics Object for the home team.
* **away team**: A Statistics Object for the away team.

##### Statistics Object

The Statistics Object contains information about game statistics for one team.

* **first downs**: The number of first downs achieved.
* **rush**: A Rush Object.
* **pass**: A Pass Object.
* **sacks**: A Sacks Object.
* **fumbles**: A Fumbles Object.
* **penalties**: A Penalties Object.

###### Rush Object

A Rush Object contains information about rushing statistics for the game.

* **plays**: Number of rushing plays run.
* **yards**: Number of rushing yards gained.
* **touchdowns**: Number of rushing touchdowns scored.

###### Pass Object

A Pass Object contains information about passing statistics for the game.

* **plays**: Number of passing plays run.
* **yards**: Number of passing yards gained.
* **touchdowns**: Number of passing touchdowns scored.
* **successful**: Number of successful passing plays.
* **interceptions**: Number of interceptions thrown.

###### Sacks Object

A Sacks Object contains information about sack statistics for the game.

* **plays**: Number of plays where the quarterback was sacked.
* **yards**: Number of yards lost, given as a negative number.

###### Fumbles Object

A Fumbles Object contains information about fumble statistics for the game.

* **plays**: Number of plays where the team fumbled the ball.
* **lost**: Number of fumbles lost to the defense.

###### Penalties Object

A Penalties Object contains information about penalty statistics for the game.

* **plays**: Number of plays with a penalty.
* **yards**: Number of yards lost due to penalties, given as a negative number.

#### Play Object

A Play Object contains information about a specific play.

* **number**: The number of the play. The first play of the game is 0, the
  second is 1, and so on until the last play.
* **score**: A Score Object.
* **state**: A State Object.
* **play**: A Play Object.
* **turnover**: A Turnover Object.
* **penalty**: A Penalty Object.

##### Score Object

A Score Object contains information about the games score.

* **home**: The home team's score at the beginning of the play.
* **away**: The away team's score at the beginning of the play.

##### State Object

A State Object contains information about the state of the play as the ball is
snapped.

* **offense**: The team code of the team on offense.
* **down**: The down, given as a number from 1-4 for normal plays, and 0 for
  plays where there is no first down marker.
* **yards to first down**: Yards to the first down marker or goal line if no
  first down is possible.
* **yards to goal**: Yards to the goal line.
* **time**: The time the play started, counted in seconds since the game
  started.

##### Play Object

An Play Object contains information about the type of play.

* **type**: The type of play.
* **scoring**: A Scoring Object.

####### Scoring Object

A Scoring Object contains information about the type of score made on the play.

* **type**: Type of scoring play.
* **team**: The team code of the team that scored.

##### Turnover Object

A Turnover Object contains information about any turnovers on the play

* **type**: Type of turnover.
* **recovered by**: The team code of the recovering team.

##### Penalty Object

A Penalty Object contains information about any penalties on the play.

* **type**: Type of penalty.
* **on**: Team code for the team that committed the penalty.
* **player**: The player the committed the penalty.
* **yards**: Yards lost to the penalty, given as a negative number.
* **no play**: Indicates that the penalty invalidated the play.

# Team Codes

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
