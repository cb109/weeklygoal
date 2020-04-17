from django.contrib import admin

from weeklygoal.apps.activities.models import Activity

admin.site.site_header = "Weekly Goal Admin"
admin.site.register(Activity)
