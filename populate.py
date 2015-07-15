import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'INSERT_HERE')

import django
django.setup()

from foursquare.models import Venue, Review
import requests
import json
from django.utils import timezone
from tools import request_description, insert_reviews

requests.packages.urllib3.disable_warnings()

parameters = {
        'client_id': 'INSERT_HERE',
        'client_secret':'INSERT_HERE',
        'v': 'INSERT_HERE',
        'll': 'INSERT_HERE',
        'categoryId': 'INSERT_HERE',
        'limit': 20
        }

categories= {
                # Example:'4d4b7104d754a06370d81259':'Arts&Entertainment',
            }

def populate():
    jsonDict = {}

    for categoryID in categories:
        parameters['categoryId'] = categoryID
        r = requests.get("http://api.foursquare.com/v2/venues/search?", params=parameters, verify = False).json()
        jsonDict[categories[categoryID]] = r

    reviews = []

    for superCategory, venueJson in jsonDict.items():
        for venue in venueJson['response']['venues']:
            uniqueID = venue['id']
            if Venue.objects.filter(unique_id = uniqueID).exists():
                review = update_venue(venue) # returns tuple (review json, id in table)
            else:
                review = add_venue(venue, superCategory) # returns tuple (review json, id in table)
            reviews += [review]

    insert_reviews(reviews)


def add_venue(venue, superCategory):
    details = request_description(venue['id'])

    address, url, subCategory = None, None, None
    if 'address' in venue['location']:
        address = venue['location']['address']
    if 'url' in venue:
        url = venue['url']
    if venue['categories'] != []:
        subCategory = venue['categories'][0]['name']

    v = Venue.objects.get_or_create(name = venue['name'],
        description = details[0],
        default_image = details[1],
        coordinate = str(venue['location']['lat']) + "," + str(venue['location']['lng']),
        raw_data = str(venue),
        source = "Foursquare",
        unique_id = venue['id'],
        created_at = timezone.now(),
        updated_at = timezone.now(),
        url = url,
        address = address,
        super_category = superCategory,
        sub_category = subCategory,
        rating = details[2],
        review = str(details[3]),
        )[0]
    v.save()

    return (v.id, details[3])

def update_venue(venue):
    details = request_description(venue['id'])

    target = Venue.objects.filter(unique_id = venue['id'])[0]
    target.raw_data = str(venue)
    target.rating = details[2]
    target.review = str(details[3])
    target.updated_at = timezone.now()

    Review.objects.filter(venue_id = target.id).delete() # delete old reviews

    return (target.id, details[3])

if __name__ == '__main__':
    populate()