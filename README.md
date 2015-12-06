# rogerprinceley's Swiss Tournament toolkit

This project contains a database and python code that provide tools to assist in conducting a tournament around the Swiss Tournament system.

# How to use (Basic Test)
1. Click [here](https://github.com/rogerprinceley/fullstack-nanodegree-vm/archive/master.zip) or on `Download Zip` button above to download the project
2. Extract the contents of the zip file
3. Execute the code by running: `python.exe tournament_test.py`

# Available python functions
* `connect()` - Connect to the PostgreSQL database.  Returns a database connection.
* `deleteMatches()` - Remove all the match records from the database.
* `deletePlayers()` - Remove all the player records from the database.
* `countPlayers()` - Returns the number of players currently registered.
* `registerPlayer(name)` - Adds a player to the tournament database.
* `playerStandings()` - Returns a list of the players and their win records, sorted by wins.
* `reportMatch(winner, loser)` - Records the outcome of a single match between two players (accepts ids.)
* `swissPairings()` - Returns a list of pairs of players for the next round of a match.

# Project contents - INCOMPLETE

# References
This project runs on code provided by the course [Intro to Relational Databases](https://www.udacity.com/course/intro-to-relational-databases--ud197-nd) at [Udacity](http://www.udacity.com)

