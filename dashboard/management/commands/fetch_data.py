import requests
import json

from os.path import dirname, join, realpath

from django.core.management.base import BaseCommand, CommandError

PROJECT_PATH = realpath(join(dirname(__file__), '../../../'))

BASE_URL = 'https://reps.mozilla.org'
URL = '/api/v1/rep/?format=json&limit=0'
FILE = PROJECT_PATH + '/reps.json'

class Command(BaseCommand):
    args = '<profiles events>'
    help = 'Fetch json data from Reps API'

    def handle(self, *args, **options):
        if 'profiles' in args:
            
            response = requests.get(BASE_URL + URL, verify=False)
        
            if not response.status_code == 200:
                raise CommandError('Invalid Response')

            data = response.json()
            
            with open(FILE, "w") as outfile:
                json.dump(data, outfile)
        
            self.stdout.write('Profiles data fetched to %s' % FILE)