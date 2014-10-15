# coding=utf-8

import requests
import json

from os.path import dirname, join, realpath

from django.http import HttpResponse
from django.shortcuts import render

PROJECT_PATH = realpath(join(dirname(__file__), '..'))

BASE_URL = 'https://reps.mozilla.org'
URL = '/api/v1/rep/?format=json&limit=0'
FILE = PROJECT_PATH + '/reps.json'
# Define if we want to fetch remote data, if not, local FILE
# will be used
REMOTE = False

# Create your views here.

def home(request):
    
    entries = []
    new_url = URL
    
    if REMOTE:
        response = requests.get(BASE_URL + new_url, verify=False)
        
        if not response.status_code == 200:
            raise ValueError('Invalid Response')

        data = response.json()
    else:
        response = open(FILE)
        data = json.load(response)
    
    mentors = []
    orphans = []
    selfmentor = []
    
    for rep in data['objects']:
        is_mentor = rep['profile']['is_mentor']
        rep_id = rep['resource_uri']
        rep_mentor = rep['profile']['mentor']
        
        if is_mentor:
            # Get mentees
            mentees = []
            for mentee in data['objects']:
                if mentee['profile']['mentor'] == rep_id:
                    mentees.append({
                        'name': mentee['fullname'],
                        'url': mentee['profile']['profile_url'],
                    })
            
            mentors.append({
                'name': rep['fullname'],
                'url': rep['profile']['profile_url'],
                'mentees': mentees
                })
            
            # Check who is mentor of himself
            if rep_id == rep_mentor:
                selfmentor.append({
                    'name': rep['fullname'],
                    'url': rep['profile']['profile_url'],
                })

        else:
            # Check if his mentor is a mentor
            for mentor in data['objects']:
                if mentor['resource_uri'] == rep_mentor and not mentor['profile']['is_mentor']:
                    orphans.append({
                        'name': rep['fullname'],
                        'url': rep['profile']['profile_url'],
                        'mentor': mentor['fullname']
                    })
    
    context = {'mentors': mentors, 'orphans': orphans, 'selfmentor': selfmentor}
    return render(request, 'dashboard/home.html', context)
