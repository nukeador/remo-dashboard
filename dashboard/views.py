# coding=utf-8

import json
import time

from os.path import dirname, join, realpath, getmtime

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import F, Count

from dashboard.models import Rep, Stat

PROJECT_PATH = realpath(join(dirname(__file__), '..'))
FILE = PROJECT_PATH + '/reps.json'

# Create your views here.

def home(request):
    
    entries = []

    response = open(FILE)
    data = json.load(response)
    data_updated = time.ctime(getmtime(FILE))
    
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
                        'avatar': mentee['profile']['avatar_url'],
                        'country': mentee['profile']['country'],
                    })
            
            mentors.append({
                'name': rep['fullname'],
                'url': rep['profile']['profile_url'],
                'avatar': rep['profile']['avatar_url'],
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
            
            # If mentor was deleted (not in the current Reps list)
            if not any(rep_mentor in rep['resource_uri'] for rep in data['objects']):
                orphans.append({
                    'name': rep['fullname'],
                    'url': rep['profile']['profile_url'],
                    'mentor': 'No longer in the program'
                })
                    
            # If mentor is no longer a mentor
            for mentor in data['objects']:
                if mentor['resource_uri'] == rep_mentor and not mentor['profile']['is_mentor']:
                    orphans.append({
                        'name': rep['fullname'],
                        'url': rep['profile']['profile_url'],
                        'mentor': mentor['fullname']
                    })
    
    # Total mentees and average
    mentees_total = len(data['objects'])
    mentees_avg =  mentees_total / len(mentors)
    
    context = {
        'updated': data_updated,
        'mentors': mentors,
        'orphans': orphans,
        'selfmentor': selfmentor,
        'total': mentees_total,
        'average': mentees_avg
    }

    return render(request, 'dashboard/home.html', context)

def home2(request):
    
    entries = []

    response = open(FILE)
    data_updated = time.ctime(getmtime(FILE))
    
    mentors = Rep.objects.filter(is_mentor=True, deleted=False).order_by('first_name')
    mentees = Rep.objects.filter(deleted=False).order_by('first_name')
    orphans = Rep.objects.filter(mentor=None, deleted=False).order_by('first_name')
    
    # FIXME: Query for mentors that are no longer mentors
    selfmentor = Rep.objects.filter(mentor=F('id'), deleted=False).order_by('first_name')
    
    # Total mentees and average
    mentees_total = mentees.count()
    mentees_avg =  mentees_total / mentors.count()
    
    # Stats
    stats = Stat.objects.filter().order_by('date')
    countries = Rep.objects.values('country').annotate(Count("id")).order_by()
    
    context = {
        'updated': data_updated,
        'mentors': mentors,
        'orphans': orphans,
        'selfmentor': selfmentor,
        'total': mentees_total,
        'average': mentees_avg,
        'stats': stats,
        'countries': countries
    }

    return render(request, 'dashboard/home2.html', context)
