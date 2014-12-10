import datetime
import requests
import json


from os.path import dirname, join, realpath

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from dashboard.models import Rep, Stat, Event, FunctionalArea, Goal, Metric, EventMetric

PROJECT_PATH = realpath(join(dirname(__file__), '../../../'))

BASE_URL = 'https://reps.mozilla.org'
URL = '/api/v1/rep/?format=json&limit=0'
URL_EVENTS = '/api/v1/event/?format=json&limit=0'


class Command(BaseCommand):
    args = '<init_mentors updte>'
    help = 'Fetch json data from Reps API'

    def handle(self, *args, **options):
        
        if 'init_mentors' in args:
            
            response = requests.get(BASE_URL + URL, verify=False)
        
            if not response.status_code == 200:
                raise CommandError('Invalid Response')

            data = response.json()
            
            # Create mentors
            
            for d in data['objects']:
                
                # If datetime is None, set it to 1970 to track it
                if d['profile']['last_report_date'] is None:
                    last_report_date = datetime.date(1970, 1, 1)
                else:
                    last_report_date =  datetime.datetime.strptime(d['profile']['last_report_date'], '%Y-%m-%d').date()
                
                if d['profile']['is_mentor']:
                    try:
                        # If it's already on the database, update data
                        r = Rep.objects.get(uri=d['resource_uri'], deleted=False)
                        
                        r.first_name = d['first_name']
                        r.last_name = d['last_name']
                        r.is_mentor = d['profile']['is_mentor']
                        r.is_council = d['profile']['is_council']
                        r.avatar_url = d['profile']['avatar_url']
                        r.profile_url = d['profile']['profile_url']
                        r.country = d['profile']['country']
                        r.city = d['profile']['city']
                        r.last_report_date = last_report_date
                        r.updated_date = timezone.now()
                        
                        r.save()
                    except Rep.DoesNotExist:
                        # If it's not on the database we create it
                        r = Rep(
                            uri = d['resource_uri'],
                            first_name = d['first_name'],
                            last_name = d['last_name'],
                            is_mentor = d['profile']['is_mentor'],
                            is_council = d['profile']['is_council'],
                            avatar_url = d['profile']['avatar_url'],
                            profile_url = d['profile']['profile_url'],
                            mentor = None,
                            country = d['profile']['country'],
                            city = d['profile']['city'],
                            last_report_date = last_report_date,
                            updated_date = timezone.now(),
                        )
                        r.save()
                
            self.stdout.write('Mentors data fetched. Please run manage.py fetch_data update')
        
        if 'update' in args:
            
            # Update just once a day
            try:
                s = Stat.objects.order_by('-date')
                if timezone.now() - s[0].date < datetime.timedelta(1):
                    do_update = False
                else:
                    do_update = True

            except:
                do_update = True
            
            if do_update:
                response = requests.get(BASE_URL + URL, verify=False)
            
                if not response.status_code == 200:
                    raise CommandError('Invalid Response')
        
                data = response.json()
                
                # to database
                reps = Rep.objects.filter(deleted=False).order_by('uri')
                        
                # Updating fields from data fetched
                for d in data['objects']:
                    
                    # Get mentor id
                    try:
                        mentor = Rep.objects.get(uri=d['profile']['mentor'])
                    except Rep.DoesNotExist:
                        mentor = None
                    
                    # If datetime is None, set it to 1970 to track it
                    if d['profile']['last_report_date'] is None:
                        last_report_date = datetime.date(1970, 1, 1)
                    else:
                        last_report_date =  datetime.datetime.strptime(d['profile']['last_report_date'], '%Y-%m-%d').date()
                            
                    try:
                        # If it's already on the database, update data
                        r = Rep.objects.get(uri=d['resource_uri'], deleted=False)
                        
                        r.first_name = d['first_name']
                        r.last_name = d['last_name']
                        r.is_mentor = d['profile']['is_mentor']
                        r.is_council = d['profile']['is_council']
                        r.avatar_url = d['profile']['avatar_url']
                        r.profile_url = d['profile']['profile_url']
                        r.mentor = mentor
                        r.country = d['profile']['country']
                        r.city = d['profile']['city']
                        r.last_report_date = last_report_date
                        r.updated_date = timezone.now()
                        
                        r.save()
                    except Rep.DoesNotExist:
                        # If it's not on the database we create it
                        r = Rep(
                            uri = d['resource_uri'],
                            first_name = d['first_name'],
                            last_name = d['last_name'],
                            is_mentor = d['profile']['is_mentor'],
                            is_council = d['profile']['is_council'],
                            avatar_url = d['profile']['avatar_url'],
                            profile_url = d['profile']['profile_url'],
                            mentor = mentor,
                            country = d['profile']['country'],
                            city = d['profile']['city'],
                            last_report_date = last_report_date,
                            updated_date = timezone.now(),
                        )
                        r.save()
                        
                    # check if someone was deleted from portal
                    for rep in reps:
                        if not any(rep.uri in d['resource_uri'] for d in data['objects']):
                            rep.deleted = True
                            rep.save()
                            print '%s is not longer on the portal, marking as deleted' % rep.full_name
                
                self.stdout.write('Profiles data updated')
                
                # Generate Stats
            
                # Query again with updated data
                reps = Rep.objects.filter(deleted=False).order_by('uri')
                
                s = Stat(
                    date = timezone.now(),
                    reps = reps.count(),
                    active = [r.status for r in reps].count('Active'),
                    casual = [r.status for r in reps].count('Casual'),
                    inactive = [r.status for r in reps].count('Inactive'),
                    orphans = reps.filter(mentor=None).count(),
                    mentors = reps.filter(is_mentor=True).count(),
                )
                
                s.save()
                
                self.stdout.write('Data stats updated')
            
            else:
                self.stdout.write('No need to update yet. Last update: %s' % s[0].date)
        
        if 'update_events' in args:
            
            new_url = URL_EVENTS
            count = 0
            
            events = Event.objects.filter(deleted=False)
            
            events_data = []
            
            while True:
                # Interate remote data in blocks
                response = requests.get(BASE_URL + new_url, verify=False)
            
                if not response.status_code == 200:
                    raise CommandError('Invalid Response')
        
                data = response.json()
                
                # Store data
                events_data.extend(data['objects'])
                
                new_url = data['meta'].get('next', None)
                
                if not new_url:
                    break
                        
            # Updating fields from data fetched
            
            for d in events_data:

                try:
                    # If it's already on the database, do some updates
                    e = Event.objects.get(uri=d['resource_uri'])
                    
                    # Update actual_attendance and bug/swag numbers
                    e.actual_attendance = d['actual_attendance']
                    e.budget_bug_id = d['budget_bug_id']
                    e.swag_bug_id = d['swag_bug_id']
                    e.save()
                    
                    # If we requested goals update
                    if 'goals' in args:
                        # Update goals
                        if d['goals']:
                            for goal in d['goals']:
                                try:
                                    goal = Goal.objects.get(name=goal['name'])
                                    e.goals.add(goal)
                                except:
                                    # If goal doesn't exist yet, we create it
                                    g = Goal(name=goal['name'])
                                    g.save()
                                    
                                    e.goals.add(g)
                    
                    # If we requested metrics update
                    if 'metrics' in args:
                        # Update metrics
                        if d['metrics']:
                            for metric in d['metrics']:
                                
                                try:
                                    m = Metric.objects.get(name=metric['metric']['name'])
                                except Metric.DoesNotExist:
                                    # If metric doesn't exist yet, we create it
                                    m = Metric(name=metric['metric']['name'])
                                    m.save()
                                    
                                try:
                                    # If that metric alredy exists for this event, update it
                                    event_metric = EventMetric.objects.get(metric=m, event=e)
                                    
                                    if 'outcome' in metric:
                                        event_metric.outcome = metric['outcome']

                                    if 'expected_outcome' in metric:
                                        event_metric.expected_outcome = metric['expected_outcome']
                                    
                                    event_metric.save()
                                    
                                except EventMetric.DoesNotExist:
                                    # If it's a new metric for this event, create it
                                    if 'outcome' in metric:
                                        event_metric = EventMetric(metric=m, event=e, expected_outcome=metric['expected_outcome'], outcome=metric['outcome'])
                                        event_metric.save()
                                    elif 'expected_outcome' in metric:
                                        event_metric = EventMetric(metric=m, event=e, expected_outcome=metric['expected_outcome'])
                                        event_metric.save()

                except Event.DoesNotExist:
                    # If it's not on the database we create it
                    
                    # Look for owner
                    try:
                        owner = Rep.objects.get(profile_url=d['owner_profile_url'])
                    except Rep.DoesNotExist:
                        owner = None
                    
                    e = Event(
                        uri = d['resource_uri'],
                        name = d['name'],
                        start = d['start']+'+00:00',
                        end = d['end']+'+00:00',
                        url = d['event_url'],
                        owner = owner,
                        mozilla_event = d['mozilla_event'],
                        country = d['country'],
                        city = d['city'],
                        estimated_attendance = d['estimated_attendance'],
                        actual_attendance = d['actual_attendance'],
                        budget_bug_id = d['budget_bug_id'],
                        swag_bug_id = d['swag_bug_id'],
                    )
                    e.save()
                    
                    # Add functional areas
                    if d['categories']:
                        for cat in d['categories']:
                            try:
                                area = FunctionalArea.objects.get(name=cat['name'])
                                e.categories.add(area)
                            except:
                                # If category doesn't exist yet, we create it
                                f = FunctionalArea(name=cat['name'])
                                f.save()
                                
                                e.categories.add(f)
                    
                    # Add goals
                    if d['goals']:
                        for goal in d['goals']:
                            try:
                                goal = Goal.objects.get(name=goal['name'])
                                e.goals.add(goal)
                            except:
                                # If category doesn't exist yet, we create it
                                g = Goal(name=goal['name'])
                                g.save()
                                
                                e.goals.add(g)
                    
                    # Update metrics
                    if d['metrics']:
                        for metric in d['metrics']:
                            
                            try:
                                m = Metric.objects.get(name=metric['metric']['name'])
                            except Metric.DoesNotExist:
                                # If metric doesn't exist yet, we create it
                                m = Metric(name=metric['metric']['name'])
                                m.save()
                                
                            try:
                                # If that metric alredy exists for this event, update it
                                event_metric = EventMetric.objects.get(metric=m, event=e)
                                
                                if 'outcome' in metric:
                                    event_metric.outcome = metric['outcome']

                                if 'expected_outcome' in metric:
                                    event_metric.expected_outcome = metric['expected_outcome']
                                
                                event_metric.save()
                                
                            except EventMetric.DoesNotExist:
                                # If it's a new metric for this event, create it
                                if 'outcome' in metric:
                                    event_metric = EventMetric(metric=m, event=e, expected_outcome=metric['expected_outcome'], outcome=metric['outcome'])
                                    event_metric.save()
                                elif 'expected_outcome' in metric:
                                    event_metric = EventMetric(metric=m, event=e, expected_outcome=metric['expected_outcome'])
                                    event_metric.save()
                    
                    count = count + 1
                    
            # check if there are events deleted from portal
            for event in events:
                if not any(event.uri in d['resource_uri'] for d in events_data):
                    event.deleted = True
                else:
                    event.deleted = False
                
                event.save()
                            
                
                    
            self.stdout.write('%i new events added' % count)