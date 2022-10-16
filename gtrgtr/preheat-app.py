from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from os import environ
import django
import requests
environ['DJANGO_SETTINGS_MODULE'] = 'gtrgtr.settings'
django.setup()

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
        finalObject['spotifyId'] = None
        for gtrSong in gtrsSongsObjects:
            if gtr['skU_ID'] == gtrSong['skU_ID']:
                finalObject['spotifyId'] = gtrSong['spotifyId'].split('?')[0]
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
        currentBodyShape = guitar['bodyShape']
        currentColour = guitar['colour']
        currentPickup = guitar['pickup']
        currentCategory = guitar['category']
        guitar['bodyShape'] = bodyShapes[currentBodyShape]
        guitar['colour'] = colour[currentColour]
        guitar['pickup'] = pickup[currentPickup]
        guitar['category'] = category[currentCategory]
        newObjects.append(guitar)
    return newObjects


def databaseDumper(guitarObjects):
    for guitar in guitarObjects:
        if guitar['spotifyId'] != None and guitar['spotifyId'] != '':
            g = Guitars.objects.get_or_create(itemName=guitar['itemName'], title=guitar['title'], category=guitar['category'], brandName=guitar['brandName'],
                                              description=guitar['description'], salesPrice=guitar['salesPrice'],
                                              pictureMain=guitar['pictureMain'],
                                              qtyInStock=guitar['qtyInStock'], qtyOnOrder=guitar[
                'qtyOnOrder'], colour=guitar['colour'],
                pickup=guitar['pickup'], bodyShape=guitar['bodyShape'],
                online=guitar['online'], spotifyPreviewURL=guitar['spotifyId'])[0]
        else:
            g = Guitars.objects.get_or_create(itemName=guitar['itemName'], title=guitar['title'], category=guitar['category'], brandName=guitar['brandName'],
                                              description=guitar['description'], salesPrice=guitar['salesPrice'],
                                              pictureMain=guitar['pictureMain'],
                                              qtyInStock=guitar['qtyInStock'], qtyOnOrder=guitar[
                'qtyOnOrder'], colour=guitar['colour'],
                pickup=guitar['pickup'], bodyShape=guitar['bodyShape'],
                online=guitar['online'])[0]
        g.save()
        print(guitar['itemName'] + "added to database")


if __name__ == "__main__":
    from gtrgtrapp.models import Guitars
    gtrgtrJSON, gtrSongsJSON = getGtrGtrObjects()
    consolidatedJSON = consolidateGtrsAndSongs(gtrgtrJSON, gtrSongsJSON)
    enrichedJSON = enumEnricher(consolidatedJSON)
    databaseDumper(enrichedJSON)
