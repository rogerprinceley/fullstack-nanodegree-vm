# rogerprinceley's Swiss Tournament toolkit
This project contains SQL code and python code that provide tools to assist in conducting a tournament around the Swiss Tournament system. This content is delivered as a vagrant package. Please ensure that you vagrant configured on your system before working with this code.

## How to use (Basic Test)
1. Click [here](https://github.com/rogerprinceley/fullstack-nanodegree-vm/archive/master.zip) or on `Download Zip` button above to download the project
2. Extract the contents of the zip file
3. Change working directory to vagrant folder: `cd *<extracted location>*/fullstack-nanodegree-vm/vagrant`
4. Start the vagrant environment: `vagrant up`
5. Connect the vagrant environment: `vagrant ssh`
6. Change working directory to vagrant folder: `cd /vagrant`
7. Setup the database by executing the SQL file: `psql -f tournament.sql`
8. Execute the basic test code by running: `python.exe tournament_test.py`

## Available python functions
* `connect()` - Connect to the PostgreSQL database.  Returns a database connection.
* `deleteMatches()` - Remove all the match records from the database.
* `deletePlayers()` - Remove all the player records from the database.
* `countPlayers()` - Returns the number of players currently registered.
* `registerPlayer(name)` - Adds a player to the tournament database.
* `playerStandings()` - Returns a list of the players and their win records, sorted by wins.
* `reportMatch(winner, loser)` - Records the outcome of a single match between two players (accepts ids.)
* `swissPairings()` - Returns a list of pairs of players for the next round of a match.

## Project contents - INCOMPLETE

## References
This project runs on code provided by the course [Intro to Relational Databases](https://www.udacity.com/course/intro-to-relational-databases--ud197-nd) at [Udacity](http://www.udacity.com)

