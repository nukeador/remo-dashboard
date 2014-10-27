import datetime
import requests
import json


from os.path import dirname, join, realpath

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from dashboard.models import Rep, Stat

PROJECT_PATH = realpath(join(dirname(__file__), '../../../'))

BASE_URL = 'https://reps.mozilla.org'
URL = '/api/v1/rep/?format=json&limit=0'
FILE = PROJECT_PATH + '/reps.json'

class Command(BaseCommand):
    args = '<profiles events>'
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
                        r.mentor = None
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
            response = requests.get(BASE_URL + URL, verify=False)
        
            if not response.status_code == 200:
                raise CommandError('Invalid Response')
    
            data = response.json()
            
            # to local file
            with open(FILE, "w") as outfile:
                json.dump(data, outfile)
            
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