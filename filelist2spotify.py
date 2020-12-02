#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import logging
import logging.handlers
import random
from difflib import SequenceMatcher
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def get_args():
    p = argparse.ArgumentParser(description='A script to import tunes by band and title into Spotify')
    p.add_argument('-f', '--file', help='Path to the file with the song list', type=argparse.FileType('r', encoding='UTF-8'), required=True)
    p.add_argument('-p','--playlist',help='Playlist code',required=True)
    p.add_argument('-s', '--startat', help='Start line at this position (Default:22)', default=22)
    p.add_argument('-d', '--debug', help='Debug mode', action='store_true', default=False)
    return p.parse_args()


def load_mp3list_file(mp3list_file):
    tracks = []
    try:
        content = [ line.strip() for line in mp3list_file if line.strip() and not line.startswith("#") ]
    except Exception as e:
        logger.critical('Playlist file "%s" failed load: %s' % (mp3list_file, str(e)))
        sys.exit(1)
    else:
        for track in content:
            # This is to trim first part of each line e.g. to manage dir or attrib output
            track=track[args.startat:]
            filename = os.path.splitext(os.path.basename(track))[0]
            track_parts = filename.split(' - ')
            if len(track_parts) > 1:
                title = track_parts[1].strip()
            # We are storing the original filename for future functionality, e.g. delete those files that could be added to the spotify playlist. 
            # Filename is used for search, title is used to compare the result
            tracks.append({'path': track, 'filename' : filename, 'title' : title})
        return tracks

def find_spotify_track(track):
    spotify_match_threshold = 0.2
    search_string= track['filename']
    track_name =track['title']

    logger.debug('Searching Spotify for "%s" trying to find track called "%s"' % (search_string, track_name))
    # Perform the search
    results_raw = sp.search(q=search_string, limit=30)
    if len(results_raw['tracks']['items']) > 0:
        spotify_results = results_raw['tracks']['items']
        logger.debug('Spotify results:%s' % len(spotify_results))
        for spotify_result in spotify_results:
            # Compare the title with the original title
            spotify_result['rank'] = SequenceMatcher(None, track_name.lower(), spotify_result['name'].lower()).ratio()
            # Exact match, we are happy
            if spotify_result['rank'] == 1.0:
                return {'id': spotify_result['id'], 'title': spotify_result['name'], 'artist': spotify_result['artists'][0]['name']}
        # Sort the results based on similarity
        spotify_results_sorted = sorted(spotify_results, key=lambda k: k['rank'], reverse=True)
        # If we have result where the similarity is above the treashold, we pass this back as match
        if len(spotify_results_sorted) > 0 and spotify_results_sorted[0]['rank'] > spotify_match_threshold:
            return {'id': spotify_results_sorted[0]['id'], 'title': spotify_results_sorted[0]['name'], 'artist': spotify_results_sorted[0]['artists'][0]['name']}
    # If we are here, we were not lucky...
    logger.debug('No good Spotify result found')
    return False



def main():
    # Load file passed as -f parameter
    tracks = load_mp3list_file(args.file)
    print ("Parsed %s tracks from %s" % (len(tracks), args.file.name))
    # Search Spotify based on the filename (assuming Artist - Title)
    for track in tracks:
        # Update the track list with the Spotify data
        track['spotify_data'] = find_spotify_track(track)
    # We will only need the IDs for those tracks that we foound in Spotify
    spotify_tracks = [ k['spotify_data']['id'] for k in tracks if k.get('spotify_data') ]
    # Shuffle a the playlist
    random.shuffle(spotify_tracks)

    if len(spotify_tracks) < 1:
        print ('\nNo tracks matched on Spotify')
        sys.exit(0)

    if len(spotify_tracks) > 100:
        def chunker(seq, size):
            return (seq[pos:pos + size] for pos in range(0, len(seq), size))
        for spotify_tracks_chunk in chunker(spotify_tracks, 100):
            results=sp.playlist_add_items(args.playlist, spotify_tracks_chunk)
    else:
        results = sp.playlist_add_items(args.playlist, spotify_tracks)
    return results

if __name__ == '__main__':

    # Parse arguments
    args = get_args()

    # Setup logger
    logger = logging.getLogger(__name__)
    if args.debug:
        logging.basicConfig(level='DEBUG')
        stdout_level = logging.DEBUG
    else:
        logging.basicConfig(level='CRITICAL')
        stdout_level = logging.CRITICAL


    # Perform Spotify authentication. This is an interactive one, you will be redirected to a fake URL, copy that URL and paste when prompted
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-modify-private'))
    print("Result: %s" % main())
