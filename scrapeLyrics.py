from ast import IsNot
from codecs import escape_encode
import time
from bs4 import BeautifulSoup
import requests
import re
import tekore as tk
import unidecode
import os

# SPOTIFY_ACCESS_TOKEN = 'BQBy_jco2WKqTtufDKmKsBpQYsCbwNbXbXqipI_Hr_QiqRYjsTh2uZ5wRW_rIfM6W3RqVTtTQOWtGsfCq6jGIgg0C27TVMFSl5M71ixtNbnvEg_qAsplR0M7fkYsnwzlc9U8T1NI2He9hJ337au2VQkbtMOnt_Rh8quX1gmLfxHK4aOtyxSRwRa23_BHWAE'

# Comment out codes in getCurrentInfo() and copy and paste the following code into the function
# Run the program, accept the pop window and copy and paste the redirect link in command window
# delete the code in getCurrentInfo and uncomment the original code 
# setup the cfg file for the first time

'''
client_id = 'ENTER YOUR CLIENT ID'
client_secret = 'ENTER YOUR CLIENT SECRET'
redirect_uri = 'https://example.com/callback'

user_token = tk.prompt_for_user_token(
    client_id,
    client_secret,
    redirect_uri,
    scope=tk.scope.every
)

spotify = tk.Spotify(user_token)

conf = (client_id, client_secret, redirect_uri, user_token.refresh_token)
tk.config_to_file('tekore.cfg', conf)

'''
def getCurrentInfo(lastSong):

    # initialise the client

    conf = tk.config_from_file('tekore.cfg', return_refresh=True)
    user_token = tk.refresh_user_token(*conf[:2], conf[3])
    spotify = tk.Spotify(user_token)

    songName = spotify.playback_currently_playing(None, True).item.name

    artistList = spotify.playback_currently_playing(None, True).item.artists

    artistName = ','.join(artist.name.replace(',','') for artist in artistList)

    if lastSong != songName:

        os.system('CLS')

        try:
            print(unidecode.unidecode(songName) + ' - ' + unidecode.unidecode(artistName) + '\n')
        except:
            print('Song name or artist name contains special character')

        getGeniusURL(artistName, songName)

    return songName


def getGeniusURL(songArtists, songName): 
    url = 'https://genius.com/'
    mObject = re.search(r'\s?\(feat\.?\s*(.*?)\)',songName)

    if mObject:
        try:
            nameMObject = re.search('.'+mObject[1].lower(),songArtists.lower())
            songArtists = songArtists.lower().replace(nameMObject[0].lower(),'')
            songName = songName.replace(mObject[0],'')
        except:
            print('irregular pattern for feature artists')

    songName = re.sub(r'\s?-.*','',songName)

    url = url + standardizeString(songArtists,'songArtists') + '-'
    url= url+ standardizeString(songName, 'songName')+'-lyrics'
    ScrapeLyrics(url)
    
    
def standardizeString(s,type):
    sdString = unidecode.unidecode(s)
    sdString = sdString.lower()
    sdString = re.sub('\s','-',sdString)
    sdString = re.sub('[()\'.!?%]','',sdString)
    sdString = re.sub('&','and',sdString)
    # sdString = re.sub(r'[^\x00-\x7f]','',sdString)

    if type == 'songArtists':
        sdString = sdString.capitalize()
        sdString = re.sub(',','-and-',sdString)
    if type == 'songName':
        sdString = re.sub('[,]','',sdString)
    return sdString

# Directly calls Spotify API to receive and parse the JSON object into song name and artist name
# Extremely low rate limit
'''
def getCurrentTrack(token):
    currentTrack = requests.get(
        'https://api.spotify.com/v1/me/player',
        headers={
            "Authorization" : f"Bearer {token}"
        }
    )

    # Parse JSON and returns a JSON with desired information
    SpotResponse =  currentTrack.json()

    pprint(SpotResponse, indent = 4)
    trackID = SpotResponse['item']['id']

    
    trackName = SpotResponse['item']['name']
    trackLink =  SpotResponse['item']['external_urls']['spotify']

    artistList = [artist for artist in SpotResponse['item']['artists']]
    trackArtists = ','.join([artist['name'] for artist in artistList])

    TrackInfo = {
        "id" : trackID,
        "name" : trackName,
        "artists" : trackArtists,
        "link" : trackLink
    }

    return TrackInfo
'''


def ScrapeLyrics(url): 

    source = requests.get(url).text


    soup = BeautifulSoup(source, 'html.parser')

    # print(soup.encode("utf-8"))

    try:
        songLyrics = soup.select_one('div[class^="Lyrics__Container"], .song_body-lyrics p').get_text(separator="\n")
        # songLyrics = re.sub(u'\u2005','', songLyrics)
        songLyrics = re.sub(r'\[.*?\]', '', songLyrics).strip()
        print(unidecode.unidecode(songLyrics))
    except:
        print('Cannot find lyrics for this song')



def main():

    currentSong = getCurrentInfo('')

    while True:
        currentSong = getCurrentInfo(currentSong)
        # input('Press ENTER to exit') 
        time.sleep(1)


if __name__ == '__main__':
    main()