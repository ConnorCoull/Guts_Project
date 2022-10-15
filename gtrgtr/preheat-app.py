import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Please run the following lines with the shared client ID and Key (or the Windows equivalent, whatever it may well be)
# export SPOTIPY_CLIENT_ID='your-spotify-client-id'
# export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)




def getGtrGtrObjects():
    gtrgtrGtrsUrl = "https://services.guitarguitar.co.uk/WebService/api/hackathon/guitars"
    gtrgtrSongsUrl = "https://services.guitarguitar.co.uk/WebService/api/hackathon/guitarswithsongs"
    try:
        gtrsResponse = requests.get(gtrgtrGtrsUrl)
        songsResponse = requests.get(gtrgtrSongsUrl)
    except:
        print('preheat failed at API calls')
    gtrgtrJson = gtrsResponse.json()
    gtrgtrSongsJson = songsResponse.json()
    return gtrgtrJson, gtrgtrSongsJson

def getSpotifyURL(spotifyID):
    return sp.track(spotifyID)['preview_url']
    
def consolidateGtrsAndSongs(gtrsObjects, gtrsSongsObjects):
    consolObjects = []
    finalIndex = len(gtrsObjects) - 1
    for i in range(0, finalIndex):
        finalObject = {}
        gtr = gtrsObjects[i]
        for gtrSong in gtrsSongsObjects:
            if gtr['skU_ID'] == gtrSong['skU_ID'] and (gtrSong['spotifyId'] != None and gtrSong['spotifyId'] != ""):
                trimmedSpotifyID = gtrSong['spotifyId'].split('?')[0]
                finalObject['spotifyId'] = getSpotifyURL(trimmedSpotifyID)
                break
        finalObject['itemName'] = gtr['itemName']
        finalObject['title'] = gtr['title']
        finalObject['brandName'] = gtr['brandName']
        finalObject['description'] = gtr['description']
        finalObject['salesPrice'] = gtr['salesPrice']
        finalObject['pictureMain'] = gtr['pictureMain']
        finalObject['qtyInStock'] = gtr['qtyInStock']
        finalObject['qtyOnOrder'] = gtr['qtyOnOrder']
        finalObject['colour'] = gtr['colour']
        finalObject['pickup'] = gtr['pickup']
        finalObject['bodyShape'] = gtr['bodyShape']
        finalObject['online'] = gtr['online']
        consolObjects.append(finalObject)
    return consolObjects

    
if __name__ == "__main__":
    gtrgtrJSON, gtrSongsJSON = getGtrGtrObjects()
    consolidatedJSON = consolidateGtrsAndSongs(gtrgtrJSON, gtrSongsJSON)
