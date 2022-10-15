import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Please run the following lines with the shared client ID and Key (or the Windows equivalent, whatever it may well be)
# export SPOTIPY_CLIENT_ID='your-spotify-client-id'
# export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)


bodyShapes = {
    1: 'SStyle',
    2: 'TStyle',
    3: 'DoubleCut',
    4: 'Offset',
    5: 'HollowBody',
    6: 'VStyle',
    7: 'SmallBody',
    8: 'Orchestral',
    9: 'Dreadnought',
    10: 'Grand Auditorium',
    11: 'Jumbo',
    12: 'Explorer',
    13: 'SingleCut',
    14: 'Combo',
    15: 'Head',
    16: 'Cabinet',
}

colour = {
    1: 'Red',
    2: 'Orange',
    3: 'Yellow',
    4: 'Green',
    5: 'Blue',
    6: 'Purple',
    7: 'Pink',
    8: 'Brown',
    9: 'Gold',
    10: 'Silver',
    11: 'Grey',
    12: 'Black',
    13: 'White',
    14: 'Natural',
    15: 'Multicolour',
}

pickup = {
    1: 'ElectroAcoustic',
    2: 'SS',
    3: 'SSS',
    4: 'HH',
    5: 'HHH',
    6: 'HS',
    7: 'HSS',
    8: 'HSH',
    9: 'P90',
    10: 'S',
    11: 'H'
}

category = {
    'GU': 'Guitars',
    'GUAG': 'Acoustics',
    'GUAGCC_1': 'Classical Guitar',
    'GUAGCC_lh': 'Left Handed Classicals',
    'GUBA': 'Basses',
    'GUEG': 'Electrics',
    'GUAG_1': '6 String Acoustics',
    'GUAG_2': '12 String Acoustics',
    'GUAG_BG': 'Beginners',
    'GUAG_lh': 'Left handed Acoustics',
    'GUBA_1': 'Solid Body Basses',
    'GUBA_14': '4 String Basses',
    'GUBA_15': '5 String Basses',
    'GUBA_16': '6 String Basses',
    'GUBA_2': 'Acoustic Basses',
    'GUBA_3': 'Fretless Basses',
    'GUBA_BG': 'Beginners',
    'GUBA_lh': 'Left handed Basses',
    'GUBASS': 'Short Scale Basses',
    'GUEG_1': 'Solid Body Electrics',
    'GUEG_2': 'Semi Acoustic Electrics',
    'GUEG_34': '3/4 Sized',
    'GUEG_7': '7 String Electrics',
    'GUEG_8': '8 String Electrics',
    'GUEG_BG': 'Beginners',
    'GUEG_lh': 'Left Handed Electrics'
}


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
    for gtr in gtrsObjects:
        finalObject = {}
        for gtrSong in gtrsSongsObjects:
            if gtr['skU_ID'] == gtrSong['skU_ID'] and (gtrSong['spotifyId'] != None and gtrSong['spotifyId'] != ""):
                trimmedSpotifyID = gtrSong['spotifyId'].split('?')[0]
                finalObject['spotifyId'] = getSpotifyURL(trimmedSpotifyID)
                break
        finalObject['itemName'] = gtr['itemName']
        finalObject['title'] = gtr['title']
        finalObject['category'] = gtr['category']
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


def enumEnricher(consolObjects):
    newObjects = []
    for guitar in consolObjects:
        print(guitar)
        currentBodyShape = guitar['bodyShape']
        currentColour = guitar['colour']
        currentPickup = guitar['pickup']
        currentCategory = guitar['category']
        guitar['bodyShape'] = bodyShapes[currentBodyShape]
        guitar['colour'] = colour[currentColour]
        guitar['pickup'] = pickup[currentPickup]
        guitar['category'] = category[currentCategory]
        newObjects.append(guitar)
        print(guitar)
    return newObjects


if __name__ == "__main__":
    # gtrgtrJSON, gtrSongsJSON = getGtrGtrObjects()
    gtrgtrJSON = [{
        'skU_ID': "12050912030058",
        'asn': "885978519156",
        'category': "GUAG_1",
        'online': True,
        'itemName':	"G5013CE Rancher Junior",
        'title': "",
        'brandName': "Gretsch",
        'description': "",
        'productDetail': "<p>Gretsch presents a darkly alluring take on its classic acoustic model with the G5013CE Rancher™ Jr. With its slick, elegant appointments and onboard electronics, it's a cool and classic performer with a distinctive Gretsch personality all its own.</p>\r\n\r\n",
        'salesPrice': 349,
        'pictureMain': "https://images.guitarguitar.co.uk/cdn/large/160/12050912030058f.jpg",
        'qtyInStock': 1,
        'qtyOnOrder': 0,
        'colour': 1,
        'pickup': 1,
        'bodyShape': 8,
        'createdOn': "2022-10-01T14:38:01.9194045+01:00"}]
    gtrSongsJSON = [{'skU_ID': "12050912030058",
                    'spotifyId': "08mG3Y1vljYA6bvDt4Wqkj?si=fd4b4b4efce64148"}]
    consolidatedJSON = consolidateGtrsAndSongs(gtrgtrJSON, gtrSongsJSON)
    print(enumEnricher(consolidatedJSON))
