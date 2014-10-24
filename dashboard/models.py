from django.db import models


class Rep(models.Model):
    """Rep model."""
    uri = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_mentor = models.BooleanField(default=False)
    is_council = models.BooleanField(default=False)
    avatar_url = models.URLField(max_length=100)
    profile_url = models.URLField(max_length=100)
    mentor = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    last_report_date = models.DateField()
    deleted = models.BooleanField(default=False)
    updated_date = models.DateTimeField()
    
    
    def _get_full_name(self):
        "Returns the rep's full name."
        return '%s %s' % (self.first_name, self.last_name)
    full_name = property(_get_full_name)
    
    
    def __unicode__(self):
        return self._get_full_name()