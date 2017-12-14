#!/usr/bin/env python

from googleplaces import GooglePlaces
from geopy.geocoders import GoogleV3
import json


def update_dict(places, place):
    if place.name not in places:
        places[place.name] = {
                'website': place.website,
                'telephone': place.local_phone_number,
                'url': place.url
                }
    return places


API_KEY_FILE = './API_key/api_key.txt'
METERS_TO_LATITUDE = 110.574

f = open(API_KEY_FILE)
api_key = f.read()

google_places = GooglePlaces(api_key)
geocoder = GoogleV3(api_key.strip())

latitude = 0
longitude = 0
while not latitude:
    try:
        q_string = 'Please input the latitude start:\n'
        latitude = int(input(q_string))
        latitude = latitude
    except Exception as e:
        print(e)
        print('Please enter a valid number')

while not longitude:
    try:
        q_string = 'Please input the longitude of the start:\n'
        longitude = int(input(q_string))
        longitude = longitude
    except Exception as e:
        print(e)
        print('Please enter a valid number')

radius = ""
while not radius:
    try:
        q_string = 'Please input the radius of the search (kilometers):\n'
        radius = int(input(q_string))
        radius = radius
    except Exception as e:
        print(e)
        print('Please enter a valid number')
        radius = ""

print('Searching...')
places_with_websites = {}

coords = {
        'lat': latitude,
        'lng': longitude
        }
print(coords)

for x in range(0, 3):
    query_result = google_places.nearby_search(
            lat_lng=coords,
            keyword='Construction',
            radius=radius*1000)
    for place in query_result.places:
        # gets website if there is one
        place.get_details()
        if(place.website is not None):
            places_with_websites = update_dict(places_with_websites, place)

    latitude = (latitude + radius / METERS_TO_LATITUDE)
    coords['lat'] = latitude
    coords['lng'] = longitude
    print("Finished pass {0}".format(x+1))


# You may prefer to use the text_search API, instead.
# If types param contains only 1 item the request to Google Places API
# will be send as type param to fullfil:
# http://googlegeodevelopers.blogspot.com.au/2016/02/changes-and-quality-improvements-in_16.html
with open('mapsdata.json', 'w') as f:  # Just use 'w' mode in 3.x
    f.write(json.dumps(places_with_websites))

"""
    # The following method has to make a further API call.
    place.get_details()
    # Referencing any of the attributes below, prior to making a call to
    # get_details() will raise a googleplaces.GooglePlacesAttributeError.
    print(place.details)  # A dict matching the JSON response from Google.
    print(place.local_phone_number)
    print(place.international_phone_number)
    print(place.website)
    print(place.url)

    # Getting place photos

    for photo in place.photos:
        # 'maxheight' or 'maxwidth' is required
        photo.get(maxheight=500, maxwidth=500)
        # MIME-type, e.g. 'image/jpeg'
        photo.mimetype
        # Image URL
        photo.url
        # Original filename (optional)
        photo.filename
        # Raw image data
        photo.data

# Are there any additional pages of results?
if query_result.has_next_page_token:
    query_result_next_page = google_places.nearby_search(
            pagetoken=query_result.next_page_token)


# Adding and deleting a place
try:
    added_place = google_places.add_place(name='Mom and Pop local store',
            lat_lng={'lat': 51.501984, 'lng': -0.141792},
            accuracy=100,
            types=types.TYPE_HOME_GOODS_STORE,
            language=lang.ENGLISH_GREAT_BRITAIN)
    print(added_place.place_id)  # The Google Places identifier - Important!
    print(added_place.id)

    # Delete the place that you've just added.
    google_places.delete_place(added_place.place_id)
except GooglePlacesError as error_detail:
    # You've passed in parameter values that the Places API doesn't like..
    print(error_detail)
    """
