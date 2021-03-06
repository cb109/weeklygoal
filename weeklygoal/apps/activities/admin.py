from django.contrib import admin
from django.utils.safestring import mark_safe

from weeklygoal.apps.activities.models import Activity, Event, UserSettings


def get_image_tag_for_activity(activity, max_width=64, max_height=64):
    if not activity.image:
        return ""
    return mark_safe(
        f"""
        <img
            src="{activity.image.url}"
            style="max-width: {max_width}px; height: auto; max-height: {max_height}px"
        >
    """
    )


class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "active",
        "user_name",
        "image_preview",
        "created_at",
        "modified_at",
        "id",
    )

    def user_name(self, activity):
        return activity.user.username

    def image_preview(self, activity):
        return get_image_tag_for_activity(activity)


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "activity_image",
        "created_at",
        "modified_at",
        "id",
    )

    def activity_image(self, event):
        return get_image_tag_for_activity(event.activity, max_width=32, max_height=32)


class UserSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "goal",
        "created_at",
        "modified_at",
        "id",
    )


admin.site.site_header = "Weekly Goal Admin"
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(UserSettings, UserSettingsAdmin)
