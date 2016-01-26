-- Table definitions for the tournament project.
--
-- Tables:
-- * players: Contains the players participating in the tournament
-- * matches: Contains a register of the matches that players have participated in
-- * results: Contains the results of matches that have been played
--
-- Views:
-- * v_simple_standings: Simple standings view at best includes match-win percentage
-- * v_standings: Uses v_simple_standings to compute Opponent Match Wins (OMW) value

CREATE DATABASE tournament;

\connect tournament

CREATE TABLE players (
  player_id serial primary key not null,
  name text not null
);

CREATE TABLE matches (
  match_id serial primary key not null,
  player1 integer references players(player_id),
  player2 integer references players(player_id)
);

CREATE TABLE results (
  result_id serial primary key not null,
  match_id integer references matches,
  winner integer references players(player_id)
);

CREATE VIEW v_simple_standings AS
SELECT
 P.player_id,
 P.name,
 SUM(CASE WHEN P.player_id = R.winner THEN 1 ELSE 0 END) AS wins,
 SUM(CASE WHEN P.player_id = M.player1 OR P.player_id = M.player2 THEN 1 ELSE 0 END) AS matches,
 CASE WHEN 
  SUM(CASE WHEN P.player_id = M.player1 OR P.player_id = M.player2 THEN 1 ELSE 0 END) = 0
 THEN 0.00
 ELSE
  ROUND(
   1.0 *
    SUM(CASE WHEN P.player_id = R.winner THEN 1 ELSE 0 END) /
    SUM(CASE WHEN P.player_id = M.player1 OR P.player_id = M.player2 THEN 1 ELSE 0 END),
   2
  )
 END AS match_wins
FROM
 players AS P
 LEFT JOIN matches AS M
  ON P.player_id = M.player1
  OR P.player_id = M.player2
 LEFT JOIN results AS R
  ON M.match_id = R.match_id
GROUP BY
 P.player_id, P.name
ORDER BY
 wins DESC, matches;

CREATE VIEW v_standings AS
SELECT
 P.player_id,
 P.name,
 P.wins,
 P.matches,
 P.match_wins,
 ROUND(
  1.0 *
   (
    -- Numerator is the SUM of opponents's match_wins
    SELECT 
     SUM(S.match_wins) 
    FROM v_simple_standings AS S 
    LEFT JOIN matches AS M1 
     ON S.player_id = M1.player1 
    LEFT JOIN matches AS M2 
     ON S.player_id = M2.player2 
    WHERE 
     M1.player2=P.player_id OR M2.player1=P.player_id
   ) /
   (
    -- Denominator is the COUNT of opponents
    SELECT
     COUNT(*)
    FROM v_simple_standings AS S
    LEFT JOIN matches AS M1 
     ON S.player_id = M1.player1 
    LEFT JOIN matches AS M2 
     ON S.player_id = M2.player2 
    WHERE 
     M1.player2=P.player_id OR M2.player1=P.player_id
    ),
   2
  ) AS opponent_match_wins
FROM
 v_simple_standings AS P
GROUP BY
 P.player_id, P.name, P.wins, P.matches, P.match_wins
ORDER BY
 P.wins DESC, opponent_match_wins DESC, P.matches;
