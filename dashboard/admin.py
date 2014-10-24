from django.contrib import admin

from dashboard.models import Rep

class RepAdmin(admin.ModelAdmin):
    model = Rep
    
    list_display = ('full_name', 'mentor', 'is_mentor', 'is_council', 'country', 'last_report_date', 'updated_date', 'status')
    list_filter = ['is_mentor', 'is_council', 'mentor']
    search_fields = ['first_name', 'last_name']
    
admin.site.register(Rep, RepAdmin)