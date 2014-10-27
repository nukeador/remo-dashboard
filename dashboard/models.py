import datetime

from django.db import models


class Rep(models.Model):
    """Rep model."""
    uri = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_mentor = models.BooleanField(default=False)
    is_council = models.BooleanField(default=False)
    avatar_url = models.URLField(max_length=500)
    profile_url = models.URLField(max_length=500)
    mentor = models.ForeignKey('self', blank=True, null=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    last_report_date = models.DateField()
    deleted = models.BooleanField(default=False)
    updated_date = models.DateTimeField()
    
    
    def full_name(self):
        "Returns the rep's full name."
        return '%s %s' % (self.first_name, self.last_name)
    full_name = property(full_name)
    
    def status(self):
        '''
            Returns rep status based on last activity
            https://wiki.mozilla.org/Contribute/Conversion_points#Reps
        '''
        if (datetime.date.today() - self.last_report_date) < datetime.timedelta(31):
            return 'Active'
        elif (datetime.date.today() - self.last_report_date) < datetime.timedelta(57):
            return "Casual"
        else:
            return "Inactive"
    status = property(status)
    
    def mentees(self):
        "Returns rep mentees."
        mentees = Rep.objects.filter(mentor=self.id, deleted=False)
        return mentees
    mentees = property(mentees)
    
    def mentees_stats(self):
        "Returns rep mentees stats."
        mentees = Rep.objects.filter(mentor=self.id, deleted=False)
        
        active = 0
        casual = 0
        inactive = 0
        
        for m in mentees:
            if m.status == 'Active':
                active = active + 1
            if m.status == 'Casual':
                casual = casual + 1
            if m.status == 'Inactive':
                inactive = inactive + 1
                
        stats = {
            'active': active,
            'casual': casual,
            'inactive': inactive
        }
            
        return stats
    mentees_stats = property(mentees_stats)
    
    def __unicode__(self):
        return self.full_name
    
class Stat(models.Model):
    """ Model to store scheduled stats """
    
    date = models.DateTimeField()
    reps = models.IntegerField()
    active = models.IntegerField()
    casual = models.IntegerField()
    inactive = models.IntegerField()
    orphans = models.IntegerField()
    mentors = models.IntegerField()
    
    def __unicode__(self):
        return str(self.date)
