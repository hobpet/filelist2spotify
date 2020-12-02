# Spotify playlist from a file list

A python script to create a Spotify playlist from a list of music files (eg. mp3)

## How to use

1. [Create a list of music files](#create-a-list-of-music-files)
1. [Create a Spotify playlist](#create-a-spotify-playlist)
1. [Run the script](#run-the-script)

### Create a list of music files

If you have your files on a PC or on a shared drive that is accessibble from your PC, the easiest is to use the [```attrib```](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/attrib) command, but you can also use and exising or [create a new m3u file](https://www.google.com/search?q=create+m3u+file).

To create a list of files from a NAS server folder, simple run the following command:

 ```attrib \\192.168.0.123\radio\*.* /S >> songlist.txt```

This will create a file like this:
 
```
A                    \\192.168.0.123\radio\d\DEBORAH COX - PLAY YOUR PART.mp3
A                    \\192.168.0.123\radio\d\DIANA ROSS - THE BOSS.mp3
A                    \\192.168.0.123\radio\d\DAS EFX - NO DIGGEDY.mp3
A                    \\192.168.0.123\radio\d\DANITY KANE - RIDE FOR YOU.mp3
A                    \\192.168.0.123\radio\d\DIANA KING - WIND YU WAIST.mp3
A                    \\192.168.0.123\radio\d\DE LA SOUL - RING RING RING.mp3
A                    \\192.168.0.123\radio\d\DE LA SOUL - ME MYSELF AND I.mp3
A                    \\192.168.0.123\radio\d\DEODATO - UNCLE FUNK.mp3
A                    \\192.168.0.123\radio\d\DARREL BELL - CARELESS WHISPER.mp3
A                    \\192.168.0.123\radio\d\DAVID SOUL - SILVER LADY.mp3
A                    \\192.168.0.123\radio\d\DEBORAH COX - LIKE I DID.mp3
A                    \\192.168.0.123\radio\d\DAZZ BAND - SHAKE IT UP.mp3
```
> [!NOTE]
> The filename is expected to be in ```BANDNAME - SONG``` format, extensions are ignored.

### Create a Spotify playlist

Choose an exising playlist or [create a new one](https://support.spotify.com/us/article/create-a-playlist/)

Copy the [Spotify Code/URI](https://support.spotify.com/us/article/sharing-music/) of the selected/created playlist. It looks like this: ```spotify:playlist:7j5qpqsNRK6wW42YMPcw7A``` You will need this as a parameter of the script

### Run the script
```
$./filelist2spotify.py -h
or
python filelist2spotify.py -h

A script to import tunes by band and title into Spotify

Arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to the file with the song list
  -p PLAYLIST, --playlist PLAYLIST
                        Spotift playlist code
  -s STARTAT, --startat STARTAT
                        Start line at this position (Default:22)
  -d, --debug           Debug mode
```

e.g. to import the sample file above to the ```spotify:playlist:7j5qpqsNRK6wW42YMPcw7A``` playlist, use this command
 
```python filelist2spotify.py -f songlist.txt -p spotify:playlist:7j5qpqsNRK6wW42YMPcw7A```

## Installation and requirements

The script uses [Spotypy](https://spotipy.readthedocs.io/) library.

To install this python module run this command:

```
pip install -r requirements.txt
```

To authenticate yourself you need to login through the OAuth interface of Spotify. You need to register an app to get access to the Spotify API:

https://developer.spotify.com/my-applications/#!/

The Redirect URI doesn't need to be valid, it can be a non-existant domain, e.g. ```https://copy.this.url:123```, after authentication this URL will appear 



Export Spotify related environment variables from your new registered app:

**Linux**
```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```

**Windows**
```
set SPOTIPY_CLIENT_ID='your-spotify-client-id'
set SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
set SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```

## Acknowledgements

https://github.com/FutureSharks/spotify-m3u-import