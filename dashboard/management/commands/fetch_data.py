import datetime
import requests
import json


from os.path import dirname, join, realpath

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from dashboard.models import Rep

PROJECT_PATH = realpath(join(dirname(__file__), '../../../'))

BASE_URL = 'https://reps.mozilla.org'
URL = '/api/v1/rep/?format=json&limit=0'
FILE = PROJECT_PATH + '/reps.json'

class Command(BaseCommand):
    args = '<profiles events>'
    help = 'Fetch json data from Reps API'

    def handle(self, *args, **options):
        
        if 'update' in args:
            response = requests.get(BASE_URL + URL, verify=False)
        
            if not response.status_code == 200:
                raise CommandError('Invalid Response')
    
            data = response.json()
            
            # to local file
            with open(FILE, "w") as outfile:
                json.dump(data, outfile)
            
            # to database
            reps = Rep.objects.filter(deleted=False).order_by('first_name')
            
            # check if someone was deleted from portal
            for rep in reps:
                if not any(rep.uri in d['resource_uri'] for d in data['objects']):
                    rep.deleted = True
                    rep.save()
                    print '%s is not longer on the portal, marking as deleted' % rep.full_name
                    
            # Updating fields from data fetched
            for d in data['objects']:
                try:
                    # If it's already on the database
                    r = Rep.objects.get(uri=d['resource_uri'], deleted=False)
                    
                    r.first_name = d['first_name']
                    r.last_name = d['last_name']
                    r.is_mentor = d['profile']['is_mentor']
                    r.is_council = d['profile']['is_council']
                    r.avatar_url = d['profile']['avatar_url']
                    r.profile_url = d['profile']['profile_url']
                    r.mentor = d['profile']['mentor']
                    r.country = d['profile']['country']
                    r.city = d['profile']['city']
                    r.last_report_date = datetime.date.today() #FIXME
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
                        mentor = d['profile']['mentor'],
                        country = d['profile']['country'],
                        city = d['profile']['city'],
                        last_report_date = datetime.date.today(), #FIXME
                        updated_date = timezone.now(),
                    )
                    r.save()
            
            self.stdout.write('Profiles data updated')
        
        if 'init' in args:
            
            response = requests.get(BASE_URL + URL, verify=False)
        
            if not response.status_code == 200:
                raise CommandError('Invalid Response')

            data = response.json()
            
            # to local file
            with open(FILE, "w") as outfile:
                json.dump(data, outfile)
            
            # to database
            for rep in data['objects']:
                r = Rep(
                    uri = rep['resource_uri'],
                    first_name = rep['first_name'],
                    last_name = rep['last_name'],
                    is_mentor = rep['profile']['is_mentor'],
                    is_council = rep['profile']['is_council'],
                    avatar_url = rep['profile']['avatar_url'],
                    profile_url = rep['profile']['profile_url'],
                    mentor = rep['profile']['mentor'],
                    country = rep['profile']['country'],
                    city = rep['profile']['city'],
                    last_report_date = datetime.date.today(), #FIXME
                    updated_date = timezone.now(),
                )
                r.save()
                
            self.stdout.write('Profiles data fetched to %s' % FILE)