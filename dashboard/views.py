# coding=utf-8

import json
import time
import calendar
import datetime

from os.path import dirname, join, realpath, getmtime

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import F, Count, Sum

from dashboard.models import Rep, Stat, Event, FunctionalArea, Goal, Metric, EventMetric

PROJECT_PATH = realpath(join(dirname(__file__), '..'))
FILE = PROJECT_PATH + '/reps.json'

def home(request):
    
    mentors = Rep.objects.filter(is_mentor=True, deleted=False).order_by('first_name')
    mentees = Rep.objects.filter(deleted=False).order_by('first_name')
    # Mentees with mentors no longer in the portal and mentors that are no longer mentors
    orphans = Rep.objects.filter(mentor=None, deleted=False).order_by('first_name')|Rep.objects.filter(mentor__is_mentor=False, deleted=False).order_by('first_name')
    empties = Rep.objects.filter(last_report_date=datetime.date(1970, 1, 1),deleted=False)
    
    selfmentor = Rep.objects.filter(mentor=F('id'), deleted=False).order_by('first_name')
    
    # Total mentees and average
    mentees_total = mentees.count()
    mentees_avg =  mentees_total / mentors.count()
    
    # Stats
    stats = Stat.objects.filter().order_by('date')
    data_updated = stats.order_by('-date')[0].date
    countries = Rep.objects.values('country').annotate(Count("id")).order_by()
    
    context = {
        'updated': data_updated,
        'mentees': mentees,
        'mentors': mentors,
        'orphans': orphans,
        'empties': empties,
        'selfmentor': selfmentor,
        'total': mentees_total,
        'average': mentees_avg,
        'stats': stats,
        'countries': countries
    }

    return render(request, 'dashboard/home.html', context)


def events(request):
    
    events = Event.objects.all()
    events_stats = [
        {
            'year': '2012',
            'count': events.filter(start__year='2012').count(),
            'mozilla': events.filter(start__year='2012', mozilla_event=True).count(),
            'non_mozilla': events.filter(start__year='2012', mozilla_event=False).count(),
        },
        {
            'year': '2013',
            'count': events.filter(start__year='2013').count(),
            'mozilla': events.filter(start__year='2013', mozilla_event=True).count(),
            'non_mozilla': events.filter(start__year='2013', mozilla_event=False).count(),
        },
        {
            'year': '2014',
            'count': events.filter(start__year='2014').count(),
            'mozilla': events.filter(start__year='2014', mozilla_event=True).count(),
            'non_mozilla': events.filter(start__year='2014', mozilla_event=False).count(),
        },
    ]
    
    # Get all event in the current year
    year_now = datetime.date.today().year
    month_now = datetime.date.today().month
    events_thisyear = events.filter(start__year=year_now)
    
    # Stats per month
    events_lastyear = []
    for month in range(1, month_now+1):
        events_lastyear.append({
            'month': calendar.month_abbr[month], 
            'total': events_thisyear.filter(start__month=month).count(),
            'fxos': events_thisyear.filter(start__month=month, categories__name='Firefox OS').count(),
            'webmaker': events_thisyear.filter(start__month=month, categories__name='Webmaker').count(),
            'recruiting': events_thisyear.filter(start__month=month, categories__name='Recruiting').count(),
            'students': events_thisyear.filter(start__month=month, categories__name='Students').count(),
            'localization': events_thisyear.filter(start__month=month, categories__name='Localization').count(),
        })

    
    areas = FunctionalArea.objects.filter().order_by('name')
    areas_stats = []
    for a in areas:
        events_count = Event.objects.filter(categories=a).count()
        areas_stats.append({
            'name': a.name,
            'count': events_count,
            'stats': [
                {
                    'year': '2012',
                    'count': Event.objects.filter(categories=a, start__year='2012').count()
                },
                {
                    'year': '2013',
                    'count': Event.objects.filter(categories=a, start__year='2013').count()
                },
                {
                    'year': '2014',
                    'count': Event.objects.filter(categories=a, start__year='2014').count()
                },
            ]
        })
        
    goals = Goal.objects.filter().order_by('name')
    goals_stats = []
    for g in goals:
        events_count = Event.objects.filter(goals=g).count()
        goals_stats.append({
            'name': g.name,
            'count': events_count,
            'stats': [
                {
                    'year': '2012',
                    'count': Event.objects.filter(goals=g, start__year='2012').count()
                },
                {
                    'year': '2013',
                    'count': Event.objects.filter(goals=g, start__year='2013').count()
                },
                {
                    'year': '2014',
                    'count': Event.objects.filter(goals=g, start__year='2014').count()
                },
            ]
        })
        
    metrics = Metric.objects.filter().order_by('name')
    
    metrics_stats = []
    for m in metrics:
        metrics_stats.append({
            'name' : m.name,
            'expected_outcome' : EventMetric.objects.filter(metric=m).aggregate(Sum('expected_outcome')),
            'outcome' : EventMetric.objects.filter(metric=m).aggregate(Sum('outcome')),
        })
    
    
    attendees = Event.objects.filter(mozilla_event=True).aggregate(Sum('estimated_attendance'))
    
    attendees_stats = [
        {
            'year': '2012',
            'count': Event.objects.filter(mozilla_event=True, start__year='2012').aggregate(Sum('estimated_attendance'))
        },
        {
            'year': '2013',
            'count': Event.objects.filter(mozilla_event=True, start__year='2013').aggregate(Sum('estimated_attendance'))
        },
        {
            'year': '2014',
            'count': Event.objects.filter(mozilla_event=True, start__year='2014').aggregate(Sum('estimated_attendance'))
        },
    ]
    
    
    countries = Event.objects.values('country').annotate(Count("id")).order_by()
    
    context = {
        'events': events,
        'events_lastyear': events_lastyear,
        'areas': areas_stats,
        'goals': goals_stats,
        'metrics': metrics_stats,
        'events_stats': events_stats,
        'attendees': attendees['estimated_attendance__sum'],
        'attendees_stats': attendees_stats,
        'countries': countries,
    }
    
    return render(request, 'dashboard/events.html', context)

    
def home_local(request):
    
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

    return render(request, 'dashboard/home-local.html', context)
