"""tournament module

This module attempts to provide all the tools necessary to track a Swiss-Style tournament.
"""

import psycopg2
import random

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament_step1")


def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""TRUNCATE TABLE results CASCADE; TRUNCATE TABLE matches CASCADE;""")
    connection.commit()
    connection.close()

def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""TRUNCATE TABLE players CASCADE;""")
    connection.commit()
    connection.close()

def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""SELECT count(*) FROM players;""")
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
    cursor.execute("""INSERT INTO players (name) VALUES (%s);""", [name])
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
    cursor.execute("""SELECT player_id, name, wins, matches FROM v_standings;""")
    result = cursor.fetchall()
    connection.close()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO matches (player1, player2) VALUES (%s, %s) RETURNING match_id;""", [winner, loser])
    result = cursor.fetchone()
    match_id = result[0]
    cursor.execute("""INSERT INTO results (match_id, winner) VALUES (%s, %s);""", [match_id, winner])
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
    cursor.execute("""SELECT count(*) FROM v_standings WHERE matches <> 0;""")
    result = cursor.fetchone()
    connection.close()   
 
    if result[0]==0:
        seed = random.uniform(-1.0, 1.0)
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""SELECT setseed(%s);""", [seed])
        cursor.execute("""SELECT player_id, name FROM v_standings ORDER BY random();""")
        result = cursor.fetchall()
        connection.close()
    else:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""SELECT player_id, name FROM v_standings ORDER BY wins;""") 
        result = cursor.fetchall()
        connection.close()

    # courtesy of 
    # http://stackoverflow.com/questions/756550/multiple-tuple-to-two-pair-tuple-in-python
    # http://stackoverflow.com/questions/509211/explain-pythons-slice-notation
    ids, names =  zip(*result)
    return zip(ids[::2], names[::2], ids[1::2], names[1::2]) 

