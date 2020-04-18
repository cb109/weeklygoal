from django.contrib import admin
from django.utils.safestring import mark_safe

from weeklygoal.apps.activities.models import Activity


class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "image_preview",
        "created_at",
        "modified_at",
        "id",
    )

    def image_preview(self, activity):
        if not activity.image:
            return ""
        return mark_safe(
            f"""
            <img
              src="{activity.image.url}"
              style="max-width: 64px; height: auto; max-height: 64px"
            >
        """
        )


admin.site.site_header = "Weekly Goal Admin"
admin.site.register(Activity, ActivityAdmin)
