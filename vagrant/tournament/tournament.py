#!/usr/bin/env python
"""tournament module

This module is an implementation of a Swiss-system tournament
"""


import psycopg2
import random


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE results CASCADE; TRUNCATE TABLE matches CASCADE;')
    connection.commit()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE players CASCADE;')
    connection.commit()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('SELECT count(*) FROM players;')
    result = cursor.fetchone()
    connection.close()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO players (name) VALUES (%s);', [name])
    connection.commit()
    connection.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('SELECT player_id, name, wins, matches FROM v_standings;')
    result = cursor.fetchall()
    connection.close()
    return result


def reportMatch(player1, player2, outcome=1):
    """Records the outcome of a single match between two players.

    Args:
      player1: the id number of player1
      player2: the id number of player2
      outcome: the value indicating match outcome (1: player1 wins, 0: draw, -1: player2 wins)
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO matches (player1, player2) VALUES (%s, %s) RETURNING match_id;', [player1, player2])
    result = cursor.fetchone()
    match_id = result[0]

    # We use dict to translate the outcome
    switcher = {
        1: player1,
       -1: player2,
        0: None
    }

    winner = switcher.get(outcome, player1)
    
    cursor.execute('INSERT INTO results (match_id, winner) VALUES (%s, %s);', [match_id, winner])
    connection.commit()
    connection.close()
 

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('SELECT count(*) FROM v_standings WHERE matches <> 0;')
    result = cursor.fetchone()

    if result[0] > 0:
        # pairs stores pairs of individual players tuples
        pairs = []
        
        # pairings is used to convert pairs into a single tuple
        pairings = []
        
        cursor.execute('SELECT player_id, name FROM v_standings;')
        result = cursor.fetchall()
        
        if matchMaker(result, pairs):
            for pair in pairs:
                pairings.append(pair[0] + pair[1])
            connection.close()
            return pairings

    # Generate a value in python to seed postgres for randomness
    seed = random.uniform(-1.0, 1.0)

    # Seed postgres with the generated seed
    cursor.execute('SELECT setseed(%s);', [seed])

    cursor.execute('SELECT player_id, name FROM v_standings ORDER BY random();')
    result = cursor.fetchall()
    connection.close()

    # courtesy of 
    # http://stackoverflow.com/questions/756550/multiple-tuple-to-two-pair-tuple-in-python
    # http://stackoverflow.com/questions/509211/explain-pythons-slice-notation

    # We extract the ids and names from the result set
    ids, names =  zip(*result)

    # This line recombines the ids and names into pairs
    return zip(ids[::2], names[::2], ids[1::2], names[1::2]) 


def matchMaker(pool, pairs=None):
    """Recursive function that provides pairings considering rematches using Depth-First Search

    We use a modified depth-first search algorithm to find a combination that prevents rematches.

    Args:
      pool: The list of player ids to match in reverse order
      pairs: Recursively gets updated to be the final list of tuples
    
    Returns:
      A list of tuples, each of which contains (id1, id2)
        id1: the first player's unique id
        id2: the second player's unique id
    """
    if pairs is None:
        pairs = list()

    # Take the first player
    player = pool.pop(0)

    # Compare with remaining opponents in pool
    for opponent in pool:
        if not hasPlayed(player, opponent):
            # We keep track of the pairs and update the pool for deeper searches
            pairs.append([player, opponent])
            position = pool.index(opponent)
            pool.remove(opponent)

            if len(pool)==0:
                # No more players to propagate forward. Goal!
                return True
            if matchMaker(pool, pairs):
                # Reached the goal with this iterative call
                return True
            else:
                # Revert by discarding the current pair and returning the opponent to the pool 
                pool.insert(position, opponent)
                pairs.remove([player, opponent])
    
    # We are unable to find the result with this pool
    pool.insert(0, player)
    return False


def hasPlayed(player1, player2):
    """Simple query to check if two players have played before

    Args:
      player1, player2: ids of players to check in match history

    Returns:
      A boolean value which can be
        True: A match has been found between the two players
        False: No matches were found between the two players
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('SELECT count(*) FROM matches WHERE (player1=%s AND player2=%s) OR (player2=%s AND player1=%s);', 
                   [player1[0], player2[0], player1[0], player2[0]])
    result = cursor.fetchone()
    connection.close()

    if result[0]==0:
        return False
    else:
        return True
