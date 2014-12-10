from django.contrib import admin

from dashboard.models import Rep, Stat, Event, FunctionalArea, Goal, Metric, EventMetric

class RepAdmin(admin.ModelAdmin):
    model = Rep
    
    list_display = ('full_name', 'mentor', 'is_mentor', 'is_council', 'country', 'last_report_date', 'updated_date', 'status')
    list_filter = ['is_mentor', 'is_council', 'mentor']
    search_fields = ['first_name', 'last_name']

class MetricInline(admin.TabularInline):
    model = EventMetric
    extra = 1
    
class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ('name', 'owner', 'start', 'country', 'city', 'mozilla_event')
    list_filter = ['mozilla_event', 'deleted', 'start', 'categories', 'country']
    search_fields = ['name', 'country', 'city']
    inlines = (MetricInline,)
    
admin.site.register(Rep, RepAdmin)
admin.site.register(Stat)
admin.site.register(Event, EventAdmin)
admin.site.register(FunctionalArea)
admin.site.register(Goal)
admin.site.register(Metric)
admin.site.register(EventMetric)