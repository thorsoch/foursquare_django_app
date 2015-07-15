import requests
from foursquare.models import Venue, Review
from datetime import date, datetime, timedelta
from django.utils import timezone

requests.packages.urllib3.disable_warnings()

def request_description(ID):
    parameters2 = {'client_id': 'INSERT_HERE',
        'client_secret':'INSERT_HERE',
        'v': 'INSERT_HERE'}

    try:
        r = requests.get("http://api.foursquare.com/v2/venues/" + ID + "?", params=parameters2, verify = False)
        r = r.json()
        r = r['response']['venue']
    except:
        return ("", "", None, [])

    try:
        rDesc = r['description']
    except:
        rDesc = ""

    try:
        urlPre = r['photos']['groups'][0]['items'][0]['prefix']
        urlSuf = r['photos']['groups'][0]['items'][0]['suffix']
        #Can use 30x30. Defines image size.
        rPhoto = urlPre + '110x110' + urlSuf
    except:
        rPhoto = ""

    try:
        rRating = r['rating']
    except:
        rRating = None

    try:
        rRev = r['tips']['groups'][0]['items']
        rReviews = rRev
    except:
        rReviews = None

    return (rDesc, rPhoto, rRating, rReviews)

def insert_reviews(reviewsList):
    for reviews in reviewsList:
        venue_id = reviews[0]
        for review in reviews[1]:
            text, firstName, lastName = "", "", ""
            if 'text' in review:
                text = review['text']
            if 'user' in review and 'firstName' in review['user']:
                firstName = review['user']['firstName']
            if 'user' in review and 'lastName' in review['user']:
                lastName = review['user']['lastName']
            r = Review.objects.get_or_create(venue_id = venue_id,
                text = text,
                first_name = firstName,
                last_name = lastName,
                uploaded = timezone.now(),
                )[0]
            r.save()

def empty_source():
    Venue.objects.all().delete()

def clear_source(source):
    Venue.objects.filter(source = source).delete()

def edit_category(currentSuper, newSuper, newSub = None):
    target = Venue.objects.filter(super_category = currentSuper)
    for v in target:
        v.super_category = newSuper
        if newSub:
            v.sub_category = newSub
