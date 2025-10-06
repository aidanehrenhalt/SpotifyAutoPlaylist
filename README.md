# SpotifyAutoPlaylist
Generate Spotify playlists from Liked Songs and generating playlists by Genre (Possibility of extending the functionalities further at a later date)

## Inputs & Scope
-- Input Format:
--- Genres: CSV, JSON, txt?
--- Pull songs from Liked Songs via Spotify API, filter into Playlist(s)
--- Maybe add a list feature where you can make a playlist from a list of songs provided Title + Artists is contained.

## Stack
-- Spotipy or Spotify Web API Node (Node.js)
-- Store secrets local in .env

## Register a Spotify App & Spotify Auth
-- via Spotify Dashboard
-- Figure out Auth Flow
-- Token Storage / Refresh Token Handling

## Handling Data from Spotify API
-- Search API if implementing list of songs (instead of pulling from Liked Songs)

## Fetch Metadata to Assist with Genres
-- Ensure limit rates are respected (batch requests)

## Genre Mapping Strategy
-- TBD

## Playlist Naming Scheme
-- TBD

## API Limitations
-- TBD - Need to Research

## Edge Cases
-- Collaboration / Features - Multiple Artists, Conflicting Genres, etc.
-- Regional Availability (Shouldn't be too much of a concern)

# App Configuration:
-- Setup environmental variables in root dir within .env
-- NOTE: Ensure .env is added to .gitignore
-- `pip freeze > requirements.txt` -- Create a `requirements.txt` file with all current packages
-- `pip install -r requirements.txt` -- Install all packages listed in `requirements.txt`
