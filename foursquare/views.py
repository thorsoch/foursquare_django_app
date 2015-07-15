from django.shortcuts import render
from foursquare.models import Venue, Mailgun
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):

    venue_list = Venue.objects.order_by('id')
    context_dict = {'venues': venue_list}

    return render(request, 'foursquare/index.html', context_dict)