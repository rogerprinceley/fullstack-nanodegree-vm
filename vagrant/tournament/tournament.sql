-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

\connect tournament

CREATE TABLE players (
  player_id serial primary key not null,
  name text not null
);

--CREATE TABLE tournaments (
--  tournament_id serial primary key not null,
--  name text not null
--);

CREATE TABLE matches (
  match_id serial primary key not null,
--  tournament_id integer references tournaments,
  player1 integer references players(player_id),
  player2 integer references players(player_id)
);

CREATE TABLE results (
  result_id serial primary key not null,
  match_id integer references matches,
  winner integer references players(player_id)
);
	
