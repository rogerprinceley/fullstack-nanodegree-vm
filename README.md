# rogerprinceley's Full Stack Nanodegree repository 

## Completed Projects

### Tournament Project
This project contains SQL and python code that provide tools to assist in conducting a tournament around the Swiss-style system. This content is delivered as a vagrant package. Please ensure that you vagrant configured on your system before working with this code.

#### How to use (Basic Test)
1. Click [here](https://github.com/rogerprinceley/fullstack-nanodegree-vm/archive/master.zip) or on `Download Zip` button above to download the project
2. Extract the contents of the zip file
3. Change working directory to vagrant folder: `cd <extracted location>/fullstack-nanodegree-vm/vagrant`
4. Start the vagrant environment: `vagrant up`
5. Connect to the vagrant environment: `vagrant ssh`
6. Change working directory to vagrant folder: `cd /vagrant/tournament`
7. Setup the database by executing the SQL file: `psql -f tournament.sql`
8. Execute the basic test code by running: `python.exe tournament_test.py`

#### Available python functions
* `connect()` - Connect to the PostgreSQL database.  Returns a database connection.
* `deleteMatches()` - Remove all the match records from the database.
* `deletePlayers()` - Remove all the player records from the database.
* `countPlayers()` - Returns the number of players currently registered.
* `registerPlayer(name)` - Adds a player to the tournament database.
* `playerStandings()` - Returns a list of the players and their win records, sorted by wins.
* `reportMatch(winner, loser, outcome=1)` - Records the outcome of a single match between two players (accepts ids.)
* `swissPairings()` - Returns a list of pairs of players for the next round of a match.
* `matchMaker(pool, pairs=None)` - Recursive Depth-first search like method that updates pairs until pool is empty. 
* `hasPlayed(player1, player2)` - Checks if the two players passed as arugments have played a match together.

#### Tables and Views
##### Tables
* players - Contains the players participating in the tournament
* matches - Contains a register of the matches that players have participated in
* results - Contains the results of matches that have been played

##### Views
* v_simple_standings - Simple standings view at best includes match-win percentage
* v_standings: Uses v_simple_standings to compute Opponent Match Wins (OMW) value

#### Project contents
* `/vagrant/tournament/tournament.sql` - SQL statements needed to setup postgresql
* `/vagrant/tournament/tournement.py` - Contains all the functions mentioned above
* `/vagrant/tournament/tournament_test.py` - Basic test script provided along with the starter source for this project

#### Extra credit options attempted
1. Prevent rematches between players
  * Uses a modified Depth-First Search algorithm using a recursive function.
  * May not be efficient as a seperate connection is spawned for every hasPlayed() call.
2. Support games where a draw (tied game) is possible. This will require changing the arguments to reportMatch.
  * Additional argument `outcome` added to reportMatch
  * 1 (default): denotes player1 wins, 0: denotes a draw, -1: denotes player2 wins
  * If any other value is provided it assumes the default case i.e., player1 wins
3. When two players have the same number of wins, rank them according to OMW (Opponent Match Wins), the total number of wins by players they have played against.
  * Implementation does not use points as outlined in the [MTG tiebreaker guide.](https://www.wizards.com/dci/downloads/tiebreakers.pdf)

#### References
* The tournament project is based off the course [Intro to Relational Databases](https://www.udacity.com/course/intro-to-relational-databases--ud197-nd) at [Udacity.](http://www.udacity.com)
* The tournament project Getting Started guide can be found [here.](https://docs.google.com/document/d/16lgOm4XprTaKxAa8w02y028oBECOoB1El1ReddADEeY/pub?embedded=true)
* Details on Opponent Match Wins information can be found in the [MTG tiebreaker guide.](https://www.wizards.com/dci/downloads/tiebreakers.pdf)

## Pending Projects

### Catalog Project (Next) 

### Forum Project (Later)


